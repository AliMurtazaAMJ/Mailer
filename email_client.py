"""Email client functionality for Gmail operations."""

import os
import smtplib
import imaplib
import email
import time
import json
from email.mime.text import MIMEText
from email.header import decode_header
from config import *

def create_cache_dir():
    """Create cache directory if it doesn't exist."""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

def get_cache():
    """Get cached emails if available and not expired."""
    create_cache_dir()
    
    if not os.path.exists(CACHE_FILE):
        return None
    
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
        
        cache_time = cache_data.get('timestamp', 0)
        if time.time() - cache_time > CACHE_EXPIRY:
            return None
        
        return cache_data.get('emails', None)
    except (json.JSONDecodeError, IOError):
        return None

def save_cache(emails):
    """Save emails to cache."""
    create_cache_dir()
    
    cache_data = {
        'timestamp': time.time(),
        'emails': emails
    }
    
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2)

def get_emails(use_cache=True):
    """Fetch emails from Gmail inbox."""
    if use_cache:
        cached_emails = get_cache()
        if cached_emails:
            print(f"📄 Using cached emails ({len(cached_emails)} messages)")
            return cached_emails
    
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(EMAIL, PASSWORD)
        mail.select('INBOX')

        result, data = mail.search(None, 'ALL')
        email_ids = data[0].split()
        
        latest_emails = email_ids[-MAX_EMAILS:] if len(email_ids) > MAX_EMAILS else email_ids
        emails = []
        
        for i in range(0, len(latest_emails), BATCH_SIZE):
            batch = latest_emails[i:i+BATCH_SIZE]
            batch_emails = process_email_batch(mail, batch)
            emails.extend(batch_emails)
        
        mail.close()
        mail.logout()
        
        save_cache(emails)
        print(f"⚡ Fetched {len(emails)} emails")
        
        return emails
    
    except Exception as e:
        print(f"Error retrieving emails: {e}")
        return []

def process_email_batch(mail, email_ids):
    """Process a batch of emails efficiently."""
    emails = []
    
    for e_id in reversed(email_ids):
        try:
            result, data = mail.fetch(e_id, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            emails.append({
                'id': e_id.decode(),
                'subject': decode_email_header(msg['Subject']),
                'sender': decode_email_header(msg['From']),
                'date': decode_email_header(msg['Date']),
                'body': extract_email_body(msg)
            })
        except Exception as e:
            print(f"Warning: Could not process email {e_id}: {e}")
    
    return emails

def extract_email_body(msg):
    """Extract email body efficiently."""
    body = ""
    
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            
            if "attachment" in content_disposition:
                continue
            
            if content_type == "text/plain":
                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        charset = part.get_content_charset() or 'utf-8'
                        body = payload.decode(charset, errors='replace')
                        break
                except Exception:
                    pass
    else:
        try:
            payload = msg.get_payload(decode=True)
            if payload:
                charset = msg.get_content_charset() or 'utf-8'
                body = payload.decode(charset, errors='replace')
        except Exception:
            body = "Could not decode message body"
    
    return body

def decode_email_header(header):
    """Decode email header properly."""
    if not header:
        return "None"
    
    try:
        decoded_header = decode_header(header)
        result = ""
        for data, encoding in decoded_header:
            if isinstance(data, bytes):
                if encoding:
                    result += data.decode(encoding)
                else:
                    result += data.decode('utf-8', errors='replace')
            else:
                result += str(data)
        return result
    except Exception:
        return str(header)

def send_email(to, subject, body):
    """Send an email message using SMTP."""
    try:
        msg = MIMEText(body)
        msg['From'] = EMAIL
        msg['To'] = to
        msg['Subject'] = subject
        
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f'Message sent to {to}!')
        return True
    
    except Exception as e:
        print(f'Error sending email: {e}')
        return False