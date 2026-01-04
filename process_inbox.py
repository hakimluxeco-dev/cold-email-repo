import imaplib
import email
from email.header import decode_header
import re
import getpass
import time
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# Configuration
IMAP_SERVER = "imap.gmail.com"
LEADS_FILE = "remaining_leads.md"

def connect_imap(user, password):
    print("Connecting to IMAP server...")
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(user, password)
    return mail

def get_email_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get("Content-Disposition"))
            # skip any text/plain (txt) attachments
            if ctype == "text/plain" and "attachment" not in cdispo:
                return part.get_payload(decode=True).decode()
    else:
        return msg.get_payload(decode=True).decode()
    return ""

def scan_inbox(user, password, unique_lead_emails):
    mail = connect_imap(user, password)
    mail.select("inbox")
    
    # Dictionary to store status updates: {email: new_status}
    updates = {}
    
    # 1. Check for Bounces
    print("Scanning for bounces...")
    # Search for emails from mailer-daemon
    # IMAP OR syntax: OR <key1> <key2>
    status, messages = mail.search(None, '(OR FROM "mailer-daemon" FROM "postmaster")')
    if status == "OK":
        for num in messages[0].split():
            res, msg_data = mail.fetch(num, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])
            body = get_email_body(msg).lower()
            
            for lead_email in unique_lead_emails:
                if lead_email in body:
                    print(f"BOUNCE DETECTED for: {lead_email}")
                    updates[lead_email] = "Inactive"
    
    # 2. Check for Replies
    print("Scanning for replies...")
    # Search for unread emails first or all? Let's check all recent.
    # To avoid re-processing old ones, we rely on the fact that status is updated.
    # But better to check ALL for now since volume is low.
    status, messages = mail.search(None, 'ALL')
    if status == "OK":
        email_ids = messages[0].split()
        # Process latest 50 for efficiency
        for num in email_ids[-50:]: 
            res, msg_data = mail.fetch(num, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])
            
            # Get sender email
            from_header = msg.get("From")
            sender_email = re.search(r'<(.+?)>', from_header)
            if sender_email:
                sender_email = sender_email.group(1).lower().strip()
            else:
                sender_email = from_header.lower().strip() # Fallback
                
            if sender_email in unique_lead_emails:
                # Analyze sentiment
                subject = msg.get("Subject", "").lower()
                body = get_email_body(msg).lower()
                full_text = subject + " " + body
                
                print(f"REPLY DETECTED from: {sender_email}")
                
                # Simple keyword analysis
                if any(x in full_text for x in ["stop", "unsubscribe", "remove", "not interested", "no thanks"]):
                    updates[sender_email] = "Not Interested"
                elif any(x in full_text for x in ["demo", "yes", "interested", "price", "call", "meet", "how much"]):
                    updates[sender_email] = "Interested"
                else:
                    updates[sender_email] = "Interested" # Default to positive if they reply
                    
    mail.close()
    mail.logout()
    return updates

def update_leads_file(file_path, status_updates):
    if not status_updates:
        print("No updates found.")
        return

    print(f"Updating {len(status_updates)} leads...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    headers_parsed = False
    
    forToUpdate = status_updates.copy()
    
    for line in lines:
        stripped = line.strip()
        
        # Identify table rows
        if stripped.startswith("|") and not "---" in stripped and "Business Name" not in stripped:
            cols = [c.strip() for c in stripped.split('|')]
            # Expected parsed indices: 
            # ['', '1', 'Name', 'Type', 'Area', 'Phone', 'Email', 'Source', 'Icebreaker', 'Status', '']
            if len(cols) >= 10:
                email_addr = cols[6].lower().strip()
                
                if email_addr in forToUpdate:
                    new_status = forToUpdate[email_addr]
                    # Update status column (Index 9)
                    cols[9] = f" {new_status} "
                    # Reconstruct line
                    new_line = "|" + "|".join(cols[1:-1]) + "|\n" 
                    # Note: cols[1:-1] drops the empty first/last from split
                    # But join needs to handle the separators correctly.
                    # safer to just construct it manually
                    
                    # Reconstruction logic:
                    # cols is ['', '#', 'Name', ..., 'Status', '']
                    # We want to keep original spacing if possible, but simplest is to just rebuild with basic padding
                    
                    # Let's try to be respectful of original line, but updating one column
                    # is tricky with split. Rebuilding is safer for data integrity.
                    rebuilt = "|"
                    for i in range(1, len(cols)-1):
                        rebuilt += f" {cols[i]} |"
                    new_line = rebuilt + "\n"
                    
                    new_lines.append(new_line)
                    print(f"Updated {email_addr} -> {new_status}")
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
            
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("File updated successfully.")


def main():
    print("--- Inbox Processor (Continuous Mode) ---")
    
    email_user = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASSWORD")

    if not email_user or not email_password or "ReplaceData" in email_password:
        print("Credentials not found in .env file.")
        email_user = input("Enter your email address: ")
        email_password = getpass.getpass("Enter your email app password: ")
    else:
        print(f"Logged in as: {email_user}")
    
    print("\nStarting continuous monitoring... Press Ctrl+C to stop.")
    
    try:
        while True:
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"\n[{current_time}] Starting scan cycle...")
            
            # 1. Parse leads fresh every time (in case file was updated manually)
            unique_emails = set()
            try:
                with open(LEADS_FILE, 'r', encoding='utf-8') as f:
                    for line in f:
                        if "|" in line and "Business Name" not in line and "---" not in line:
                            parts = line.split('|')
                            if len(parts) >= 7:
                                email_addr = parts[6].strip().lower()
                                if "@" in email_addr:
                                    unique_emails.add(email_addr)
            except Exception as e:
                print(f"Error reading leads file: {e}")
                time.sleep(60)
                continue
            
            print(f"Monitoring {len(unique_emails)} leads.")
            
            # 2. Scan & Update
            try:
                updates = scan_inbox(email_user, email_password, unique_emails)
                update_leads_file(LEADS_FILE, updates)
            except Exception as e:
                print(f"Error during scan: {e}")
            
            # 3. Wait
            print("Cycle complete. Waiting 30 minutes...")
            time.sleep(1800)
            
    except KeyboardInterrupt:
        print("\nStopping Inbox Processor.")

if __name__ == "__main__":
    main()
