# from src.parser import test
from parsers.parsers import parse_phones, parse_emails

# Emails and phone numbers are fake (generated). Potential clashes will existing contacts
# of real people are coincidental and not intended.

def describe_parse_phones() -> None:
    def parses_international() -> None:
        assert parse_phones("+1 123 456-7890") == ["+11234567890"]    # US
        assert parse_phones("+44 20 1234 5678") == ["+442012345678"]  # UK
        assert parse_phones("+61 2 1234 5678") == ["+61212345678"]    # Australia
        assert parse_phones("+1 416 123-4567") == ["+14161234567"]    # Canada
        assert parse_phones("+39 02 1234 5678") == ["+390212345678"]  # Italy
        assert parse_phones("+91 12345 67890") == ["+911234567890"]   # India
        assert parse_phones("+91 1234-567890") == ["+911234567890"]   # India v2
        assert parse_phones("+49 999 12345678") == ["+4999912345678"] # Germany
        assert parse_phones("+49 30 12345678") == ["+493012345678"]   # Germany v2

    def does_not_parse_arithmetic() -> None:
        assert parse_phones("x = 1 + 3.14") == []
        assert parse_phones("(17 +30658)") == []
        assert parse_phones("49x+384") == []
        assert parse_phones("+38,400,800$") == []
        assert parse_phones("+38,400,800$") == []
        assert parse_phones("0793412657 seconds elapsed") == []

    def parses_unicode() -> None:
        assert parse_phones("☎ 5573558") == ["5573558"]
        assert parse_phones("📞5573558") == ["5573558"]
        assert parse_phones("☎️5573558") == ["5573558"]
        assert parse_phones("📱:5573558") == ["5573558"]

    def parses_urls() -> None:
        assert parse_phones("https://wa.me/15551234567") == ["+15551234567"]
        assert parse_phones("https://t.me/+15551234567") == ["+15551234567"]

    def parses_prefixed_set1() -> None:
        assert parse_phones("Automotive developer in Reproteq & Fixhex [phone +44 637594190]") == ["+44637594190"]
        assert parse_phones("phone: 27737526637 WeChat: 27737526367") == ["27737526637"]
        assert parse_phones("Email: natt@gmail.com Phone: +54 7934483354 +96 13729958189") == ["+547934483354"]
        assert parse_phones("WeChat & Phone: 28813178921. Email: zangho@lab.com") == ["28813178921"]
        assert parse_phones("Avid Full Stack Developer Email: akashkash934@hotmail.ru Phone: +81 7355891640") == ["+817355891640"]

    def parses_prefixed_set2() -> None:
        assert parse_phones("Python-backend developer Phone: +998950609954") == ["+998950609954"]
        assert parse_phones("HCM66 Phone https://hcm66.com | https://hcm66.com | https://hcm666.com") == []
        assert parse_phones("Phone Number: +55 91 99601-4554 E-mail: antonioluca902@gmail.com") == ["+5591996014554"]
        assert parse_phones("Phone: +84.933911093 Email: 1870583@vermut.edu.vn / cxtinh.gov.vn") == ["+84933911093"]
        assert parse_phones("Phone : +94 769767692 || Email : mohamedalthaff@gmail.com || Phone +555") == ["+94769767692"]

    def parses_prefixed_set3() -> None:
        assert parse_phones("email: bishal-hadka-1600@gg.com phone: 970-799-9291") == ["9707999291"]
        assert parse_phones("Consultant/Trainer - React.js, Node.js Phone:- 8637 44 8012") == ["8637448012"]
        assert parse_phones("Phone: +380969490333") == ["+380969490333"]
        assert parse_phones("Sefine Shipyard Phone: +90(553) 382 85 13 https://www.linkedin.com/in/hhy34/") == ["+905533828513"]
        assert parse_phones("Email: justin.rick@gmail.com Phone: 9046571689") == ["9046571689"]

    def parses_prefixed_set4() -> None:
        assert parse_phones("Django And Flutter Contributor - OpenSRP Phone: 0653188031") == ["0653188031"]
        assert parse_phones("kakao:youngchol2 phone:010-4417-3317") == ["01044173317"]
        assert parse_phones("I am a web developer Email : 99haroon99@gmail.com. Phone : 03122325792") == ["03122325792"]
        assert parse_phones("QQ:3206771968 Phone-Number: 86-13979231490 Wechat:tel-F4 Add-Me") == ["8613979231490"]
        assert parse_phones("EMAIL: otakoijairus@gmail.com | PHONE: +254722763364") == ["+254722763364"]

    def parses_prefixed_set5() -> None:
        assert parse_phones("phone:93-009-1994 Front-end developer") == ["930091994"]
        assert parse_phones("Phone : 03028921818") == ["03028921818"]
        assert parse_phones("Phone number: 0793412657") == ["0793412657"]
        assert parse_phones("email: huyhain926guyen@gmail.com phone: (+84) 39-226-0047") == ["+84392260047"]
        assert parse_phones("Cell phone: 603-923-3615") == ["6039233615"]

    def parses_prefixed_set6() -> None:
        assert parse_phones("QQ:308066400 WhatsApp:+1.2086141414 phone：+86.13516521121") == ["+8613516521121"]
        assert parse_phones("Phone number : +964 07705856141") == ["+96407705856141"]
        assert parse_phones("Phone number : 09078451758") == ["09078451758"]
        assert parse_phones("phone: +86 186-4202-1059") == ["+8618642021059"]
        assert parse_phones("Phone: 03366893938") == ["03366893938"]

    def parses_prefixed_set7() -> None:
        assert parse_phones("Phone +18608000001") == ["+18608000001"]
        assert parse_phones("Phone : 03422080317") == ["03422080317"]
        assert parse_phones("webchat : 18210659133 phone : +8618210659133 💯") == ["+8618210659133"]
        assert parse_phones("E-mail: ahmedalmohammed2@gmail.com Phone: +962777128689") == ["+962777128689"]
        assert parse_phones("QQ:825846102 Phone:15910377031") == ["15910377031"]

    def parses_prefixed_set8() -> None:
        assert parse_phones("Tel: +7919-086-29-27") == ["+79190862927"]
        assert parse_phones("Phone: +7(919)-086-2977") == ["+79190862977"]
        assert parse_phones("Phone : +989395912630") == ["+989395912630"]
        assert parse_phones("From: Uzbekistan Phone: +998903519040") == ["+998903519040"]
        assert parse_phones("phone/mobile = +918210268246") == ["+918210268246"]

def describe_parse_emails() -> None:
    def parses_set1() -> None:
        assert parse_emails("email: bishal-hadka-1600@gg.com phone: 970-799-9291") == ["bishal-hadka-1600@gg.com"]
        assert parse_emails("akashkash934@hotmail.ru") == ["akashkash934@hotmail.ru"]
        assert parse_emails("Email, Phone, other contacts") == []
        assert parse_emails("Email: justin.rick@gmail.com Phone: 9046571689") == ["justin.rick@gmail.com"]
        assert parse_emails("huyhain926guyen@gmail.com salmanzuck@zoho.com") == ["huyhain926guyen@gmail.com", "salmanzuck@zoho.com"]
