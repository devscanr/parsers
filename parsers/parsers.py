import re

PHONE_PREFIX_REGEX = r"(?:phone|mobile|tel)(?:\s*-?\s*(?:num\.?|number))?\s*[:=-]{0,2}\s*"
PHONE_NUMBER_REGEX = r"([(+]{0,2}\d[-\d(). ]+\d)"

# https://github.com/fabian-hiller/valibot
EMAIL_REGEX = r"[\w+-]+(?:\.[\w+-]+)*@[\da-z]+(?:[.-][\da-z]+)*\.[a-z]{2,}"
# Note: underscores are not universally allowed in emails

def clean_text(text: str) -> str:
    return text.replace("：", ": ").strip()

def parse_phones(text: str) -> list[str]:
    text = clean_text(text)
    phones = re.findall(PHONE_PREFIX_REGEX + PHONE_NUMBER_REGEX, text, re.IGNORECASE)
    return [re.sub(r"[- .()]", "", phone) for phone in phones]

def parse_emails(text: str) -> list[str]:
    text = clean_text(text)
    emails = re.findall(EMAIL_REGEX, text, re.IGNORECASE)
    return emails
