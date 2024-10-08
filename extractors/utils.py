import re
from emoji import replace_emoji
from typing import Any, Generator, cast, Iterable

__all__ = ["normalize", "uniq", "fix_grammar"]

def normalize(text: str) -> str:
  text = text.replace("：", ": ")
  text = re.sub(r"\s*[•|]+\s*", ". ", text)
  text = re.sub(r"(📞|☎️|📱|☎)\s*:?\s*", "Phone: ", text, re.UNICODE)
  text = replace_emoji(text, "!")
  return text.strip()

def uniq[T](arr: list[T] | Generator[str, Any, Any]) -> list[T]:
  # Note: does not collapse "+NNN" with "NNN" so far
  d = {}
  for x in arr:
    d[x] = 1
  keys = cast(Iterable[T], d.keys()) # Looks like MyPy (or something) is improperly typing this
  return list(keys)

# --------------------------------------------------------------------------------------------------
# Invalid grammar, especially punctuation, ruins Spacy analysis. I've found that
# it's much easier to fix common errors preventively, than to fight them post-factum.
# --------------------------------------------------------------------------------------------------

GRAMMAR_FIXES: list[tuple[str, str, re.RegexFlag | int]] = [
  (r"under[-\s]+graduated?", r"undergraduate", re.IGNORECASE),
  (r"free[-\s]+lance(r)?", r"freelance\1", re.IGNORECASE),
  (r"B\.?[sS]\.?[cC]?\.?|S[cC]?\.?[bB]\.?", r"B.S", 0), # B.S  = Bachelor of Science
  (r"M\.?[sS]\.?[cC]?\.?|S[cC]\.?[mM]\.?", r"M.S", 0),  # M.S  = Master of Science (not handling "SM" forms for now)
  (r"P\.?[hH]\.?[dD]?\.?", r"Ph.D", 0),                 # Ph.D = Doctor of Philosophy
  # ...
  # TODO devops, mlops, sec-ops (insane number of varieties here)
]
GRAMMAR_FIXES = [
  (r"(?<!\w)" + pattern + r"(?!\w)", replacement, flags)
  for (pattern, replacement, flags) in GRAMMAR_FIXES
]

def fix_grammar(text: str) -> str:
  for pattern, replacement, flags in GRAMMAR_FIXES:
    text = re.sub(pattern, replacement, text, 0, flags)
  return text
