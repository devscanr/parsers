import spacy
from extractors.nondev import NondevParser
from extractors.utils import fix_grammar, normalize

nlp = spacy.load("en_core_web_lg", exclude=["ner"])
nondev_parser = NondevParser(nlp)

def are_nondevs(texts: list[str]) -> list[bool | None]:
  return nondev_parser.are_nondevs([
    fix_grammar(normalize(text)) for text in texts
  ])

def is_nondev(text: str) -> bool | None:
  return nondev_parser.is_nondev(
    fix_grammar(normalize(text))
  )

def describe_NondevParser() -> None:
  def describe_are_nondevs() -> None:
    def it_works() -> None:
      texts = [
        "I'm a manager",
        "I'm a developer",
      ]
      assert are_nondevs(texts) == [
        True,
        None,
      ]

  def describe_is_nondev() -> None:
    def it_basically_works() -> None:
      assert is_nondev("I'm a manager")
      assert is_nondev("I used to be an artist like you")
      assert not is_nondev("I'm a student")
      assert not is_nondev("I'm a developer")
      assert is_nondev("I'm a manager and an engineer")
