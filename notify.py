"""Email queued paper-trading reports (data/paper/outbox.json) with a link to the report on GitHub.

Env: SMTP_USER, SMTP_PASS (Gmail app password), MAIL_TO; optional SMTP_HOST, SMTP_PORT.
"""
import html
import json
import os
import smtplib
import ssl
import sys
from email.message import EmailMessage

import reporting as R

ROOT = os.path.dirname(os.path.abspath(__file__))
OUTBOX = os.path.join(ROOT, "data", "paper", "outbox.json")


def main():
    if "--test" in sys.argv:
        box = [{"path": "reports/paper/latest.md", "subject": "[Paper trade] Test email - setup check"}]
    elif os.path.exists(OUTBOX):
        with open(OUTBOX) as f:
            box = json.load(f)
    else:
        print("nothing to send")
        return
    user, pw, to = os.environ.get("SMTP_USER"), os.environ.get("SMTP_PASS"), os.environ.get("MAIL_TO")
    if not (user and pw and to):
        print(f"email not configured; {len(box)} report(s) left in outbox")
        return
    repo = f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/{os.environ.get('GITHUB_REPOSITORY', '')}"
    branch = os.environ.get("GITHUB_REF_NAME", "main")
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL(os.environ.get("SMTP_HOST", "smtp.gmail.com"),
                          int(os.environ.get("SMTP_PORT", "465")), context=ctx) as s:
        s.login(user, pw)
        for item in box:
            path = os.path.join(ROOT, item["path"])
            if not os.path.exists(path):
                continue
            with open(path) as f:
                text = f.read()
            link = f"{repo}/blob/{branch}/{item['path']}"
            site = os.environ.get("SITE_URL") or None
            msg = EmailMessage()
            msg["Subject"], msg["From"], msg["To"] = item["subject"], user, to
            msg.set_content(f"Dashboard: {site or '-'}\nGitHub: {link}\n\n{text}")
            msg.add_alternative(R.email_html(text, html.escape(link), site and html.escape(site)), subtype="html")
            s.send_message(msg)
            print("sent:", item["subject"])
    if os.path.exists(OUTBOX):
        os.remove(OUTBOX)


if __name__ == "__main__":
    main()
