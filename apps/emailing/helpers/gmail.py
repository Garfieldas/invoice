from django.core.mail import send_mail
from django.conf import settings
from emailing.helpers.base_classes import EmailMessage

def send_email(email_message:EmailMessage):
    try:
        send_mail(
            email_message.subject,
            email_message.message,
            settings.DEFAULT_FROM_EMAIL,
            [email_message.to_email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Failed to send email to {email_message.to_email}, error: {e}")