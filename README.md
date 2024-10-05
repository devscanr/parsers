## Extractors

Extract (parse) phones, email, etc. from human texts. Aims to supports an imprecisely formatted data,
to the degree it's possible to support.

### Phone number recognition

- International format (e.g `+49 30 xxxxxxxx`)
- Preceded by trigger words (e.g. `Phone: xxx`, `Whatsapp: xxx`)
- Preceded by unicode emojis (e.g. `📞 xxx`)
- From URLs (e.g. `t.me/xxxxxxxx`)

## Existing Libraries

Existing libraries: 
- https://github.com/daviddrysdale/python-phonenumbers

### Inacceptable tradeoffs

#### Ambiguity

Phone numbers, in general, are ambiguos. They can match numbers in math formulas,
crypto wallet ids, different card numbers, etc. To prevent false positives, we can't simply
capture anything "resembling a phone". Emails, at least, have globally unique formatting and while
there's always potential for ambiguity and contextuality (should we capture emails from markdown code),
it's less likely to capture a non-email token as an email.

#### Complexity

`python-phonenumbers` in particular claims to take 12Mb of RAM just to load locale-specific
data. How much of that is really useful? People mistype numbers, forget to
close parentheses... You can't match against formats that are not obeyed, to begin with.

#### Culture agnostic

`python-phonenumbers` can parse properly formatted international numbers. In many cases 
you have to provide a locale to disambiguate. This is inacceptable for real-world parsing 
where we often don't know the locale.
