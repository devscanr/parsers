import re
from typing import Any, Generator, cast, Iterable

# TODO list __all__

PHONE_TRIGGER_REGEXES = [
  r"(?:phone|mobile|tel)(?:\s*-?\s*(?:num\.?|numbers?))?\s*[:=-]{0,2}\s*",
  r"(?:to\s+reach\s+me)\s*[:=-]{0,2}\s*",
  r"(?:whatsapp|viber|telegram|tg|signal)\s*[:=-]{0,2}\s*",
]
PHONE_NUMBER_REGEX = r"([(+]{0,2}\s*\d[-\d().\s]+\d)"
PHONE_CONTEXTUALIZED_REGEXES = [
  (PHONE_TRIGGER_REGEX + PHONE_NUMBER_REGEX) for PHONE_TRIGGER_REGEX in PHONE_TRIGGER_REGEXES
]

PHONE_INTERNATIONAL_REGEX = r"(\+\d{1,3}[-\s]\d{1,5}[-\s][-\d\s]{4,}\d)"

PHONE_URL_REGEX = "|".join([
  r"(?<!\w)(?:wa.me|t.me)/(\+?\d{7,14})",
])
# TODO viber://contact?number=%2B0000000000000

# https://github.com/fabian-hiller/valibot
EMAIL_REGEX = r"[\w+-]+(?:\.[\w+-]+)*@[\da-z]+(?:[.-][\da-z]+)*\.[a-z]{2,}"

# Note: underscores are not universally allowed in emails

# Order preserving uniq
def uniq[T](arr: list[T] | Generator[str, Any, Any]) -> list[T]:
  # Note: does not collapse "+NNN" with "NNN" so far
  d = {}
  for x in arr:
    d[x] = 1
  keys = cast(Iterable[T], d.keys()) # Looks like MyPy (or something) is improperly typing this
  return list(keys)

def normalize_text(text: str) -> str:
  text = text.replace("：", ": ").strip()
  return (
    re.sub(r"(📞|☎️|📱|☎)\s*:?\s*", "Phone: ", text, re.UNICODE)
  )

def parse_phones(text: str) -> list[str]:
  text = normalize_text(text)
  phones1 = [
    phone
    for REGEX in PHONE_CONTEXTUALIZED_REGEXES
    for phone in re.findall(REGEX, text, re.IGNORECASE)
  ]
  print(phones1)
  phones2 = re.findall(PHONE_INTERNATIONAL_REGEX, text)
  phones3 = re.findall(PHONE_URL_REGEX, text)
  phones = phones1 + phones2 + [ensure_plus_prefixed(p) for p in phones3]
  clean_phones = (
    re.sub(r"[-\s.()]", "", phone) for phone in phones
  )
  return uniq(
    phone for phone in clean_phones
    if 4 <= len(phone.strip("+")) <= 17
  )

def parse_emails(text: str) -> list[str]:
  # Notes:
  # - https://stackoverflow.com/questions/1423195/what-is-the-actual-minimum-length-of-an-email-address-as-defined-by-the-ietf
  # - https://stackoverflow.com/questions/386294/what-is-the-maximum-length-of-a-valid-email-address
  text = normalize_text(text)
  emails = re.findall(EMAIL_REGEX, text, re.IGNORECASE)
  return [
    email for email in emails
    if 6 <= len(email) <= 254
  ]

def ensure_plus_prefixed(phone: str) -> str:
  return phone if phone.startswith("+") else ("+" + phone)
