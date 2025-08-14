import os
import imaplib
import email
import re
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

def clean_html(raw_html):
    """Remove HTML tags and extra spaces from email content."""
    soup = BeautifulSoup(raw_html, "html.parser")
    return re.sub(r"\s+", " ", soup.get_text()).strip()

def connect_mailbox():
    """Connect to Zoho Mail using IMAP credentials from .env."""
    mail = imaplib.IMAP4_SSL(os.getenv("IMAP_SERVER"))
    mail.login(os.getenv("EMAIL_ACCOUNT"), os.getenv("PASSWORD"))
    mail.select("inbox")
    return mail

def fetch_latest_emails(n=5):
    """Fetch latest N emails as dicts, newest first."""
    mail = connect_mailbox()
    status, email_ids = mail.search(None, "ALL")
    ids = email_ids[0].split()[::-1]  # Newest first
    latest_ids = ids[:n]
    
    emails_list = []
    for eid in latest_ids:
        status, msg_data = mail.fetch(eid, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        subject = msg["subject"] or "(No Subject)"
        from_ = msg["from"] or "(Unknown sender)"
        
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body += part.get_payload(decode=True).decode(errors="ignore")
                elif part.get_content_type() == "text/html" and not body:
                    body += clean_html(part.get_payload(decode=True).decode(errors="ignore"))
        else:
            body += clean_html(msg.get_payload(decode=True).decode(errors="ignore"))
        
        # Store as dict instead of string
        emails_list.append({
            "from": from_,
            "subject": subject,
            "body": body.strip()
        })
    
    mail.logout()
    
    # Save to file (optional)
    with open("emails.json", "w", encoding="utf-8") as f:
        json.dump(emails_list, f, ensure_ascii=False, indent=2)

    return emails_list

