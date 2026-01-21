from dataclasses import dataclass, field
from typing import Any, Optional

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

@dataclass
class EmailPayload:
    subject: str
    to: list[str] = field(default_factory=list)
    from_email: Optional[str] = None
    template_name: Optional[str] = None
    body: str = ""
    context: dict[str, Any] = field(default_factory=dict)
    attachments: list[tuple[str, bytes, str]] = field(default_factory=list)
    origin: Optional[str] = None

