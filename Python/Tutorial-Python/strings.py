#!/usr/bin/env python3

# References
# https://docs.python.org/3/library/string.html
# https://docs.python.org/3/tutorial/introduction.html#strings
# https://docs.python.org/3/library/stdtypes.html#textseq
# https://docs.python.org/3/tutorial/inputoutput.html
# https://docs.python.org/3/reference/lexical_analysis.html#literals
# https://docs.python.org/3/library/text.html#stringservices

print(f'\n===== Running {__file__} =====\n')
import pytest
import string
from string import Template
_string = 'ABC'
_integer = 555
_float = 555.555

################################################################################
# Syntax
################################################################################
# single, double, and triple quotes
assert 'string' == "string" == '''string''' == """string"""
assert 'doesn\'t' == "doesn't" == '''doesn't''' == """doesn't"""
assert 'He said "Hi".' == "He said \"Hi\"." == """He said "Hi".""" == '''He said "Hi".'''
assert '''Multiline
comments''' == ('Multiline'
'\ncomments') == 'Multiline\ncomments'

# Conversion
assert str(1234) == '1234'
assert str(1/3)  == '0.3333333333333333'

# Literals
s  =   'default string       (Tab : "\t") (Unicode : \u03A3) ({1+1})' # unicode string literal
u  =  u'unicode string       (Tab : "\t") (Unicode : \u03A3) ({1+1})'
f  =  f'formatted string     (Tab : "\t") (Unicode : \u03A3) ({1+1})' # formatted to unicode string literal
r  =  r'raw string           (Tab : "\t") (Unicode : \u03A3) ({1+1})'
rf = rf'raw formatted string (Tab : "\t") (Unicode : \u03A3) ({1+1})'
b  =  b'byte string        (Tab : "\t") (Unicode : \u03A3) ({1+1})' # was default for Python 2
rb = rb'raw byte string    (Tab : "\t") (Unicode : \u03A3) ({1+1})'
for x in [s,u,f,b,r,rf,rb]: print(x)
print()

# Escape sequences
# \newline 	Backslash and newline ignored
# \\ 		Backslash (\)
# \' 		Single quote (')
# \" 		Double quote (")
# \a 		ASCII Bell (BEL)
# \b 		ASCII Backspace (BS)
# \f 		ASCII Formfeed (FF)
# \n 		ASCII Linefeed (LF)
# \r 		ASCII Carriage Return (CR)
# \t 		ASCII Horizontal Tab (TAB)
# \v 		ASCII Vertical Tab (VT)
# \ooo 		Character with octal value ooo
# \xhh 		Character with hex value hh

# \N{name} 	Character named name in the Unicode database
# \uxxxx 	Character with 16-bit hex value xxxx
# \Uxxxxxxxx 	Character with 32-bit hex value xxxxxxxx

################################################################################
# Manipulation
################################################################################
assert 'Hello' ' world' == 'Hello' + ' world' == 'Hello world'
assert 'x'*3 == 'xxx'

# Slicing (start:stop:step)
#  _________________________
#  | P | y | t | h | o | n |
#  0   1   2   3   4   5   6
# -6  -5  -4  -3  -2  -1
s = "Python"
assert s[0] == s[-len(s)] == s[0:1] == 'P'
assert s[-1] == s[len(s)-1] == 'n'
assert s == s[::] == s[0:len(s):1]
assert s[::2] == 'Pto'
assert s[::-1] == 'nohtyP'
assert s[len(s):0:-1] == 'nohty'
assert s[4:3] == s[4:3:1] == s[3:4:-1] == ''
assert s[-len(s):] == s[-len(s)-100:]
assert s[:len(s)] == s[:len(s)+100]
with pytest.raises(IndexError): s[len(s)+100]
with pytest.raises(IndexError): s[-len(s)-100]
with pytest.raises(TypeError): s[0] = 'X'


