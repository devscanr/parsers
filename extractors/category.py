from dataclasses import dataclass
from extractors import is_freelancer, is_student
import spacy
from spacy.tokens import Doc
from typing import Iterable

__all__ = ["categorize", "Categorized"]

from extractors.nondev import is_nondev

nlp = spacy.load("en_core_web_md", exclude=["ner"])

@dataclass
class Categorized:
  is_freelancer: bool
  is_nondev: bool
  is_student: bool

def categorize(ntexts: Iterable[str | Doc]) -> list[Categorized]:
  docs = nlp.pipe(ntexts)
  return [
    Categorized(
      is_freelancer=is_freelancer(doc),
      is_nondev=is_nondev(doc),
      is_student=is_student(doc),
    ) for doc in docs
  ]

