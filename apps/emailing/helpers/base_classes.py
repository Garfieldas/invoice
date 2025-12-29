from dataclasses import dataclass

@dataclass
class EmailMessage:
    subject: str
    to_email:str
    title: str
    body: str
    cta_name: str
    cta_url: str
    extra_body: str
    base_template: str = "emailing/base_email.html"