################################################################################
# Formatting comparisons
# > Types of string formatting
#   (1) Manual string formatting
#   (2) %-interpolation
#   (3) str.format()
#   (4) Template strings
#   (5) Formatted string literals (f-strings)
# > Standard format specifier
#   [[fill]align][sign][#][0][width][grouping_option][.precision][type]
#   fill            ::=  <any character>
#   align           ::=  "<" | ">" | "=" | "^"
#   sign            ::=  "+" | "-" | " "
#   width           ::=  digit+
#   grouping_option ::=  "_" | ","
#   precision       ::=  digit+
#   type            ::=  bcdeEfFgGnosxX%
# ################################################################################
# Method comparison
print('String '+_string+'; Integer '+str(_integer)+'; Float '+str(_float))
print('String %s; Integer %i; Float %f' % (_string, _integer, _float))
print('String {}; Integer {}; Float {}'.format(_string, _integer, _float))
print(f'String {_string}; Integer {_integer}; Float {_float}')
print(Template('String $s; Integer $i; Float $f').substitute(s=_string, i=_integer, f=_float))
print()

################################################################################
# f-strings
assert f'{_integer}' == f'{_integer:d}' == str(_integer)
assert f'{_string}'  == f'{_string:s}'  == str(_string) == _string
# Argument conversion
x = '(\t) (\u03A3)'
print(f'no      converstion : {x}')
print(f'str()   converstion : {x!s}')
print(f'repr()  converstion : {x!r}')
print(f'ascii() converstion : {x!a}')

## general padding and aligning (fill, align, width)
s = 'Python'
assert f'{s:<10}'  == 'Python    ' == f'{s:10}'
assert f'{s:>10}'  == '    Python'
assert f'{s:^10}'  == '  Python  '
assert f'{s:_<10}' == 'Python____'

## padding for sign (sign)
assert f'{1:+} {-1:+}' == '+1 -1'
assert f'{1:-} {-1:-}' == '1 -1'
assert f'{1: } {-1: }' == ' 1 -1'
assert f'{1:0=+3} {-1:0=+3}' == '+01 -01'
assert f'{1:0=-3} {-1:0=-3}' == '001 -01' == f'{1:03} {-1:03}'
assert f'{1:0= 3} {-1:0= 3}' == ' 01 -01'

## Thousands seperator (0)
assert f'{1000000:,}' == '1,000,000'
assert f'{1000000:_}' == '1_000_000'

## Integer presentation (decimal : binary : octal : HEX : hex)
assert f'{255:d}' == f'{0b11111111:d}' == f'{0o377:d}' == f'{0XFF:d}' == f'{0xff:d}' == '255'
assert f'{255:b}' == f'{0b11111111:b}' == f'{0o377:b}' == f'{0XFF:b}' == f'{0xff:b}' == '11111111'
assert f'{255:o}' == f'{0b11111111:o}' == f'{0o377:o}' == f'{0XFF:o}' == f'{0xff:o}' == '377'
assert f'{255:X}' == f'{0b11111111:X}' == f'{0o377:X}' == f'{0XFF:X}' == f'{0xff:X}' == 'FF'
assert f'{255:x}' == f'{0b11111111:x}' == f'{0o377:x}' == f'{0XFF:x}' == f'{0xff:x}' == 'ff'
### Alternate form (#) - add prefix
assert f'{11:#d}' == f'{11:d}' == '11'
assert f'{0b11:#b}' == '0b' + f'{0b11:b}' == '0b11'
assert f'{0o11:#o}' == '0o' + f'{0o11:o}' == '0o11'
assert f'{0x11:#x}' == '0x' + f'{0x11:x}' == '0x11'
assert f'{0X11:#X}' == '0X' + f'{0X11:X}' == '0X11'

