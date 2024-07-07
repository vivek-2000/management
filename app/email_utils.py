import logging
from aiosmtplib import SMTP, SMTPException, send
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from fastapi import HTTPException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

async def send_invitation_email(email):
    message = EmailMessage()
    message["From"] = os.getenv('EMAIL_USERNAME')
    message["To"] = email
    message["Subject"] = "API Documentation Invitation"
    message.set_content("""
Hello,

We are excited to invite you to view our User Management API documentation on ReDoc.

You can access the documentation by clicking the button below:

View API Documentation

As per the Requirements, I changed that 'Any' method because of Flutter.

I have also set up an AWS EC2 instance for the public IP, used Reverse Proxy for port forwarding, and GCP Postgres for the database.

We appreciate your time and look forward to your feedback.

Thank you,
Ulrich Bachmann

If you have any questions, feel free to reply to this email.
    """)
    message.add_alternative("""
<!DOCTYPE html>
<html>
<head>
    <title>API Documentation Invitation</title>
</head>
<body>
    <div style="font-family: Arial, sans-serif; text-align: center;">
        <h2 style="background-color: #4CAF50; color: white; padding: 10px;">API Documentation Invitation</h2>
        <p>Hello,</p>
        <p>We are excited to invite you to view our User Management API documentation on <strong>ReDoc</strong>.</p>
        <p>You can access the documentation by clicking the button below:</p>
        <a href="https://user-management.koyeb.app/redoc" style="display: inline-block; padding: 10px 20px; font-size: 16px; color: white; background-color: #4CAF50; text-decoration: none; border-radius: 5px;">View API Documentation</a>
        <p>I am not able to use GCP due to unavailability of credit card </p>
        <br>
        <p>Thank you,</p>
        <p>Vivek Kumar Patel</p>
        <p>If you have any questions, feel free to reply to this email.</p>
    </div>
</body>
</html>
    """, subtype="html")

    try:
        await send(
            message,
            hostname="smtp.gmail.com",
            port=587,
            start_tls=True,
            username=os.getenv('EMAIL_USERNAME'),
            password=os.getenv('EMAIL_PASSWORD'),
        )
        print("Email sent successfully")
        return {"status": "Email sent successfully"}
    except SMTPException as e:
        logger.error(f"Failed to send email: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")
