#!/usr/bin/env python3

# References
# https://docs.python.org/3/howto/regex.html
# https://docs.python.org/3/library/re.html

print(f'\n===== Running {__file__} =====\n')
import re
import pytest
import string
print("Printable characters :", repr(string.printable))

################################################################################
# Basic search and find functions in re module (search, match, findall, finditer)
################################################################################
s = 'Match this'
p = 'this'

match = re.search(p, s)
assert type(match) == re.Match
assert match.group() == 'this'

assert re.search(p, s) != re.search(p, s)
assert re.search(p, s).group() == re.search(p, s).group()
assert re.search('no match', s) == None

pattern = re.compile(p)
assert pattern.search(s).group() == re.search(p, s).group()

# Other common search functions
assert re.match(p, s) == re.search("^" + p, s) == None
s = 'Match this and this and this'
assert re.findall(p, s) == ['this', 'this', 'this']
assert [m.group() for m in re.finditer(p, s)] == ['this', 'this', 'this']
assert [m.start() for m in re.finditer(p, s)] == [6, 15, 24]

def grep(pattern, string, mode=0b0):
    matches = [m.group() for m in re.finditer(pattern, string, mode)]

    # Correct for patterns that match zero-lenth strings (e.g. '.*', '.?')
    if len(matches) > 0 and not matches[0]:
        # e.g. ['','a','','b',''] -> ['']
        matches = matches[:1]
    if len(matches) > 1 and not matches[-1]:
        # e.g. ['a','b',''] -> ['a','b']
        matches = matches[:-1]


    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        return matches
    else:
        return None

################################################################################
# Character sets/classes ('[]')
################################################################################
for c in (string.ascii_letters + string.digits):
    assert grep('[a-fA-F0-5]',  c) == grep('[abcdefABCDEF012345]', c)
    # Negation (^)
    assert grep('[^a-fA-F0-5]', c) != grep('[abcdefABCDEF012345]', c)

# Escaping character class metacharacters ('][\^-')
for c in '][\\^-':
    # ']', '[', and '\' must always be escaped
    # '^' must be escaped to be the first literal
    # '-' must be escaped unless it is the first or last literal
    assert grep(r'[\- \[ \\ \] \^]', c) == c
    assert grep(r'[-^]', c) == grep(r'[\^\-]', c)

########################################
# Shorthand classes (\d\D \w\W \s\S) and the dot (.)
for c in string.printable:
    raw_c = f'{c!r}'[1:-1] # convert to raw string
    # Not available in python
    #   \l == [a-z]
    #   \u == [A-Z]
    #   POSIX bracket expressions (e.g. [:alnum:], [:digit:])
    assert grep(r'\d', raw_c) == grep(r'[0-9]',       raw_c)
    assert grep(r'\D', raw_c) == grep(r'[^0-9]',       raw_c)
    
    assert grep(r'\w', raw_c) == grep(r'[A-Za-z\d_]', raw_c)
    assert grep(r'\W', raw_c) == grep(r'[^A-Za-z\d_]', raw_c)
    
    assert grep(r'\s', raw_c) == grep(r'[ \t\r\n\f]', raw_c)
    assert grep(r'\S', raw_c) == grep(r'[^ \t\r\n\f]', raw_c)
    
    assert grep(r'.',  raw_c) == grep(r'''[\w\s!"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~]''', raw_c)

################################################################################
# Alteration (|)
assert grep('this|that', 'this or that') == ['this', 'that']

################################################################################
# Zero-width assertions 
################################################################################
# Anchors (^ $)
assert grep(r'^abc','abc 123') == 'abc' 
assert grep(r'^abc','123 abc') == None 
assert grep(r'abc$','abc 123') == None
assert grep(r'abc$','123 abc') == 'abc' 

# Word boundaries (\b \B)
for c in string.printable.replace('a',''):
    # \b = [^a-zA-Z0-9_] but without a match
    s = c+'a'
    if c in (string.ascii_letters + string.digits + '_'):
        assert grep(r'\ba', s) == None
        assert grep(r'\Ba', s) == 'a'
    else:
        assert grep(r'\ba', s) == 'a' 
        assert grep(r'\Ba', s) == None

################################################################################
# Repitition
################################################################################
for s in ['', 'a', 'aa', 'aaa', 'a'*100]:
    assert grep(r'a{3}', s) == grep(r'aaa', s)
    assert grep(r'a{3,5}', s) == grep(r'aaaaa|aaaa|aaa', s)
    assert grep(r'a?', s) == grep(r'a{,1}', s)
    assert grep(r'a+', s) == grep(r'a{1,}', s)
    assert grep(r'a*', s) == grep(r'a{0,}', s)

# Non greedy (*? +? ?? {m,n}?)
s = '012345'
assert grep(r'\d{3,5}',  s) == '01234'
assert grep(r'\d{3,5}?', s) == ['012', '345']
assert grep(r'\d?',      s) == ['0','1','2','3','4','5']
assert grep(r'\d??',     s) == ''
assert grep(r'\d+',      s) == '012345'
assert grep(r'\d+?',     s) == ['0','1','2','3','4','5']
assert grep(r'\d*',      s) == '012345'
assert grep(r'\d*?',     s) == ''

