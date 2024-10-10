from dataclasses import dataclass
from extractors.freelancer import FreelancerParser
from extractors.nondev import NondevParser
from extractors.student import StudentParser
import spacy
# from spacy.language import Language
from spacy.tokens import Doc
from typing import Iterable

__all__ = ["Categorized", "Categorizer"]

@dataclass
class Categorized:
  is_freelancer: bool
  is_nondev: bool
  is_student: bool

class Categorizer:
  def __init__(self) -> None:
    self.nlp = spacy.load("en_core_web_lg", exclude=["lemmatizer", "ner"])
    self.freelancer_parser = FreelancerParser(self.nlp)
    self.nondev_parser = NondevParser(self.nlp)
    self.student_parser = StudentParser(self.nlp)

  def categorize(self, ntexts: Iterable[str | Doc]) -> list[Categorized]:
    docs = self.nlp.pipe(ntexts)
    return [
      Categorized(
        is_freelancer = self.freelancer_parser.is_freelancer(doc) or False,
        is_nondev = self.nondev_parser.is_nondev(doc) or False,
        is_student = self.student_parser.is_student(doc) or False,
      ) for doc in docs
    ]
