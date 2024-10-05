from emoji import replace_emoji
from html2text import HTML2Text
from markdown import markdown
import re

h = HTML2Text()
h.mark_code = True

def html2text(html: str) -> str:
  text = h.handle(html).strip()
  clean_text = replace_emoji(text, "!")
  return re.sub(
    r"\[code].*\[/code]",
    "--",
    clean_text,
    flags=re.DOTALL  # | re.UNICODE | re.IGNORECASE | re.MULTILINE
  )

def markdown2text(md: str) -> str:
  html = markdown(md, extensions=["fenced_code"])
  return html2text(html)