################################################################################
# Compilation Flags
################################################################################
# (IGNORECASE, (?i)) Case-insensative matching
assert grep('a', 'A') == None
assert grep('a', 'A', re.I) == grep('(?i)a', 'A') == 'A'
assert grep('(?i:a)a','aa aA Aa AA') == ['aa', 'Aa']

# (DOTALL, (?s)) dot matches a newline
s = 'line1\nline2'
assert grep('.*', s)[0] == 'line1'
assert grep('.*', s, re.S) == grep(r'[^..]*', s) == grep(r'[\s\S]*', s) == 'line1\nline2'

# (ASCII, (?a)) Shorthand classes limited to ASCII

# (LOCALE, (?L)) Locale dependent matching

########################################
# (VERBOSE, (?x)) Readable expressions
s = 'jane_doe-valid.email@gmail.us.edu jane_doe-invalid.email@gmailcom'

p = r'\b[\w\.-]+@[\w\.-]+\.([a-zA-Z\.]{2,6})\b'
p_verbose = r'''
            \b
            [\w\.-]+        # email name
            @               # single @ symbol
            [\w\.-]+        # domain name
            \.              # final dot
            [a-zA-Z\.]{2,6} # top level domain
            \b
            '''
assert grep(p, s) == grep(p_verbose, s, re.VERBOSE) == 'jane_doe-valid.email@gmail.us.edu'

########################################
# (MULTILINE, (?m)) Multi-line mode and ^ $ versus \A \Z anchors
s = '''0 9
1 8
2 7
3 6'''

assert grep('^\d', s) == '0'
assert grep('^\d', s, re.M) == ['0','1','2','3']
assert grep('\A\d', s, re.M) == '0'

assert grep('\d$', s) == '6'
assert grep('\d$', s, re.M) == ['9','8','7','6']
assert grep('\d\Z', s, re.M) == '6'

################################################################################
# Capturing groups
################################################################################
match = re.search(r'(a)b','ab ')
assert match.group() == match.group(0) == 'ab'
assert match.group(1) == 'a'
assert match.group(0,1) == ('ab','a')
assert match.group(1,0,1) == ('a','ab','a')
match = re.search(r'((a)((b)c))d','abcd')
assert match.group(0,1,2,3,4) == ('abcd', 'abc', 'a', 'bc', 'b')

# Backreferences
assert grep(r'(\w)\1', 'ab bb') == 'bb'
assert grep(r'\w{2}',  'ab bb') == ['ab', 'bb']

################################################################################
# Non-capturing groups (?:...) (?=...) (?!...) (?<=...) (?<!...)
################################################################################
# (?:...)
assert re.search(r'ca(t)',     'cat').group(1) == 't'
assert re.search(r'c(a)(t)',   'cat').group(1) == 'a'
assert re.search(r'c(?:a)(t)', 'cat').group(1) == 't'

# Lookaheads (?=...) (?!...)
assert grep(r'\w*\.txt','filename.txt') == 'filename.txt'
assert grep(r'\w*(?=\.txt)','filename.txt') == 'filename'
assert grep(r'12(?:3)(.)\1','12344 1233') == '12344'
assert grep(r'12(?=3)(.)\1','12344 1233') == '1233'

assert grep(r'file\.\w*'       , 'files file.txt file.csv') == ['file.txt', 'file.csv']
assert grep(r'file\.(?!txt)\w*', 'files file.txt file.csv') == 'file.csv'

# Lookbehinds (?<=...) (?<!...)
assert grep(r'abc\d','123abc1abc2') == ['abc1','abc2']
assert grep(r'(?<=123)abc\d','123abc1abc2') == 'abc1'
assert grep(r'(?<!123)abc\d','123abc1abc2') == 'abc2'

# Conditionals (?(id/name)yes-pattern|no-pattern)
pattern = r'(True)?.*(?(1)this|that)'
m = re.search(pattern, "if True, then this")
assert m.group() == 'True, then this'
assert m.groups() == ('True',)
m = re.search(pattern, "else, that")
assert m.group() == 'else, that'
assert m.groups() == (None,)

# Comments (?#...) - python flavor specific
assert grep('123', '01234') == '123'
assert grep('12(?#ignored comment)3', '01234') == '123'

# Named groups (?P<...>...) - python flavor specific
match = re.search('(?P<key>value)','value')
assert match.group('key') == match.group(1) == 'value'
match = re.search('(?P<x>\w)(?P=x)','ab aa')
assert match.group() == 'aa'
assert match.group('x') == match.group(1) == 'a'

################################################################################
################################################################################
# Python specific tools
################################################################################
################################################################################
# Compilation flags
assert re.I == re.IGNORECASE == 2**1
assert re.L == re.LOCALE     == 2**2
assert re.M == re.MULTILINE  == 2**3
assert re.S == re.DOTALL     == 2**4
assert re.compile('').flags  == 2**5 # default
assert re.X == re.VERBOSE    == 2**6
assert         re.DEBUG      == 2**7
assert re.A == re.ASCII      == 2**8

