from extractors.category import Categorizer, Categorized
from extractors.utils import fix_grammar, normalize

categorizer = Categorizer()

def categorize(texts: list[str]) -> list[Categorized]:
  return categorizer.categorize(texts)

def t(text: str) -> str:
  return fix_grammar(normalize(text))

def describe_Categorizer() -> None:
  def describe_categorize() -> None:
    def it_works() -> None:
      texts = [
        t("I'm a student and a freelancer"),
        t("I'm an engineer, a student, occasionally a musician"),
      ]
      assert categorize(texts) == [
        Categorized(is_freelancer=True, is_nondev=False, is_student=True),
        Categorized(is_freelancer=False, is_nondev=True, is_student=False),
      ]
