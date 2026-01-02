from django.core.mail import send_mail, EmailMessage as ReportMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from django.conf import settings
from django_rq import job
from accounts.models import User
from accounts.helpers.utils import create_password_reset_link
from emailing.helpers.base_classes import EmailMessage

def send_email(email_message:EmailMessage):
    """
    Sends an email using Django's send_mail function.
    params: email_message: An instance of EmailMessage containing email details.
    returns: None"""
    try:
        context: dict = {
            "title": email_message.title,
            "body": email_message.body,
            "cta_name": email_message.cta_name,
            "cta_url": email_message.cta_url,
            "extra_body": email_message.extra_body,
        }
        email_html_message: str = render_to_string(email_message.base_template, context)
        plain_message: str = strip_tags(email_html_message)

        send_mail(
            email_message.subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [email_message.to_email],
            fail_silently=False,
            html_message=email_html_message
        )
    except Exception as e:
        print(f"Failed to send email to {email_message.to_email}, error: {e}")

@job('default')
def send_welcome_email(to_email:str):
    """
    Sends a welcome email to a new user.
    params: to_email: The recipient's email address.
    returns: None
    """
    email_message: EmailMessage = EmailMessage(
        subject="Welcome to Our Service",
        to_email=to_email,
        title="InvoiceGo",
        body="Thank for registering in our service. We're excited to have you on board.",
        cta_name="Get Started",
        cta_url=f"{settings.BASE_URL}{reverse('login')}",
        extra_body="If you have any questions, feel free to reach out to our support team."
    )
    send_email(email_message)

@job('default')
def send_password_reset_email(to_email:str):
    """
    Sends a password reset email to a user.
    params: to_email: The recipient's email address.
    returns: None"""
    try:
        user: User = User.objects.get(email=to_email)
    except Exception as e:
        print(f"Failed to get user with email {to_email}")
    
    password_reset_link:str = create_password_reset_link(user)
    email_message: EmailMessage = EmailMessage(
        subject="Password Reset Request",
        to_email=to_email,
        title="Password Reset",
        body="We received a request to reset your password.",
        cta_name="Reset Password",
        cta_url=password_reset_link,
        extra_body="If you did not request a password reset, please ignore this email."
    )
    send_email(email_message)

@job('default')
def send_invoice_pdf(pdf):
    email_message: EmailMessage = EmailMessage(
        subject="Password Reset Request",
        to_email=settings.EMAIL_HOST_USER,
        title="Invoice",
        body="invoic shit",
        cta_name="check pdf",
        cta_url=settings.BASE_URL,
        extra_body="If you did not request a password reset, please ignore this email."
    )
    pass