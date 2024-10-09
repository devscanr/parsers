import spacy
from extractors.freelancer import FreelancerParser
from extractors.utils import fix_grammar, normalize

nlp = spacy.load("en_core_web_lg", exclude=["ner"])
freelancer_parser = FreelancerParser(nlp)

def are_freelancers(texts: list[str]) -> list[bool | None]:
  return freelancer_parser.are_freelancers([
    fix_grammar(normalize(text)) for text in texts
  ])

def is_freelancer(text: str) -> bool | None:
  return freelancer_parser.is_freelancer(
    fix_grammar(normalize(text))
  )

def describe_FreelancerParser() -> None:
  def describe_are_freelancers() -> None:
    def it_works() -> None:
      texts = [
        "I'm a freelancer",
        "I'm a developer",
      ]
      assert are_freelancers(texts) == [
        True,
        None,
      ]

  def describe_is_freelancer() -> None:
    def it_basically_works() -> None:
      assert is_freelancer("I'm a freelancer")
      assert is_freelancer("I was a free-lancer")
      assert is_freelancer("I used to be a free lancer")
      assert not is_freelancer("I'm a student")
      assert not is_freelancer("I'm a developer")

    def it_handles_set1() -> None:
      assert is_freelancer("""
        Freelancer Nasim is a Web Application Developer. 
        He knows JavaScript, Python, Django, NodeJS, Laravel, PhP. 
      """)
      assert not is_freelancer("""
        Opensource enthusiast, Skillbox teacher, Blogger 
      """)
      assert is_freelancer("""
        Free-lancer @ BYTESADMIN • Security Researcher 
      """)
      assert is_freelancer("Freelance Clojure programmer")
      assert is_freelancer("Freelance ⠁⣿⣿ ⣿⣿⣿ ⣿⣿⣿")

    def it_handles_set2() -> None:
      assert is_freelancer("indie dev • iOS & macOS • freelance")
      assert is_freelancer("Freelancer Jedi Padawan")
      assert is_freelancer("freelance math teacher, freelance front-end developer")
      assert not is_freelancer("I'm a Software Engineer, Ethical Hacker, and Cyber security enthusiast")
      assert not is_freelancer("⭐️ Senior Software Developer ⭐️ Blockchain / Backend / Frontend / ETL / RPA")

    def it_handles_set3() -> None:
      assert is_freelancer("Freelancer and video editor")
      assert is_freelancer("Full stack developer, tech consultant, guitarist, windsurfer.")
      assert is_freelancer("Backend SWE & consulting")
      assert is_freelancer("Java Full-stack Developer at j-labs.pl Crif consultant")
      assert is_freelancer("Front-end & WordPress developer, UX consultant. Making stuff for the web since 2005")

  def it_handles_set4() -> None:
      assert is_freelancer("Frontend Consultant; Web, Mobile and Desktop Applications Developer; Team Lead; Mentor;")
      assert is_freelancer("My name is Jorens, I'm a Full Stack developer, currently freelancing (but looking for a real job).")
      assert is_freelancer("WebGL, WebXR, full-stack, consulting")
      assert is_freelancer("Full-stack junior software developer, system administrator and IT consultant.")
      assert is_freelancer("As a backend developer mastering Java, I have transformed years of freelancing into a full-time career.")

  def it_handles_set5() -> None:
      assert is_freelancer("NET Developer with front-end skills, Freelancer, Photographer and Science Lover")
      assert not is_freelancer("Arman is a full-stack developer who mainly focuses on web development")
      assert is_freelancer("Teenager, freelancer, backend developer (TypeScript, C++17)")
      assert is_freelancer("Oleg Rybnikov - a freelancing web artisan specializing in Vite/Vue3")
      assert is_freelancer("#backend #java #freelancer")
      assert not is_freelancer("applied artificial intelligence student")
      assert is_freelancer("Hi, I am 22 years old freelance full-stack developer from Czech Republic.")
      assert is_freelancer("🇸🇰 Freelancer full-stack developer. #React #ReactNative")
      assert is_freelancer("Full stack software engineer at dextra | Freelancer")
      # is_freelancer("Self-taught Developer graded in Back-end Development. -Freelancer") -- character "-"
