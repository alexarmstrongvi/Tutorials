import Unicode

function test_strings()
    ############################################################################
    # Characters
    literals = ('A', 'a' ,'1', 'π', ' ', '\t', '\x3f', '\u3f', '\u003f', '\U10FFFF')
    @assert(typeof('A') == Char)

    # Attributes
    codepoint('A') == 0x41
    codepoint('\U10FFFF') == 0x0010ffff

    # Comparisons and +/- operations applied to the underlying UTF-8 integer
    @assert('A' < 'a' > 'Z')
    @assert('A' + 1 == Char(Int('A') + 1))
    for ii in 0x00:0x7e
        @assert( Char(ii+1)  > Char(ii))
        @assert( Char(ii+1) == Char(ii) + 1)
    end

    # Operations
    'A'^4 == repeat('A', 4) == "AAAA"

    ############################################################################
    # Strings
    ############################################################################

    # Literals
    literals = ("string", "A,B,C", "\t\n\r")
    typeof("string") == String

    # Construction
    string(1.23)   == "1.23"
    string(-5, base=3, pad=5) == "-00012"
    string(62*61, base=62) == "z0"

    # repr()
    # sprintf()
    # show()

    string("AB", 'C', "D") == "ABCD"

    # Triple quoted Strings
    s1 = """Line 1
        Line 2
        Line 3""" 
    s2 = """
    Line1
    Line2
    Line3"""
    s3 = """
Line1
Line2
Line3"""
    s1 == s2 == s3

    # Raw strings (@raw_str)
    raw"X \t\n $var $(1+2) \" \\\" X" == "X \\t\\n \$var \$(1+2) \" \\\" X"

    # Byte strings (@b_str)
    typeof(b"ABC") == CodeUnits{UInt8, String}
    b"Az"       == UInt8[0x41, 0x7a]
    b"\x00\xff" == UInt8[0x00, 0xff]
    b"\U00\u7f" == UInt8[0x00, 0x7f]
    b"\U7ff"    == UInt8[0xdf, 0xbf]             == UInt8[                        0b11011111, 0b10111111]
    b"\Uffff"   == UInt8[0xef, 0xbf, 0xbf]       == UInt8[            0b11101111, 0b10111111, 0b10111111]
    b"\U10FFFF" == UInt8[0xf4, 0x8f, 0xbf, 0xbf] == UInt8[0b11110100, 0b10001111, 0b10111111, 0b10111111]

    # Version strings (@v_str)
    typeof(v"2") == VersionNumber
    v"2" == v"2.0.0"
    v"2-rc1+win64" == v"2.0.0-rc1+win64"
    v"2.0.0-" < v"2.0.0-rc1" < v"2.0.0+"
    v"2.0.0-rc1+win64" < v"2.0.0-rc1+" < v"2.0.0-rc2"

    # Invalid UTF-8 code unit sequences
    length("\xc0\xa0\xe2\x88\xe2|") == 4
    length("\xf7\xbf\xbf\xbf") == 1

    ########################################
    # Attributes
    # length(), ncodeunits(), sizeof()
    length("")  == 0 == ncodeunits("")
    length("A") == 1 == ncodeunits("A")      && 'A' == '\U41'
    length("λ") == 1  < ncodeunits("λ") == 2 && 'λ' == '\U3BB'
    length("∀") == 1  < ncodeunits("∀") == 3 && '∀' == '\U2200'
    length("😄") == 1 < ncodeunits("😄") == 4 && '😄' == '\U1F604'

    ncodeunits("∀") == sizeof('∀') # only differ for custom string types I think

    length("12345", 2, 4) == length("12345"[2:4]) == 3

    # firstindex(), lastindex()
    s = "🧐A∀A🧐"
    0 < length(s) <= ncodeunits(s)
    firstindex(s) == 1
    lastindex(s) > length(s)
    lastindex("Julia") == length("Julia")

    # codeunit()
    codeunit("ABC") == UInt8

    # Unicode.textwidth
    Unicode.textwidth("∀") == 1
    Unicode.textwidth("😄") == 2

    ########################################
    # Slicing/Indexing
    s = "123456789"
    typeof(s[2]) == Char
    typeof(s[2:6]) == String
    typeof(s[2:2]) == String

    s[begin] == s[firstindex(s)] == s[1]
    s[end]   == s[lastindex(s)]
    try s[0]; catch BoundsError; end
    try s[end+1]; catch BoundsError; end

    typeof(s[2])   == Char
    typeof(s[2:4]) == String
    length(s[2:4]) == 4-2 + 1    

    first(s)   === s[1]
    first(s,1) === s[1:1]
    first(s,3) === s[1:3]
    first(s,0) === ""
    # last

    ########################################
    # Indexing
    s = "🧐A∀A🧐"
    # eachindex(), codeunit(), codeunits()
    valid_indexes = [1, 5, 6, 9, 10]
    length(eachindex(s))  == length(s) == length(valid_indexes)
    collect(eachindex(s)) == [nextind(s,0,n) for n in 1:length(s)] == valid_indexes
    length(codeunits(s))  == ncodeunits(s)
    collect(codeunits(s)) == [codeunit(s,n) for n in 1:ncodeunits(s)]

    # prevind/nextind(s, start_idx, n_repeats=1)
    nextind(s,0) == 1
    nextind(s,1) == 1 + ncodeunits(s[1]) == 5
    nextind(s,2) == nextind(s,3) == nextind(s,4) == 5
    nextind(s,lastindex(s)) == ncodeunits(s) + 1
    try nextind(s, ncodeunits(s)+1); catch BoundsError; end
    try nextind(s, -1); catch BoundsError; end

    nextind(s,1,2) == nextind(s,nextind(s,1))
    nextind(s,lastindex(s), 999) == ncodeunits(s) + 999
    nextind(s,5,0) == 5
    nextind(s,0,0) == 0
    try nextind(s,3,0); catch StringIndexError; end

    prevind(s,1) == 0
    prevind(s,2) == 1
    prevind(s,3) == prevind(s,4) == prevind(s,5) == 1
    prevind(s, ncodeunits(s)+1) == lastindex(s)
    try prevind(s, ncodeunits(s)+2); catch BoundsError; end
    try prevind(s, 0); catch BoundsError; end

    prevind(s,6,2) == prevind(s, prevind(s,6))
    prevind(s,1,999) == 1 - 999
    prevind(s,5,0) == 5
    prevind(s, ncodeunits(s)+1, 0) == ncodeunits(s)+1
    try prevind(s, 3, 0); catch StringIndexError; end

    # This ind
    thisind(s,2) === 1

    ########################################
    ## Operations

    # Comparisons
    # == < > isless() 
    # cmp()

    # Concatenation
    x,y,z = "AB", "CD", "12"
    string(x, y, z) == x * y * z == "ABCD12"

    a, b = "\xe2\x88", "\x80"
    a * b == "\xe2\x88\x80" == "\u2200" == "∀"

    # Repetition
    "AB"^4 == repeat("AB", 4) == "ABABABAB"

    # Interpolation
    "$x & $y"  == string(x, " & ", y)   == "AB & CD"
    "A$(1+2)B" == string("A", 1+2, "B") == "A3B"

    # Formatting
    # lpad()
    # rpad()
    # Unicode.uppercase()
    # Unicode.lowercase()
    # Unicode.titlecase()
    # Unicode.uppercasefirst()
    # Unicode.lowercasefirst()
    # escape_string()
    # unescape_string()

    # Finding
    # findall()
    # findfirst()
    # findlast()
    # findnext()
    # findprev()

    # SubStrings
    typeof(SubString("ABC")) == SubString{String}
    SubString("ABCDE", 2, 4) == "BCD"
    chop("123456", head=1, tail=2) == "234"
    strip(" \twhitespace \n") == "whitespace"
    # rstrip(), lstrip()
    chomp("\nLine1\nLine2\n") == "\nLine1\nLine2"

    # Type conversion
    # transcode()

    ascii("ABC") == "ABC"
    try ascii("αβγ"); catch ArgumentError; end

    html"HTML object" # @html_str

    text"Text object" # @text_str

    # Other
    reverse("ABCD") == "DCBD"
    reverse("ax̂e") == "êxa" # be cautious with order sensative unicode
    
    replace("ABCDAB", "AB" => "12", count=1) == "12CDAB"

    split("A B C") == ["A", "B", "C"]
    # rsplit()
    join(["A", "B", "C", "D"], ", ", " and ") == "A, B, C and D"

    ########################################
    # Tests
    isvalid('\uffff')
    # isvalid
    # isascii
    # Unicode.iscntrl
    # Unicode.isdigit
    # Unicode.isletter
    # Unicode.islowercase
    # Unicode.isnumeric
    # Unicode.isprint
    # Unicode.ispunct
    # Unicode.isspace
    # Unicode.isuppercase
    # Unicode.isxdigit

    # startswith()
    # endswith()
    # occursin()
    # contains()

    ########################################
    # Conversions (int, char, string)
    
    ########################################
    # Unsorted
    # unsafe_string

    println("Success")
end

# string formatting
# Underdeveloped right now
# "Support python style f"{x:0.2}"
#   - https://github.com/JuliaIO/Formatting.jl/issues/41
# "How do you format a string when interpolated in Julia?"
#   - https://stackoverflow.com/questions/37031133

import Printf # built in
function test_string_formatting()
    # Standard library
    @Printf.printf "%s World" "Hello"
    s = @Printf.sprintf "%s World" "Hello"

    # 3rd party : Formatting
    # - https://github.com/JuliaIO/Formatting.jl
    # Formatting.printfmt()
    # s = Formatting.fmt()

    # 3rd party : StringLiterals
    # - https://github.com/JuliaString/StringLiterals.jl

end

if abspath(PROGRAM_FILE) == @__FILE__
    #test_strings()
    test_printf()
end

    