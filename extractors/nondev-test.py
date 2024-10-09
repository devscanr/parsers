from extractors.nondev import are_nondevs, is_nondev as _is_nondev
from extractors.utils import fix_grammar, normalize

def is_nondev(text: str) -> bool | None:
  return _is_nondev(
    fix_grammar(normalize(text))
  )

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

# def describe_is_nondev():
#   def it_basically_works():
#     assert is_nondev("I'm a manager")
#     assert is_nondev("I used to be an artist")
#     assert not is_nondev("I'm a student")
#     assert not is_nondev("I'm a developer")
#     assert is_nondev("I'm a manager and an engineer")


