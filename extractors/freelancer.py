import spacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc, Token
from typing import Iterable

__all__ = ["are_freelancers", "is_freelancer"]

nlp = spacy.load("en_core_web_md", exclude=["ner"])
matcher = PhraseMatcher(nlp.vocab)

FREELANCER_NOUNS = {"freelancer", "freelance"}

def are_freelancers(ntexts: Iterable[str | Doc]) -> list[bool]:
  docs = nlp.pipe(ntexts)
  return [
    is_freelancer(doc) for doc in docs
  ]

def is_freelancer(ntext: str | Doc) -> bool:
  doc = ntext if type(ntext) is Doc else nlp(ntext)
  # for nc in doc.noun_chunks:
  #   print(nc)
  for token in doc:
    # print(token, token.pos_, token.dep_)
    # Assuming whatever role is found first, is more important and deciding
    if is_freelancer_noun(token):
      return True
  return False

def is_freelancer_noun(token: Token) -> bool:
  return (
    token.lower_ in FREELANCER_NOUNS and
    token.pos_ in {"NOUN", "PROPN", "ADJ"} and # spacy default models have PROPN false positives and ADJ mistakes
    # (token.dep_ not in ["dobj", "pobj", "nsubj", "amod", "compound"]) # , "appos", "npadvmod"
    (token.dep_ in {
      "ROOT",    # Student
      "conj",    # Freelancer and student
      "attr",    # I am a student (need to check for "nsubj", ideally)
      "appos",   # Freelancer, student
      "compound" # Freelancer Nasim (Spacy mistakenly thinks the first word is PROPN)
    })
  )