## Float presentation (fixed : exponent)
fp = 5/9 * 1000
inf = float('INF')
nan = float('NAN')
assert f'{fp}'    == '555.5555555555555'
assert f'{fp:f}'  == f'{fp:.6f}' == '555.555556'
assert f'{fp:e}'  == f'{fp:.6e}' == '5.555556e+02' 
assert f'{inf:f}' == f'{inf:e}' == 'inf'
assert f'{inf:F}' == f'{inf:E}' == 'INF'
assert f'{nan:f}' == f'{nan:e}' == 'nan'
assert f'{nan:F}' == f'{nan:E}' == 'NAN'

assert f'{0.0005555:f}' == f'{5.555e-4:f}' == '0.000556'
assert f'{0.0005555:e}' == f'{5.555e-4:e}' == '5.555000e-04'
l = [f'{50 / 10**x:g}' for x in range(8)]
assert l == ['50', '5', '0.5', '0.05', '0.005', '0.0005', '5e-05', '5e-06']
assert f'{0.0005555:%}' == '0.055550%'
### Alternate form (#) -- force decimal point
assert f'{10:#.0f}' == f'{10:.0f}' + '.' == '10.'

## Putting it all together
assert f'{12345.6789999:_>+15_.3f}' == '____+12_345.679'

## Other
import datetime
d = datetime.datetime(2010, 7, 4, 12, 15, 58)
assert f'{d:%Y-%m-%d %H:%M:%S}' == '2010-07-04 12:15:58'

################################################################################
# Manula string formatting

################################################################################
# %-interpolation

################################################################################
# str.format()
# > Same format specifier syntax as f-strings but replacement field differs
assert f'{_integer!s:10}' == '{_integer!s:10}'.format(_integer=_integer)
assert '{} {}'.format(  'A','B') == 'A B' =='{0} {1}'.format('A','B')
assert '{1} {0}'.format('A','B') == 'B A'
assert '{0} {0}'.format('A','B') == 'A A'
assert '{1} {1}'.format('A','B') == 'B B'
assert '{arg1} {arg2}'.format(arg1='A', arg2='B') == 'A B'

################################################################################
# Template strings

################################################################################
# Why %-formatting is discouraged

# Why f-strings are preferred over str.format()

################################################################################
# String methods
################################################################################
# Modify case
# string.capitalize
# string.casefold
# string.lower
# string.title
# string.upper
# string.swapcase

# Modify alignment (center, ljust, rjust, zfill)
s = 'Python'
assert s.center(10) == s.center(10,' ') == '  Python  '
assert s.ljust(10)  == s.ljust(10,' ')  == 'Python    '
assert s.rjust(10)  == s.rjust(10,' ')  == '    Python'
assert s.zfill(10)  == s.rjust(10,'0')  == '0000Python'

# Remove or replace
# string.expandtabs
# string.strip
# string.lstrip
# string.rstrip
# string.replace
# string.translate and string.maketrans

# Analyze
# string.count
# string.find
# string.rfind
# string.index
# string.rindex

# Combine (input iterable)
# string.join

# Break up (return list)
# string.split
# string.rsplit
# string.partition
# string.rpartition
# string.splitlines

# Test
# string.isalnum
# string.isalpha
# string.isascii
# string.isdecimal
# string.isdigit
# string.isidentifier
# string.islower
# string.isnumeric
# string.isprintable
# string.isspace
# string.istitle
# string.isupper
# string.startswith
# string.endswith

# Transform
# string.encode

################################################################################
# String module
################################################################################
import string
assert string.ascii_lowercase == 'abcdefghijklmnopqrstuvwxyz'
assert string.ascii_uppercase == 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
assert string.digits          == '0123456789'
assert string.hexdigits       == '0123456789abcdefABCDEF'
assert string.octdigits       == '01234567'
assert string.punctuation     == '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
assert string.whitespace      ==  ' \t\n\r\x0b\x0c'
assert string.ascii_letters == string.ascii_lowercase + string.ascii_uppercase
assert string.printable == (string.digits
                           +string.ascii_letters
                           +string.punctuation
                           +string.whitespace)

s = 'It was the best of times, it was the worst of times.'
assert string.capwords(s) == s.title()

################################################################################
print()
