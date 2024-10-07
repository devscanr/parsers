from extractors.student import is_student

def describe_is_student() -> None:
  def it_works() -> None:
    assert is_student("I'm a student") == True
    assert is_student("Carl is a student") == True
    assert is_student("Phd student") == True
    assert is_student("I'm a perpetual student") == False
    assert is_student("Chasing a perpetual motion. An applied mechanics student") == True
    assert is_student("My name is Josh Student") == True
    # ^ known false positive. Can't fix due to Spacy model limitations,
    # without a retrained Spacy model, that properly recognizes PROPN vs NOUN.
    assert is_student("A friend of a student") == False
    assert is_student("On a mission to help every student") == False
    # assert is_student("Being a life-long student is hard") == False

  def it_handles_set1() -> None:
    assert is_student("On a mission to help every student to reach their potential with technologies") == False
    assert is_student("Software engineer and PhD student specializing in robotics") == False
    assert is_student("PhD student making open source learning tools.") == True
    assert is_student("Lawyer. Lecturer. Researcher. Student") == False
    assert is_student("Developer at Sky and undergraduated in C.S. in Federal University of South Frontier") == False

  def it_handles_set2() -> None:
    assert is_student("Gamer, life-long student and hacker of regexes.") == False
    assert is_student("Gamer, student, hacker of regexes.") == True
    assert is_student("Hello there, I am a passionate student who loves to learn and explore new things!") == True
    assert is_student("undergraduate student of Tongji university") == True
    assert is_student("Undergraduate at UC Berkeley, double major in CS and Math.") == True

  def it_handles_set3() -> None:
    assert is_student("Undergraduate studying 'Software and Information Engineering' at the Vienna University of Technology") == True
    assert is_student("Junior UI Designer @ Section BFA Design Art Undergraduate from NTU ADM, Singapore") == False
    assert is_student("Associate Professor, Vice Dean for Undergraduate Studies") == False
    assert is_student("associate dean of undergraduate education school of engineering and applied sciences") == False
    assert is_student("Graduate Diploma in IT graduate with an undergraduate degree in Bachelor of Laws") == False

  def it_handles_set4() -> None:
    assert is_student("""
      Professor of the Practice in Computer Science, Program Director 
      for the Fundamentals of Computing Undergraduate Certificate Program
    """) == False
    assert is_student("""
      My name is Harold Bogg, I am a college student, I like basketball, music, 
      my favorite star is lebron James of the Laker
    """) == True
    assert is_student("""
      Senior Software Engineer at @pagarme | Computer Science undergraduate at Pontifical Catholic University of Paraná
    """) == False
    assert is_student("Full-time software developer and student. Spare-time Japan fan and gamer") == False
    assert is_student("Student of Chinese medicine, dance teacher, rare soul & funk music digger") == True

  def it_handles_set5() -> None:
    assert is_student("I engineer 'learn by doing' experiences for uni students with lean, agile, & service design.") == False
    assert is_student("""
      Software engineer at @GRID-is. Fellow of the Royal Geographical Society. 
      Postgraduate student at Lund University.
    """) == False
    assert is_student("""
      Lead AI/ML Engineer at MITRE. Graduate student in Statistics at George Mason University. 
      Officer emeritus of @srct, @gmuthetatau, @masonlug
    """) == False
    assert is_student("""
      A strong conceptual thinker and a constant student who has a keen interest in all things 
      related to the Internet. An avid developer, entrepreneur obsessed with
    """) == False
    assert is_student("Dad | Runner | Aviation Student | Dog Lover | Builder of cool shit") == True

  def it_handles_set6() -> None:
    assert is_student("Engineering @ Rubrik. MemCachier Co-Founder. Formerly Stanford CS PhD Student.") == False
    assert is_student("Blockchain student. Crypto investor.") == True
    assert is_student("""
      Technology leader at Gartner (Managing Vice President). 
      Graduate student at University of Illinois, getting my MBA. Forever an engineer.
    """) == False # Note: fails without comma before "getting" :( -- need to retrain POS tagger.
    assert is_student("""
      Graduate student at University of Illinois, getting my MBA. Forever an engineer.
    """) == True # Note: fails without comma before "getting" :( -- need to retrain POS tagger.
    assert is_student("""
      Technology entrepreneur, sports lover, network security student.
    """) == False

  def it_handles_set7() -> None:
    assert is_student("""
      👨‍💻 developer of 🌐 coora-ai.com 🧭 igapo.xyz / tech enthusiast / applied artificial intelligence student
    """) == False
    assert is_student("""
      👨 tech enthusiast / applied artificial intelligence student
    """) == True
    assert is_student("A Ph.D. student in statistical science.") == True
    assert is_student("PhD student at MIT Brain and Cognitive Sciences") == True
    assert is_student("VP Eng. at MedScout, storyteller, student of disasters.") == False

  def it_handles_set8() -> None:
    assert is_student("Biotech student and sometimes software developer.") == True
    assert is_student("Software developer and sometimes biotech student.") == False
    assert is_student("Everlasting student · Rails Core · Zeitwerk · Freelance · Life lover") == False
    assert is_student("Principal Engineer @github. Ruby/Go mostly. Perpetual student.") == False
    assert is_student("Perpetual student. Principal Engineer @github. Ruby/Go mostly.") == False

  def it_handles_set9() -> None:
    assert is_student("""
      TOGAF 9 Certified Enterprise Architect, Pragmatist, Economic Student, Biker, 
      Bass Fisherman (Angler), Coder (Angular), FX Trader, American Football fan.
    """) == False
    assert is_student("""
      As a Klingon code warrior, I take seriously the old proverb: 
      "ghojwI'pu'lI' tISaH" ('Care about your students').
    """) == False
    assert is_student("""
      Currently a Computer Science graduate student at University 
      of the Philippines Diliman working on quantum algorithms.
    """) == True
    assert is_student("""
      Over 30 years of experience working with diverse teams of researchers and 
      students developing interactive software and hardware for science inquiry.
    """) == False
    assert is_student("B.Sc. in C.S. and M.Eng. student at the University of Bologna. I randomly bump into some code.") == True
    # Note: ^ should be false, add Bachelor as "Graduate" synonim

  def it_handles_set10() -> None:
    assert is_student("""
      I am Viktor Klang, a finder, researcher, problem solver, improver of things,
      life-long student, developer/programmer, leader, mentor/advisor, public speaker…
    """) == False
    assert is_student("""
      Specializing generalist. CS PhD, student of life. Lover of words and hyperbole. Remote.
    """) == False
    assert is_student("music student java elasticsearch ai subversion git vim node, fans of strings instrument") == False
    # FN ^ Spacy can't interpret this mess properly
    assert is_student("Back-End Developer | Information Systems bachelor") == False
    assert is_student("CS Bachelor student at USI") == True
    assert is_student("CS Bachelor at USI") == False

  def it_handles_set11() -> None:
    assert is_student("Bachelor student of Comp Sci @ Concordia University") == True
    assert is_student("Bachelor of Comp Sci student @ Concordia University") == False
    # FN ^ Spacy can't interpret this mess
    assert is_student("Private Pilot | Bachelor of Science") == False
    assert is_student("Computer Engineer & MSc Student") == False
    assert is_student("MSCS Student") == True

