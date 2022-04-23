#===============================================================================
"UTF-8 is a variable-width character encoding used for electronic communication.
Defined by the Unicode Standard, the name is derived from Unicode (or Universal
Coded Character Set) Transformation Format – 8-bit."

"Unicode, formally the Unicode Standard, is an information technology standard
for the consistent encoding, representation, and handling of text expressed in
most of the world's writing systems. The standard, which is maintained by the
Unicode Consortium, defines 144,697 characters[1][2] covering 159 modern and
historic scripts, as well as symbols, emoji, and non-visual control and
formatting codes."

- Wikipedia

# References
    * https://docs.julialang.org/en/v1/manual/unicode-input/
===============================================================================#
import Unicode

# Raw String
@assert( raw"\u41" == "\\u41" )
# String
@assert( "A" == "\u41" == "\u0041" == "\x41" )
@assert( "π" == "\u3c0" == "\u03c0" != "\x3c0" == "\x3c"*"0")
# Char
@assert( 'A' == '\u41' == '\u0041' == '\x41' )
@assert( 'π' == '\u3c0' == '\u03c0') # '\x3c0' is invalid
# Integer
@assert (0x41 == 65 == 0o101 == 0b1000001)

# Conversions
r, s, c, i = raw"\u3c0", "π", 'π', 0x3c0
@assert( i == UInt(c) )
@assert( c == Char(i) )
@assert( c == only(s) )
@assert( s == unescape_string(r) )
@assert( s == string(c) )
@assert( r == raw"\u" * string(i, base=16) )

# char   -> uint   : i == UInt(c)
# string -> uint   : -> char
# raw    -> uint   : -> string -> char

# uint   -> char   : c == Char(i)
# string -> char   : c == only(s)
# raw    -> char   : -> string

# raw    -> string : s == unescape_string(r)
# char   -> string : s == string(c)
# uint   -> string : -> char

# uint   -> raw    : r == raw"\u" * string(i, base=16)
# char   -> raw    : -> uint
# string -> raw    : -> char -> uint

#===============================================================================
8-bit
ASCII character codes
    * Control characters: 0x0000 - 0x0020 [0 - 32], 0x007F [127]
    * Non-control characters: 0x0021 - 0x007E [33 - 126]

16-bit
"almost all Latin-script alphabets, and also IPA extensions, Greek,
Cyrillic, Coptic, Armenian, Hebrew, Arabic, Syriac, Thaana and N'Ko alphabets,
as well as Combining Diacritical Marks" -Wikipedia

24-bit
"the rest of the Basic Multilingual Plane...including most Chinese,
Japanese and Korean characters" -Wikipedia

32-bit
"less common CJK characters, various historic scripts, mathematical symbols, and
emoji"
=# 
ascii           = '\x00':'\x7f'
digits          = collect('0':'9')
ascii_uppercase = collect('A':'Z')
ascii_lowercase = collect('a':'z')
ascii_letters   = vcat(ascii_uppercase, ascii_lowercase)
punctuation     = [c for c in ascii if Base.Unicode.category_abbrev(c)[1] == 'P']
control         = [c for c in ascii if Base.Unicode.category_abbrev(c) == "Cc"]
#whitespace     = 

# Print UTF-8 Table
print("       ")
for ii = 0:15
    print(string(ii, base=16), ' ')
end
print('\n')
for code_point = 0x0000 : 0xffff #0x03ff
    row_start = rem(code_point, 0x10) == 0
    row_end   = rem(code_point+1, 0x10) == 0

    if row_start
        x = lpad(string(code_point ÷ 0x10, base=0x10), 3, '0')
        print("\\u$(x)x ")
    end
    
    char = Char(code_point)
    category = Base.Unicode.category_abbrev(char)
    if !isvalid(char)    
        print('X')
    elseif Unicode.iscntrl(char)
        print(' ')
    elseif category == "Mn" # Mark, nonspacing
        # Can non-spacing character be combined with any other char? No
        # When it can, is the combined char also encoded in UTF-8? Not always
        print("+" * string(char))
    else
        print(char)
    end
    print(' ')
    
    if row_end
        print("\n")
    end
end
println()