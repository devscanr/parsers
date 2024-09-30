import re

PHONE_PREFIX_REGEX = r"(?:phone|mobile|tel)(?:\s*-?\s*(?:num\.?|number))?\s*[:=-]{0,2}\s*"
PHONE_NUMBER_REGEX = r"([(+]{0,2}\d[-\d(). ]+\d)"
PHONE_NUMBER_INTERNATIONAL_REGEX = r"(\+\d{1,3}[- ]\d{1,5}[- ][-\d ]{4,}\d)"
                                   # COUNTRY-CODE AREA-CODE NUMBER

# https://github.com/fabian-hiller/valibot
EMAIL_REGEX = r"[\w+-]+(?:\.[\w+-]+)*@[\da-z]+(?:[.-][\da-z]+)*\.[a-z]{2,}"
# Note: underscores are not universally allowed in emails

# Order preserving uniq
def uniq[T](arr: list[T]) -> list[T]: # type: ignore
    d = {}
    for x in arr:
        d[x] = 1
    return list(d.keys())

def clean_text(text: str) -> str:
    return (
        re.sub(r"(?:📞|☎️|📱|☎)\s*:?\s*", "Phone: ", text, re.UNICODE)
            .replace("：", ": ")
            .strip()
    )

def parse_phones(text: str) -> list[str]:
    text = clean_text(text)
    phones1 = re.findall(PHONE_PREFIX_REGEX + PHONE_NUMBER_REGEX, text, re.IGNORECASE)
    phones2 = re.findall(PHONE_NUMBER_INTERNATIONAL_REGEX, text)
    phones = uniq(phones1 + phones2)
    clean_phones = set(re.sub(r"[- .()]", "", phone) for phone in phones)
    return [
        phone for phone in clean_phones
        if 4 <= len(phone.strip("+")) <= 17
    ]

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

