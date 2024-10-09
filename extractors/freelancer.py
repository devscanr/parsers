from spacy.language import Language
# from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc, Token
from typing import Iterable

__all__ = ["FreelancerParser"]

FREELANCER_NOUNS = {"consulting", "consultant", "freelancer", "freelance", "freelancing"}
FREELANCER_VERBS = {"consulting", "freelancing"}

class FreelancerParser:
  def __init__(self, nlp: Language) -> None:
    self.nlp = nlp

  def are_freelancers(self, ntexts: Iterable[str | Doc]) -> list[bool | None]:
    docs = self.nlp.pipe(ntexts)
    return [
      self.is_freelancer(doc) for doc in docs
    ]

  def is_freelancer(self, ntext: str | Doc) -> bool | None:
    doc = ntext if type(ntext) is Doc else self.nlp(ntext)
    # for nc in doc.noun_chunks:
    #   print(nc)
    for token in doc:
      # if not token.is_space and not token.is_punct:
      #   print(token, token.pos_, token.dep_)
      if is_freelancer_noun(token):
        return True
      elif is_freelancer_verb(token):
        return True
    return None

def is_freelancer_noun(token: Token) -> bool:
  if token.lower_ not in FREELANCER_NOUNS:
    return False
  return (
    token.pos_ in {"NOUN", "PROPN", "ADJ"} # and # spacy default models have PROPN false positives and ADJ mistakes
    # token.dep_ in {
    #   "ROOT",     # Student
    #   "conj",     # Freelancer and student
    #   "amod",     # freelance math teacher
    #   "attr",     # I am a student
    #   "appos",    # Freelancer, student
    #   "compound", # Freelancer Nasim (Spacy mistakenly thinks the first word is PROPN)
    #   "nmod",     # Freelancer and editor
    #   "pobj",     # Appears in complex (ill-understood) sentences
    # }
  )

def is_freelancer_verb(token: Token) -> bool:
  if token.lower_ not in FREELANCER_VERBS:
    return False
  # Special case if it's the first word (a relatively often case)
  if not token.i:
    return True
  # ...
  if token.pos_ == "VERB":
    return True
    # if token.dep_ == "ROOT":
    #   return True
    # elif token.dep_ == "acl":
    #   return True
  return False
