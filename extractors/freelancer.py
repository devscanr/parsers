import spacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc, Token
from typing import Iterable

__all__ = ["are_freelancers", "is_freelancer"]

nlp = spacy.load("en_core_web_md", exclude=["ner"])
matcher = PhraseMatcher(nlp.vocab)

FREELANCER_NOUNS = {"freelancer", "freelance"}

def are_freelancers(ntexts: Iterable[str | Doc]) -> list[bool | None]:
  docs = nlp.pipe(ntexts)
  return [
    is_freelancer(doc) for doc in docs
  ]

def is_freelancer(ntext: str | Doc) -> bool | None:
  doc = ntext if type(ntext) is Doc else nlp(ntext)
  # for nc in doc.noun_chunks:
  #   print(nc)
  for token in doc:
    # if not token.is_space and not token.is_punct:
    # print(token, token.pos_, token.dep_)
    if is_freelancer_noun(token):
      return True
  return None

def is_freelancer_noun(token: Token) -> bool:
  if token.lower_ not in FREELANCER_NOUNS:
    return False
  return (
    token.pos_ in {"NOUN", "PROPN", "ADJ"} and # spacy default models have PROPN false positives and ADJ mistakes
    token.dep_ in {
      "ROOT",    # Student
      "conj",    # Freelancer and student
      "attr",    # I am a student
      "appos",   # Freelancer, student
      "compound" # Freelancer Nasim (Spacy mistakenly thinks the first word is PROPN)
    }
  )
