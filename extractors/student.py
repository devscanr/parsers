import re
import spacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Token
from extractors.match import words_to_regex

nlp = spacy.load("en_core_web_md", exclude=["ner"])
# nlp.add_pipe("merge_noun_chunks")
matcher = PhraseMatcher(nlp.vocab)

ROLE_NOUNS = {
  # intern -> does not mean a non-student
  # pilot -> non-digital
  "architect", "artist", "bachelor", "cto", "dean", "designer", "devops", "developer", "doctor",
  "engineer", "engineering", "eng", "entrepreneur",
  "founder", "generalist", "graduate", "guru", "lawyer", "lead", "leader", "magician", "mathematician",
  "mlops", "ninja", "phd", "physicist", "professor", "researcher", "scientist", "specialist", "vp",

  # A Master of Science abbreviated MS, M.S., MSc, M.Sc., SM, S.M., ScM or Sc.M. @_@
  # ^ need to retokenize
  # ^ need to compare as ORTH, not LOWER
}
STUDENT_NOUNS = {"sophomore", "student", "undergraduate"}
ASPIRING_SYNONIMS = {"aspiring", "future", "wannabe"}
ASPIRING_REGEX = words_to_regex(ASPIRING_SYNONIMS)
PERPETUAL_SYNONIMS = {"constant", "eternal", "everlasting", "life=long", "permanent", "perpetual"}
PERPETUAL_REGEX = words_to_regex({"constant", "eternal", "everlasting", "life=long", "permanent", "perpetual"})

def is_student(text: str) -> bool:
  ntext = normalize_text(text)
  doc = nlp(ntext)
  # for nc in doc.noun_chunks:
  #   print(nc)
  for token in doc:
    print(token, token.pos_, token.dep_)
    # Assuming whatever role is found first, is more important and deciding
    if is_student_noun_token(token):
      subtree = "".join([token.lower_ + token.whitespace_ for token in token.subtree])
      if re.search(PERPETUAL_REGEX, subtree) is not None:
        continue
      return True
    elif is_role_noun_token(token):
      subtree = "".join([token.lower_ + token.whitespace_ for token in token.subtree])
      if re.search(ASPIRING_REGEX, subtree) is not None:
        continue
      return False
  return False

def normalize_text(text: str) -> str:
  return re.sub(r"\s*\|\s*", ". ", text)

def is_student_noun_token(token: Token) -> bool:
  return (
    token.lower_ in STUDENT_NOUNS and
    token.pos_ in {"NOUN", "PROPN", "ADJ"} and # spacy default models have PROPN false positives and ADJ mistakes
    # (token.dep_ not in ["dobj", "pobj", "nsubj", "amod", "compound"]) # , "appos", "npadvmod"
    (token.dep_ in {
      "ROOT", # Student
      "conj", # Freelancer and student
      "attr",  # I am a student (need to check for "nsubj", ideally)
      "appos", # Freelancer, student
    })
  )

def is_role_noun_token(token: Token) -> bool:
  return (
    token.lower_ in ROLE_NOUNS and
    token.pos_ in {"NOUN", "PROPN", "ADJ"} and # spacy default models have numerous _PROPN_ false positives and ADJ mistakes
    # (token.dep_ not in ["dobj", "pobj", "nsubj", "amod", "compound"]) # , "appos", "npadvmod"
    (token.dep_ in {"ROOT", "conj", "attr", "appos"})
  )

# E.g.
# "Lawyer. Lecturer. Researcher. Student." -> only the last noun gets properly marked as "NOUN"
