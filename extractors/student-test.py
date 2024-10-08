from extractors.student import are_students, is_student as _is_student
from extractors.utils import fix_grammar, normalize

def is_student(text: str) -> bool:
  return _is_student(
    fix_grammar(normalize(text))
  )

def describe_are_students():
  def it_works():
    texts = [
      "I'm a student",
      "I'm a developer",
    ]
    assert are_students(texts) == [
      True,
      False,
    ]

def describe_is_student():
  def it_basically_works():
    assert is_student("I'm a student")
    assert is_student("Carl was a student")
    assert is_student("Maria is an undergraduate")
    assert is_student("Phd student")
    assert not is_student("Michael is a bachelor in MIT")
    assert not is_student("I'm a perpetual student")
    assert is_student("Chasing a perpetual motion. An applied mechanics student")
    assert is_student("My name is Josh Student")
    # ^ known false positive. Can't fix due to Spacy model limitations,
    # without a retrained Spacy model, that properly recognizes PROPN vs NOUN.
    assert not is_student("A friend of a student")
    assert not is_student("On a mission to help every student")
    assert not is_student("Being a life-long student is hard")

  def it_handles_set1():
    assert not is_student("On a mission to help every student to reach their potential with technologies")
    assert not is_student("Software engineer and PhD student specializing in robotics")
    assert is_student("PhD student making open source learning tools.")
    assert not is_student("Lawyer. Lecturer. Researcher. Student")
    assert not is_student("Developer at Sky and undergraduated in C.S. in Federal University of South Frontier")

  def it_handles_set2():
    assert not is_student("Gamer, life-long student and hacker of regexes.")
    assert is_student("Gamer, student, hacker of regexes.")
    assert is_student("Hello there, I am a passionate student who loves to learn and explore new things!")
    assert is_student("undergraduate student of Tongji university")
    assert is_student("Undergraduate at UC Berkeley, double major in CS and Math.")

  def it_handles_set3():
    assert is_student("Undergraduate studying 'Software and Information Engineering' at the Vienna University of Technology")
    assert not is_student("Junior UI Designer @ Section BFA Design Art Undergraduate from NTU ADM, Singapore")
    assert not is_student("Associate Professor, Vice Dean for Undergraduate Studies")
    assert not is_student("associate dean of undergraduate education school of engineering and applied sciences")
    assert is_student("Graduate Diploma in IT graduate with an undergraduate degree in Bachelor of Laws")

  def it_handles_set4():
    assert not is_student("""
      Professor of the Practice in Computer Science, Program Director
      for the Fundamentals of Computing Undergraduate Certificate Program
    """)
    assert is_student("""
      My name is Harold Bogg, I am a college student, I like basketball, music,
      my favorite star is lebron James of the Laker
    """)
    assert not is_student("""
      Senior Software Engineer at @pagarme | Computer Science undergraduate at Pontifical Catholic University of Paraná
    """)
    assert not is_student("Full-time software developer and student. Spare-time Japan fan and gamer")
    assert is_student("Student of Chinese medicine, dance teacher, rare soul & funk music digger")

  def it_handles_set5():
    assert not is_student("I engineer 'learn by doing' experiences for uni students with lean, agile, & service design.")
    assert not is_student("""
      Software engineer at @GRID-is. Fellow of the Royal Geographical Society.
      Postgraduate student at Lund University.
    """)
    assert not is_student("""
      Lead AI/ML Engineer at MITRE. Graduate student in Statistics at George Mason University.
      Officer emeritus of @srct, @gmuthetatau, @masonlug
    """)
    assert not is_student("""
      A strong conceptual thinker and a constant student who has a keen interest in all things
      related to the Internet. An avid developer, entrepreneur obsessed with
    """)
    assert is_student("Dad | Runner | Aviation Student | Dog Lover | Builder of cool shit")

  def it_handles_set6():
    assert not is_student("Engineering @ Rubrik. MemCachier Co-Founder. Formerly Stanford CS PhD Student.")
    assert is_student("Blockchain student. Crypto investor.")
    assert not is_student("""
      Technology leader at Gartner (Managing Vice President).
      Graduate student at University of Illinois, getting my MBA. Forever an engineer.
    """) # Note: fails without comma before "getting" :( -- need to retrain POS tagger.
    assert is_student("""
      Graduate student at University of Illinois, getting my MBA. Forever an engineer.
    """)  # Note: fails without comma before "getting" :( -- need to retrain POS tagger.
    assert not is_student("""
      Technology entrepreneur, sports lover, network security student.
    """)

  def it_handles_set7():
    assert not is_student("""
      👨‍💻 developer of 🌐 coora-ai.com 🧭 igapo.xyz / tech enthusiast / applied artificial intelligence student
    """)
    assert is_student("""
      👨 tech enthusiast / applied artificial intelligence student
    """)
    assert is_student("A Ph.D. student in statistical science.")
    assert is_student("PhD student at MIT Brain and Cognitive Sciences")
    assert not is_student("VP Eng. at MedScout, storyteller, student of disasters.")

  def it_handles_set8():
    assert is_student("Biotech student and sometimes software developer.")
    assert not is_student("Software developer and sometimes biotech student.")
    assert not is_student("Everlasting student · Rails Core · Zeitwerk · Freelance · Life lover")
    assert not is_student("Principal Engineer @github. Ruby/Go mostly. Perpetual student.")
    assert not is_student("Perpetual student. Principal Engineer @github. Ruby/Go mostly.")

  def it_handles_set9():
    assert not is_student("""
      TOGAF 9 Certified Enterprise Architect, Pragmatist, Economic Student, Biker,
      Bass Fisherman (Angler), Coder (Angular), FX Trader, American Football fan.
    """)
    assert not is_student("""
      As a Klingon code warrior, I take seriously the old proverb:
      "ghojwI'pu'lI' tISaH" ('Care about your students').
    """)
    assert is_student("""
      Currently a Computer Science graduate student at University
      of the Philippines Diliman working on quantum algorithms.
    """)
    assert not is_student("""
      Over 30 years of experience working with diverse teams of researchers and
      students developing interactive software and hardware for science inquiry.
    """)
    assert is_student("B.Sc. in C.S. and M.Eng. student at the University of Bologna. I randomly bump into some code.")
    # Note: ^ should be false, add Bachelor as "Graduate" synonim

  def it_handles_set10():
    assert not is_student("""
      I am Viktor Klang, a finder, researcher, problem solver, improver of things,
      life-long student, developer/programmer, leader, mentor/advisor, public speaker…
    """)
    assert not is_student("""
      Specializing generalist. CS PhD, student of life. Lover of words and hyperbole. Remote.
    """)
    assert is_student("music student java elasticsearch ai subversion git vim node, fans of strings instrument")
    # FN ^ Spacy can't interpret this mess properly
    assert not is_student("Back-End Developer | Information Systems bachelor")
    assert is_student("CS Bachelor student at USI")
    assert not is_student("CS Bachelor at USI")

  def it_handles_set11():
    assert is_student("Bachelor student of Comp Sci @ Concordia University")
    assert not is_student("Bachelor of Comp Sci student @ Concordia University")
    # FN ^ Spacy can't interpret this mess
    assert not is_student("Private Pilot | Bachelor of Science")
    assert not is_student("Computer Engineer & MSc Student")
    assert is_student("MSCS Student")

  def it_handles_set12():
    assert is_student("Bachelor student of Comp Sci @ Concordia University")
    assert not is_student("Bachelor of Comp Sci student @ Concordia University")
    # FN ^ Spacy can't interpret this mess
    assert not is_student("Private Pilot | Bachelor of Science")
    assert not is_student("Computer Engineer & MSc Student")
    assert is_student("MSCS Student")
