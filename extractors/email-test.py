from extractors.email import parse_emails
from extractors.utils import normalize

def parse(text: str) -> list[str]:
  return parse_emails(normalize(text))

# Emails and phone numbers are fake (generated). Potential clashes will existing contacts
# of real people are coincidental and not intended.

def describe_parse_emails():
  def it_parses_set1():
    assert parse("email: bishal-hadka-1600@gg.com phone: 970-799-9291") == ["bishal-hadka-1600@gg.com"]
    assert parse("akashkash934@hotmail.ru") == ["akashkash934@hotmail.ru"]
    assert parse("Email, Phone, other contacts") == []
    assert parse("Email: justin.rick@gmail.com Phone: 9046571689") == ["justin.rick@gmail.com"]
    assert parse("huyhain926guyen@gmail.com salmanzuck@zoho.com") == ["huyhain926guyen@gmail.com", "salmanzuck@zoho.com"]
  # Few test because it's already tested
