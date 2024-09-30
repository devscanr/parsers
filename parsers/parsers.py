import re
from typing import Any, Generator

PHONE_PREFIX_REGEX = r"(?:phone|mobile|tel)(?:\s*-?\s*(?:num\.?|number))?\s*[:=-]{0,2}\s*"
PHONE_NUMBER_REGEX = r"([(+]{0,2}\d[-\d(). ]+\d)"
PHONE_PREFIXED_REGEX = PHONE_PREFIX_REGEX + PHONE_NUMBER_REGEX

PHONE_INTERNATIONAL_REGEX = r"(\+\d{1,3}[- ]\d{1,5}[- ][-\d ]{4,}\d)"

PHONE_URL_REGEX = "|".join([
    r"(?<!\w)(?:wa.me|t.me)/(\+?\d{7,14})",
])

# https://github.com/fabian-hiller/valibot
EMAIL_REGEX = r"[\w+-]+(?:\.[\w+-]+)*@[\da-z]+(?:[.-][\da-z]+)*\.[a-z]{2,}"
# Note: underscores are not universally allowed in emails

# Order preserving uniq
def uniq[T](arr: list[T] | Generator[str, Any, Any]) -> list[T]: # type: ignore
    # Note: does not collapse "+NNN" with "NNN" so far
    d = {}
    for x in arr:
        d[x] = 1
    return list(d.keys())

def clean_text(text: str) -> str:
    text = text.replace("：", ": ").strip()
    return (
        re.sub(r"(📞|☎️|📱|☎)\s*:?\s*", "Phone: ", text, re.UNICODE)
    )

def parse_phones(text: str) -> list[str]:
    text = clean_text(text)
    phones1 = re.findall(PHONE_PREFIXED_REGEX, text, re.IGNORECASE)
    phones2 = re.findall(PHONE_INTERNATIONAL_REGEX, text)
    phones3 = re.findall(PHONE_URL_REGEX, text)
    phones = phones1 + phones2 + [ensure_plus_prefixed(p) for p in phones3]
    clean_phones = (re.sub(r"[- .()]", "", phone) for phone in phones)
    return uniq(
        phone for phone in clean_phones
        if 4 <= len(phone.strip("+")) <= 17
    )

def parse_emails(text: str) -> list[str]:
    # Notes:
    # - https://stackoverflow.com/questions/1423195/what-is-the-actual-minimum-length-of-an-email-address-as-defined-by-the-ietf
    # - https://stackoverflow.com/questions/386294/what-is-the-maximum-length-of-a-valid-email-address
    text = clean_text(text)
    emails = re.findall(EMAIL_REGEX, text, re.IGNORECASE)
    return [
        email for email in emails
        if 6 <= len(email) <= 254
    ]

def ensure_plus_prefixed(phone: str) -> str:
    return phone if phone.startswith("+") else ("+" + phone)