################################################################################
# search vs match vs fullmatch
assert re.search(   '123', '123').group() == '123'
assert re.match(    '123', '123').group() == '123'
assert re.fullmatch('123', '123').group() == '123'

assert re.search(   '12',  '123').group() == '12'
assert re.match(    '12',  '123').group() == '12'
assert re.fullmatch('12',  '123') == None

assert re.search(   '2',   '123').group() == '2'
assert re.match(    '2',   '123') == None
assert re.fullmatch('2',   '123') == None

################################################################################
# search vs findall vs finditer
## without groups
s = '1A 1B 1C'
pattern = '1\w'
assert re.search(pattern, s).group() == '1A'
assert re.findall(pattern, s) == [m.group() for m in re.finditer(pattern, s)] == ['1A','1B','1C']

## with 1 group
pattern = '1(\w)'
assert re.search(pattern, s).groups() == ('A',)
assert re.findall(pattern, s) == ['A','B','C']
assert [m.groups() for m in re.finditer(pattern, s)] == [('A',),('B',),('C',)]

## with 2+ groups
pattern = '(1)(\w)'
assert re.search(pattern, s).groups() == ('1','A')
assert re.findall(pattern, s) == [m.groups() for m in re.finditer(pattern, s)] == [('1','A'),('1','B'),('1','C')]

################################################################################
# re.split()
s = '1Aa 2Bb 3Cc'
assert s.split(' ') == re.split(' ',s)
assert re.split(r'[0-9]', s) == ['','Aa ','Bb ','Cc']
assert re.split(r'[0-9]', s, maxsplit=2) == ['','Aa ','Bb 3Cc']
## groups
assert re.split(r'[A-Z][a-z]', s) == ['1',' 2',' 3','']
assert re.split(r'([A-Z])[a-z]', s) == ['1','A',' 2','B',' 3','C','']
assert re.split(r'([A-Z])([a-z])', s) == ['1','A','a',' 2','B','b',' 3','C','c','']
assert re.split(r'([A-Z][a-z])', s) == ['1','Aa',' 2','Bb',' 3','Cc','']

################################################################################
# re.sub() and re.subn()
s = 'abcABC123'
assert re.sub('3', '-', s) == s.replace('3','-') == 'abcABC12-'
assert re.sub('\d', '-', s) == 'abcABC---'
assert re.sub('\d*', '-', s) == '-a-b-c-A-B-C--'
assert re.sub('\d', '-', s, count=2) == 'abcABC--3'
assert re.sub('(\d)(\d)', r'\2\1', s) == 'abcABC213'
def func(m):
    if m.lastindex == 2:
        return m.group(2) + m.group(1)
    elif m.lastindex == 1:
        return m.group(1)*2
    return '-'
assert re.sub('(\d)(\d)?', func, s) == 'abcABC2133'

assert re.subn('\d','-','123abc')[0] == re.sub('\d','-','123abc')
assert re.subn('\d','-','123abc')[1] == 3
################################################################################
# re.Pattern
s = 'abc 1A2'
pattern = r'a((b)(c)) (?P<key1>1(?P<key1A>A))(?P<key2>2)'
p = re.compile(pattern)
assert p.pattern    == pattern
assert p.groups     == 6 == pattern.count('(')
assert p.groupindex == {'key1': 4, 'key1A': 5, 'key2': 6}
assert p.flags      == 2**5 # default

# Remaining functions mostly identical to module level (e.g. re.search).
# However, they do allow for additional start and end position restrictions
# p.search()
# p.match()
# p.fullmatch()
# p.findall()
# p.finditer()
# p.split()
# p.sub()
# p.subn()

################################################################################
# re.Match
s = '012345'
pattern = '1\d{2,3}'
m = re.search(pattern,s)
assert m.string == s
assert m.re == re.compile(pattern)
assert m.group() == '1234'
assert m.end() == 5
assert m.start() == 1
assert m.span() == (m.start(), m.end())

p = re.compile(pattern)
m = p.search(s,1,4)
assert m.group() == '123'
assert m.pos     == 1
assert m.endpos  == 4

s = 'abc 1A2'
pattern = r'a((b)(c)) (?P<key1A>1(?P<keyA>A))(?P<key2>2)'
m = re.search(pattern,s)
assert m.group()     == 'abc 1A2'
assert m.groups() == tuple(m[i] for i in range(1, 7)) == ('bc', 'b', 'c', '1A', 'A', '2')
assert m.groupdict() == {'key1A': '1A', 'keyA': 'A', 'key2': '2'}
assert m.lastgroup == 'key2'
assert m.lastindex == 6
assert m.re.groupindex[m.lastgroup] == m.lastindex
assert m.expand(r'\1 \2 \3 \4 \5 \6') == " ".join(m.groups())
assert m.expand(r'\g<1> \g<2> \g<3> \g<4> \g<5> \g<6>') == " ".join(m.groups())
assert m.expand(r'\g<key1A> \g<keyA> \g<key2>') == " ".join(m.groupdict().values())

################################################################################
print()

