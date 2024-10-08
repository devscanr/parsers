import re
from emoji import replace_emoji
from typing import Any, Generator, cast, Iterable

__all__ = ["normalize", "uniq"]

def normalize(text: str) -> str:
  text = text.replace("：", ": ")
  text = re.sub(r"\s*\|+\s*", ". ", text)
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
