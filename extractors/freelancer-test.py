from extractors.freelancer import are_freelancers, is_freelancer as _is_freelancer
from extractors.utils import fix_grammar, normalize

def is_freelancer(text: str) -> bool:
  return _is_freelancer(
    fix_grammar(normalize(text))
  )

def describe_are_freelancers() -> None:
  def it_basically_works() -> None:
    texts = [
      "I'm a freelancer",
      "I'm a developer",
    ]
    assert are_freelancers(texts) == [
      True,
      False,
    ]

def describe_is_freelancer() -> None:
  def it_basically_works() -> None:
    assert is_freelancer("I'm a freelancer")
    assert is_freelancer("I was a free-lancer")
    assert is_freelancer("I used to be a free lancer like you")
    assert not is_freelancer("I'm a student")
    assert not is_freelancer("I'm a developer")

  def it_handles_set1() -> None:
    assert is_freelancer("""
      Freelancer Nasim is a Web Application Developer. 
      He knows JavaScript, Python, Django, NodeJS, Laravel, PhP. 
    """)
    assert not is_freelancer("""
      Opensource enthusiast, Skillbox teacher, Blogger 
    """)
    assert is_freelancer("""
      Free-lancer @ BYTESADMIN • Security Researcher 
    """)
    assert is_freelancer("Freelance Clojure programmer")
    assert is_freelancer("Freelance ⠁⣿⣿ ⣿⣿⣿ ⣿⣿⣿")

  def it_handles_set2() -> None:
    assert is_freelancer("indie dev • iOS & macOS • freelance")
    assert is_freelancer("Freelancer Jedi Padawan")
    assert is_freelancer("freelance math teacher, freelance front-end developer")
    assert not is_freelancer("I'm a Software Engineer, Ethical Hacker, and Cyber security enthusiast")
    assert not is_freelancer("⭐️ Senior Software Developer ⭐️ Blockchain / Backend / Frontend / ETL / RPA")


