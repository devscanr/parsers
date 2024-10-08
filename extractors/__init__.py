from .phone import parse_phones
from .email import parse_emails
from .freelancer import is_freelancer
from .student import is_student
from .web import html2text, markdown2text

__all__ = [
  # Parsers
  "parse_phones",
  "parse_emails",

  # Predicates
  "is_freelancer",
  "is_student",

  # Web Utils
  "html2text",
  "markdown2text"
]
