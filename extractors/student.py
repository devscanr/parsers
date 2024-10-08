from extractors.match import words_to_regex
import re
import spacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc, Token
from typing import Iterable

__all__ = ["are_students", "is_student"]

nlp = spacy.load("en_core_web_md", exclude=["ner"])
matcher = PhraseMatcher(nlp.vocab)

STUDENT_NOUNS = {
  "freshman",  # first-course
  "graduate",  # has a degree but often used as a shortening for "graduate student" which is someone who continues to learn
  "sophomore", # second-course
  "student",   # junior student (3rd), senior student (4th year), no universal term for 5th year
  "undergraduate",
}
NON_STUDENT_NOUNS = {
  # Non-included cases:
  #   intern -- does not mean a non-student
  #   pilot -- non-digital
  # Conflicts:
  #   MS - Mississippi State
  #   BC - British Columbia Province
  "B.S", "M.S", "Ph.D",
  "analyst", "architect", "artist", "bachelor", "cto", "dean", "designer", "devops", "developer", "doctor",
  "engineer", "engineering", "eng", "entrepreneur",
  "founder", "generalist", "guru", "lawyer", "lead", "leader", "magician", "mathematician", "mechanic",
  "mlops", "musician", "ninja", "physicist", "professor", "researcher", "scientist", "specialist", "vp",
   # hr, recruiter
}
ASPIRING_SYNONIMS = {"aspiring", "future", "wannabe"}
ASPIRING_REGEX = words_to_regex(ASPIRING_SYNONIMS)
PERPETUAL_SYNONIMS = {"constant", "eternal", "everlasting", "life=long", "permanent", "perpetual"}
PERPETUAL_REGEX = words_to_regex(PERPETUAL_SYNONIMS)

def are_students(ntexts: Iterable[str | Doc]) -> list[bool]:
  docs = nlp.pipe(ntexts)
  return [
    is_student(doc) for doc in docs
  ]

def is_student(ntext: str | Doc) -> bool:
  doc = ntext if type(ntext) is Doc else nlp(ntext)
  # for nc in doc.noun_chunks:
  #   print(nc)
  for token in doc:
    # print(token, token.pos_, token.dep_)
    # Assuming whatever role is found first, is more important and deciding
    if is_student_noun(token):
      subtree = "".join([token.lower_ + token.whitespace_ for token in token.subtree])
      if re.search(PERPETUAL_REGEX, subtree) is not None:
        continue
      return True
    elif is_non_student_noun(token):
      subtree = "".join([token.lower_ + token.whitespace_ for token in token.subtree])
      if re.search(ASPIRING_REGEX, subtree) is not None:
        continue
      return False
  return False

def is_student_noun(token: Token) -> bool:
  return (
    token.lower_ in STUDENT_NOUNS and
    token.pos_ in {"NOUN", "PROPN", "ADJ"} and # spacy default models have PROPN false positives and ADJ mistakes
    # (token.dep_ not in ["dobj", "pobj", "nsubj", "amod", "compound"]) # , "appos", "npadvmod"
    (token.dep_ in {
      "ROOT",     # Student
      "conj",     # Freelancer and student
      "attr",     # I am a student
      "appos",    # Freelancer, student
      "compound", # Undergraduate engineer
      "nmod"      # Appears in complex, badly formatted sentences
    })
  )

def is_non_student_noun(token: Token) -> bool:
  return (
    token.lower_ in NON_STUDENT_NOUNS and
    token.pos_ in {"NOUN", "PROPN", "ADJ"} and # spacy default models have numerous _PROPN_ false positives and ADJ mistakes
    (token.dep_ in {
      "ROOT", "conj", "attr", "appos"
    })
  )

# E.g.
# "Lawyer. Lecturer. Researcher. Student." -> only the last noun gets properly marked as "NOUN"

# UNIVERSITIES. Currently thinking we can't generalize to students – could be teachers or scientists.
# assert is_student("Itmo")
# assert is_student("Dstu")
# assert is_student("Itmo university")
# assert is_student("Financial University under the government of Russia")
# assert is_student("Yandex.Fintech | ITMO SWE '25")

# GRADUATE
# assert not is_student("CMC MSU bachelor's degree, FCS HSE master student, ex-Data Scientist at Tinkoff bank.")

# TYPOS
# assert is_student("A 2nd year studxnt of the Higher IT School.")

# INTERNSHIP
# assert is_student("Currently looking for an ML internship. I love interesting and non-typical projects.")

# STUDY
# assert is_student("I'm studying data analytics and here are my first projects")
# assert is_student("Hello. I'am Vadim Tikhonov. I study code, data analysis and data science.")
# assert is_student("I am new to ML & DL")
