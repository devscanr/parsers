import spacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc, Token
from typing import Iterable

__all__ = ["are_nondevs", "is_nondev"]

nlp = spacy.load("en_core_web_md", exclude=["ner"])
matcher = PhraseMatcher(nlp.vocab)

NONDEV_NOUNS = {
  "artist", "dean", "founder", "manager", "mechanic", "musician", "cto", "technician", "vp",
  "physicist", # hr, recruiter
}

# --------------------------------------------------------------------------------------------------
# Currently follows the "Freelancer" scheme. Can be update to follow the "Student" scheme instead,
# where the preceding nouns have priotity over subsequent.
# --------------------------------------------------------------------------------------------------

def are_nondevs(ntexts: Iterable[str | Doc]) -> list[bool | None]:
  docs = nlp.pipe(ntexts)
  return [
    is_nondev(doc) for doc in docs
  ]

def is_nondev(ntext: str | Doc) -> bool | None:
  doc = ntext if type(ntext) is Doc else nlp(ntext)
  for token in doc:
    # if not token.is_space and not token.is_punct:
    # print(token, token.pos_, token.dep_, token.head.lemma_)
    if is_nondev_noun(token):
      return True
  return None

def is_nondev_noun(token: Token) -> bool:
  return (
    token.lower_ in NONDEV_NOUNS and
    token.pos_ in {"NOUN", "PROPN", "ADJ"} and # spacy default models have PROPN false positives and ADJ mistakes
    token.dep_ in {
      "ROOT",    # Manager
      "conj",    # Manager and student
      "attr",    # I am a manager
      "appos",   # Manager, student
      "compound" # Manager Nasim (Spacy mistakenly thinks the first word is PROPN)
    }
  )
