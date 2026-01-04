import csv
import io
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Lead

async def process_import(file_content: str, filename: str, db: AsyncSession):
    """
    Generic importer that dispatches to specific parsers based on file extension.
    """
    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    
    if ext == 'csv':
        return await _parse_csv(file_content, db)
    elif ext == 'txt':
        return await _parse_txt(file_content, db)
    else:
        # Default to markdown for .md and others
        return await _parse_markdown(file_content, db)

async def _parse_csv(content: str, db: AsyncSession):
    imported_count = 0
    f = io.StringIO(content)
    reader = csv.reader(f)
    try:
        header = next(reader)
    except StopIteration:
        return 0
        
    # Find indices with flexible matching
    headers_lower = [h.lower().strip() for h in header]
    
    email_idx = -1
    name_idx = -1
    
    for i, col in enumerate(headers_lower):
        if 'email' in col:
            email_idx = i
        if 'business' in col or ('name' in col and 'business' not in col): # Prioritize business name, fallback to name
            if name_idx == -1: name_idx = i
            if 'business' in col: name_idx = i
            
    if email_idx == -1:
        email_idx = 0 # Fallback
        
    seen_emails = set()

    for row in reader:
        if not row: continue
        if len(row) <= email_idx: continue
        
        raw_email = row[email_idx].strip().lower()
        if "@" not in raw_email: continue
        
        # Sanitize
        if ' ' in raw_email:
            email = raw_email.split(' ')[0]
        else:
            email = raw_email
        email = email.replace("(", "").replace(")", "")
        
        if email in seen_emails:
            continue
        seen_emails.add(email)
        
        name = "Unknown"
        if name_idx != -1 and len(row) > name_idx:
            name = row[name_idx].strip()
            
        if await _add_lead_if_new(db, email, name, "Imported CSV"):
            imported_count += 1
            
    await db.commit()
    return imported_count

async def _parse_txt(content: str, db: AsyncSession):
    imported_count = 0
    lines = content.splitlines()
    for line in lines:
        email = line.strip().lower()
        if "@" in email:
            if await _add_lead_if_new(db, email, "Unknown", "Imported TXT"):
                imported_count += 1
    await db.commit()
    return imported_count

async def _add_lead_if_new(db: AsyncSession, email: str, name: str, source: str, **kwargs):
    # Check existence
    result = await db.execute(select(Lead).where(Lead.email == email))
    existing = result.scalars().first()
    
    if not existing:
        new_lead = Lead(
            name=name,
            email=email,
            source=source,
            status="Pending",
            **kwargs
        )
        db.add(new_lead)
        return True
    return False

async def _parse_markdown(file_content: str, db: AsyncSession):
    """
    Parses Markdown tables with dynamic header detection.
    """
    lines = file_content.splitlines()
    imported_count = 0
    
    print(f"DEBUG: Parsing lines: {len(lines)}")
    
    # Find header and detect column positions
    email_idx, name_idx, source_idx, ice_idx = None, None, None, None
    
    for line in lines:
        stripped = line.strip()
        if not stripped or not stripped.startswith("|"):
            continue
        
        # Check for header keywords
        if any(kw in stripped.lower() for kw in ["email", "business", "name"]):
            print(f"DEBUG: Found likely header: {stripped}")
            cols = [c.strip().lower() for c in stripped.split('|')]
            
            for i, col in enumerate(cols):
                if 'email' in col and 'whatsapp' not in col:
                    email_idx = i
                if 'business' in col or ('name' in col and name_idx is None):
                    name_idx = i
                if 'source' in col:
                    source_idx = i
                if 'ice' in col:
                    ice_idx = i
            
            print(f"DEBUG: Indices found - Email: {email_idx}, Name: {name_idx}")
            if email_idx is not None and name_idx is not None:
                break
    
    # Fallback if no headers found
    if email_idx is None or name_idx is None:
        print("DEBUG: No headers found, using fallbacks.")
        email_idx, name_idx, source_idx, ice_idx = 6, 2, 7, 8
    
    # Track locally seen emails to prevent batch duplicates
    seen_emails = set()
    
    # Parse data rows
    for line in lines:
        stripped = line.strip()
        
        # Skip non-table lines
        if not stripped or not stripped.startswith("|") or "---" in stripped:
            continue
        
        # Skip header rows
        if any(kw in stripped.lower() for kw in ["business name", "email address"]):
            continue
        
        # Determine actual max index needed
        needed_idx = max(email_idx, name_idx)
        
        cols = [c.strip() for c in stripped.split('|')]
        print(f"DEBUG: Processing row with {len(cols)} columns (Needed: {needed_idx})")
        
        try:
            if len(cols) > needed_idx:
                name = cols[name_idx].replace("**", "").strip()
                # Sanitize email (remove ' (likely)', etc)
                raw_email = cols[email_idx].strip().lower()
                # Simple extraction: take first part if space exists, or regex
                if ' ' in raw_email:
                    email = raw_email.split(' ')[0]
                else:
                    email = raw_email
                
                # Further cleanup if needed (remove parens)
                email = email.replace("(", "").replace(")", "")
                
                # Check duplication within file
                if email in seen_emails:
                    print(f"DEBUG: Skipping duplicate in file: {email}")
                    continue
                seen_emails.add(email)
                
                print(f"DEBUG: Extracting - Name: {name}, Email: {email}")
                source = cols[source_idx].strip() if source_idx and len(cols) > source_idx else "Imported"
                icebreaker = cols[ice_idx].strip() if ice_idx and len(cols) > ice_idx else ""
                
                if "@" in email and "." in email and name:
                    if await _add_lead_if_new(db, email, name, source, icebreaker=icebreaker):
                        imported_count += 1
        except:
            continue
    
    await db.commit()
    return imported_count
