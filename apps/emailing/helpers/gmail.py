from typing import Optional
from django.core.mail import send_mail, EmailMessage as ReportMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from django.conf import settings
from django_rq import job
from accounts.models import User
from accounts.helpers.utils import create_password_reset_link
from invoice.models import Invoice
from emailing.helpers.base_classes import EmailMessage, EmailPayload

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
def send_invoice_pdf(invoice_pk:str, to_email:str)->None:
    """
    Sends an invoice PDF as an email attachment.
    params: invoice_pk: The primary key of the invoice to be sent.
            to_email: The recipient's email address.
    returns: None"""
    try:
        from invoice.helpers.pdf import generate_invoice_pdf
        pdf:Optional[bytes] = generate_invoice_pdf(invoice_pk)
        invoice:Invoice = Invoice.objects.get(pk=invoice_pk)
    except Exception as e:
        print(f"Failed to send invoice PDF to {to_email}, error: {e}")
    
    email_message: EmailMessage = EmailMessage(
        subject="Your Invoice from InvoiceGo",
        to_email=to_email,
        title="Invoice Attached",
        body="Please find attached your invoice.",
        cta_name="View Invoices",
        cta_url=f"{settings.BASE_URL}{reverse('invoices')}",
        extra_body="Thank you for using our service."
    )
    context: dict = {
        "title": email_message.title,
        "body": email_message.body,
        "cta_name": email_message.cta_name,
        "cta_url": email_message.cta_url,
        "extra_body": email_message.extra_body,
    }
    email_html_message: str = render_to_string(email_message.base_template, context)
    msg = ReportMessage(
        subject=email_message.subject,
        body=email_html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email_message.to_email],
    )
    msg.content_subtype = "html"
    msg.attach(f"invoice_{invoice.invoice_number_display}.pdf", pdf, "application/pdf")
    try:
        msg.send(fail_silently=False)
    except Exception as e:
        print(f"Failed to send invoice PDF to {to_email}, error: {e}")

def send_password_reset_email2(request, email: str):
    """
    Sends a password reset email to the given email address.
    """
    try:
        user: User = User.objects.get(email=email)
        uid: str = (user.pk)
        token: str = (user.pk)
        reset_link: str = request.build_absolute_uri(
            reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})
        )
        payload = EmailPayload(
        subject="Inreal.lt - Slaptažodžio atstatymas",
        to=[user.email],
        template_name="components/email/password_reset_email.html",
        context={"user": user, "reset_link": reset_link},
        )
        send_email2(payload)

    except Exception as ex:
        raise Exception(f"Error sending password reset email: {ex}")
    
def send_email2(payload: EmailPayload) -> int:
    signers_list: list[str] = [signer for signer in payload.to if signer]
    if not signers_list:
        raise ValueError("No recipients provided")

    sender = payload.from_email or getattr(settings, "SEND_FROM_EMAIL", None) or settings.DEFAULT_FROM_EMAIL

    html = ""
    text = payload.body

    if payload.template_name:
        html = render_to_string(payload.template_name, payload.context)
        if not text:
            text = strip_tags(html)

    msg = EmailMultiAlternatives(
        subject=payload.subject,
        body=text or "",
        from_email=sender,
        to=signers_list,
    )

    if html:
        msg.attach_alternative(html, "text/html")

    for filename, content, mimetype in payload.attachments:
        msg.attach(filename, content, mimetype)

    return msg.send(fail_silently=False)