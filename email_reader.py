import imaplib
import email
from email.header import decode_header
import os

def clean(text):
    return ''.join(c if c.isalnum() else "_" for c in text)

def get_unread_emails(username: str, password: str) -> str:
    try:
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(username, password)
        imap.select("inbox")

        status, messages = imap.search(None, 'UNSEEN')
        if status != "OK":
            return "Could not fetch emails."

        mail_ids = messages[0].split()
        if not mail_ids:
            return ""

        result = []
        for mail_id in mail_ids:
            _, msg_data = imap.fetch(mail_id, "(RFC822)")
            if _ != "OK":
                continue

            msg = email.message_from_bytes(msg_data[0][1])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")

            from_ = msg.get("From", "Unknown")
            date_ = msg.get("Date", "Unknown")

            # Extract email body (only plain text)
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        try:
                            body = part.get_payload(decode=True).decode()
                            break
                        except:
                            continue
            else:
                body = msg.get_payload(decode=True).decode()

            body = body.strip().replace("\r\n", "\n")
            result.append(f"From: {from_}\nDate: {date_}\nSubject: {subject}\n\n{body}\n{'-'*40}")

        imap.logout()
        return f"{len(result)} unread emails found:\n\n" + "\n\n".join(result)

    except Exception as e:
        print("❌ Error in get_unread_emails():", e)
        return ""
