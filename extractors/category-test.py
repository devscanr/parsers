from extractors.category import categorize, Categorized
from extractors.utils import fix_grammar, normalize

def t(text: str) -> str:
  return fix_grammar(normalize(text))

def describe_categorize():
  def it_works():
    texts = [
      t("I'm a student and a freelancer"),
      t("I'm an engineer, a student, occasionally a musician"),
    ]
    assert categorize(texts) == [
      Categorized(is_freelancer=True, is_nondev=False, is_student=True),
      Categorized(is_freelancer=False, is_nondev=True, is_student=False),
    ]

