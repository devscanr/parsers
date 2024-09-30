## Parsers

Parse phones, email, etc. from human texts (imprecisely formatted).

## Existing Libraries

Existing libraries: 
- https://github.com/daviddrysdale/python-phonenumbers

Inacceptable tradeoffs:

#### Ambiguity

Phone numbers, in general, are ambiguos. They can match numbers in math formulas,
crypto wallets identifiers, different card numbers, etc. To not allow false positives, we can't simply
capture anything "resembling" a phone. Emails, at least, have globally unique formatting and while
there's also a potential for ambiguity (e.g. emails in markdown vs emails in markdown code), it's arguably
lower.

#### Complexity

`python-phonenumbers` in particular claims to take 12Mb of RAM and more just to store some locale-specific
data. How much of this data is really useful in reality, where people mistype numbers, forget to
close parentheses and so on?

#### Culture agnostic

`python-phonenumbers` requires to know the locale for numbers that are not properly internatiolized.
This is inacceptable for real-world parsing where we often don't know the locale.
