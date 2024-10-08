from extractors.freelancer import is_freelancer as _is_freelancer
from extractors.utils import normalize

def is_freelancer(text: str) -> bool:
    return _is_freelancer(normalize(text))

def describe_is_freelancer() -> None:
  def it_basically_works() -> None:
    assert is_freelancer("I'm a freelancer")
    assert not is_freelancer("I'm a student")
