from django.dispatch import receiver
from django.db.models.signals import post_save
from accounts.models import User
from emailing.helpers.base_classes import EmailMessage
from emailing.helpers.gmail import send_welcome_email

@receiver(post_save, sender=User)
def recalculate_invoice_total_price(sender, instance:User, created, **kwargs)->None:
    """
    Signal to send a welcome email to a newly registered user.
    params:
        sender: The model class.
        instance: The actual instance being saved.
        created: A boolean; True if a new record was created.
        **kwargs: Additional keyword arguments.
    returns: None
    """
    try:
        if created:
            to_email: str = instance.email
            send_welcome_email(to_email)
        else:
            return None
    except Exception as e:
        print(f"Failed to send email to user {instance.pk}, error {e}")