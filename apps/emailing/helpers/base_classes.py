from dataclasses import dataclass

@dataclass
class EmailMessage:
    subject: str
    message: str
    to_email:str
