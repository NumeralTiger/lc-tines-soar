import os, smtplib
from email.message import EmailMessage
import requests

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USERNAME")
SMTP_PASS = os.getenv("SMTP_PASSWORD")
ALERT_TO = os.getenv("ALERT_TO_EMAIL")

def send_slack_alert(text: str, blocks=None):
    if not SLACK_WEBHOOK:
        raise EnvironmentError("SLACK_WEBHOOK_URL missing")
    payload = {"text": text}
    if blocks:
        payload["blocks"] = blocks
    r = requests.post(SLACK_WEBHOOK, json=payload, timeout=10)
    r.raise_for_status()
    return r.status_code

def send_email(subject: str, body: str, to_addr=ALERT_TO):
    if not (SMTP_SERVER and SMTP_USER and SMTP_PASS and to_addr):
        raise EnvironmentError("SMTP environment incomplete")
    msg = EmailMessage()
    msg["From"] = SMTP_USER
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.set_content(body)
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=20) as s:
        s.starttls()
        s.login(SMTP_USER, SMTP_PASS)
        s.send_message(msg)
    return True
