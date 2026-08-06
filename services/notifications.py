import os


def send_notification(user_email, subject, message):
    if not user_email:
        return False

    try:
        from dotenv import load_dotenv
        load_dotenv()
    except Exception:
        pass

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT", "587")
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not all([smtp_host, smtp_user, smtp_password]):
        return False

    try:
        import smtplib
        from email.message import EmailMessage

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = smtp_user
        msg["To"] = user_email
        msg.set_content(message)

        with smtplib.SMTP(smtp_host, int(smtp_port)) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        return True
    except Exception:
        return False
