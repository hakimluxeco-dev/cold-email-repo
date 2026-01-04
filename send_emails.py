import time
import smtplib
import csv
import re
import getpass
import os
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
# You will be prompted for these when you run the script
SMTP_SERVER = "smtp.gmail.com" # Change to smtp.office365.com for Outlook
SMTP_PORT = 587
SENT_LOG_FILE = "sent_emails.log"

def load_sent_emails():
    """Load the set of already sent email addresses from the log file."""
    if not os.path.exists(SENT_LOG_FILE):
        return set()
    
    with open(SENT_LOG_FILE, 'r', encoding='utf-8') as f:
        # Read lines, strip whitespace, and filter out empty lines
        return set(line.strip() for line in f if line.strip())

def log_sent_email(email):
    """Append a successfully sent email address to the log file."""
    with open(SENT_LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{email}\n")

def parse_markdown_leads(file_path):
    leads = []
    seen_emails = set()
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Simple markdown table parser
    start_parsing = False
    headers = []
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
            
        if stripped.startswith("|") and "Business Name" in stripped and not headers:
            headers = [h.strip() for h in stripped.split('|') if h.strip()]
            continue
            
        if stripped.startswith("|") and "---" in stripped:
            start_parsing = True
            continue
            
        if start_parsing and stripped.startswith("|"):
            cols = [c.strip() for c in stripped.split('|')]
            # Markdown splitter often leaves empty first/last elements
            # | # | Business Name | Type | Area | WhatsApp | Email | Source | Icebreaker |
            # split results in: ['', ' # ', ' Business Name ', ..., ' Source ', ' Icebreaker ', '']
            
            # Using specific indices based on standard md table split:
            # 2 = Name, 6 = Email, 7 = Source, 8 = Icebreaker (if present)
            
            if len(cols) >= 8:
                try:
                    name = cols[2].strip()
                    email = cols[6].strip()
                    # If splits are correct, Icebreaker should be at index 8?
                    # Let's verify standard structure: 
                    # ['', '1', 'Name', 'Type', 'Area', 'Phone', 'Email', 'Source', 'Icebreaker', ''] -> 10 elements
                    icebreaker = cols[8].strip() if len(cols) > 8 else ""
                except IndexError:
                    icebreaker = ""
                
                # Basic validation
                if "@" in email and "Business Name" not in name and "---" not in name:
                    clean_email = email.lower().strip()
                    if clean_email not in seen_emails:
                        leads.append({
                            "name": name, 
                            "email": email,
                            "icebreaker": icebreaker
                        })
                        seen_emails.add(clean_email)
                    else:
                        print(f"DEBUG: Skipping duplicate email in list: {name} ({email})")

    return leads

def load_template(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def connect_smtp(user, password):
    """Establishes and returns an SMTP connection."""
    print("Connecting to SMTP server...")
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(user, password)
    print("Connected!")
    return server

def send_emails():
    print("--- Cold Email Automation ---")
    
    email_user = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASSWORD")
    
    if not email_user or not email_password or "ReplaceData" in email_password:
        print("Credentials not found in .env file.")
        email_user = input("Enter your email address: ")
        email_password = getpass.getpass("Enter your email app password: ")
    else:
        print(f"Logged in as: {email_user}")
    
    # Use relative paths for the copied files
    leads_file = "remaining_leads.md"
    template_file = "cold_email_template.md"
    
    # Load sent history
    sent_emails_history = load_sent_emails()
    print(f"Loaded {len(sent_emails_history)} previously sent emails from log.")

    print(f"Reading leads from: {leads_file}")
    leads = parse_markdown_leads(leads_file)
    print(f"Found {len(leads)} unique leads with email addresses.")
    
    template_raw = load_template(template_file)
    
    # Extract subject and body from template artifact
    subject = "Quick idea for " 
    
    # Clean up template body (remove markdown headers)
    body_start = template_raw.find("Hi [Name")
    if body_start != -1:
        body_template = template_raw[body_start:]
    else:
        body_template = template_raw # Fallback
        
    print("\n--- Starting Sending Process ---")
    
    server = None
    
    try:
        # Initial connection
        server = connect_smtp(email_user, email_password)
        
        for lead in leads:
            b_name = lead['name'].replace("**", "") # Clean markdown bold
            b_email = lead['email']
            b_icebreaker = lead.get('icebreaker', f"I came across {b_name}.") # Fallback
            
            # Check history
            if b_email in sent_emails_history:
                print(f"Skipping {b_name}: Emailed already ({b_email})")
                continue

            if "Likely" in b_email or "Placeholder" in b_email:
                print(f"Skipping {b_name}: Email marked as Placeholder/Likely")
                continue
                
            # Personalize
            msg_subject = subject + b_name
            msg_body = body_template.replace("[Business Name]", b_name) \
                                    .replace("[Name/Owner Name]", "there") \
                                    .replace("[Icebreaker]", b_icebreaker)
            
            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = b_email
            msg['Subject'] = msg_subject
            msg.attach(MIMEText(msg_body, 'plain'))
            
            # Retry loop for sending
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    if server is None:
                         server = connect_smtp(email_user, email_password)

                    server.send_message(msg)
                    print(f"SENT: {b_name} <{b_email}>")
                    log_sent_email(b_email) # Update log immediately
                    
                    # Random delay between 10 and 20 minutes (600 to 1200 seconds)
                    delay = random.randint(600, 1200)
                    print(f"Waiting {delay} seconds (approx {round(delay/60, 1)} mins) before the next email...")
                    time.sleep(delay)
                    break # Success, move to next lead
                
                except Exception as e:
                    print(f"Attempt {attempt+1} failed for {b_name}: {e}")
                    # Try to close and clear the server to force reconnection next loop
                    try:
                        server.quit()
                    except:
                        pass
                    server = None
                    
                    if attempt < max_retries - 1:
                        print("Waiting 30 seconds before reconnecting/retrying...")
                        time.sleep(30)
                    else:
                        print(f"FAILED PERMANENTLY: {b_name} - giving up on this lead.")
                
        if server:
            server.quit()
        print("\nAll done!")
        
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    except Exception as e:
        print(f"\nCritical Error: {e}")
        print("Note: If using Gmail, make sure to use an 'App Password', not your main password.")

if __name__ == "__main__":
    send_emails()
