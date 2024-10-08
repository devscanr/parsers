from extractors.web import html2text, markdown2text
from textwrap import dedent

def describe_html2text() -> None:
  def it_works() -> None:
    html = c("""
      <div>
        First 🧡
        <pre>
          <code>
            console.log('foo')
          </code>
        </pre>
        Second 💚
      </div>
    """)
    text = c("""
      First 🧡
      
      --
      
      Second 💚
    """)
    assert html2text(html) == dedent(text).strip()

def describe_markdown2text() -> None:
  def it_works() -> None:
    md = c("""
      First 🧡
      ```js
      console.log('foo')
      ```
      Second 💚
    """)
    text = c("""
      First 🧡
      
      --
      
      Second 💚
    """)
    assert markdown2text(md) == text

def c(text: str) -> str:
  return dedent(text).strip()
