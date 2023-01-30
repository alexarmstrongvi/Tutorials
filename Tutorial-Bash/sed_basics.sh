#!/usr/bin/env bash
# see https://www.grymoire.com/Unix/Sed.html
# see https://catonmat.net/sed-one-liners-explained-part-one
# gsed used when sed will not work

echo "Running Stream EDitor (SED) basics"

################################################################################
# Basic find and apply commands : print, delete, quit
################################################################################
# WARNING : this will print all lines and print again those that match
echo -e "(01) Print this line\n But not THIS line" | sed '/this/ p'
# Only print lines that match
echo -e "(02) Print this line\n But not THIS line" | sed -n '/this/ p'

# find and delete
echo -e "(03) Print this line\n Delete this line" | sed '/Delete/ d'

# find and delete
echo -e "(04) Print this line\n Quit before this line" | sed '/Print/ q'

# WARNING : doesn't work on Mac OSX
echo "(05) Ignore CASE" | gsed -n '/case/I p'

################################################################################
# Basic substituion
################################################################################
# Piping to sed or reading in file
echo "(06) Change day into night" | sed 's/day/night/'
echo "(07) Change day into night" > tmp.txt
sed 's/day/night/' tmp.txt
rm tmp.txt

# Replacing multiple occurances (g)
# WARNING: Will only replace first occurance
echo "(08) Change day and day into night" | sed 's/day/night/' 
echo "(09) Change day and day into night" | sed 's/day/night/g'

# Using different delimeters (/ -> |)
echo "(10) Change /path/to/day/ into /path/from/night/" | sed 's|/to/day|/from/night|'

# Using matched string (&)
echo "(11) Change day into night" | sed 's/day/night (was &)/'

# Targeting a specific match (1 through 512)
echo "(12) A1 A2 A3 A4 A5 A6 A7 A8 A9 A10 A11" | sed 's/A/B/10'

################################################################################
# Regular expressions
################################################################################
echo "(13) 321 abc" | sed "s/3[1-5]*/___/"

# Extended regular expressions (-E for MacOSX, -r or -E for Linux)
echo "(14) 321 abc" | sed "s/3[1-5]{2}/___/" # Wont work
echo "(15) 321 abc" | sed -E "s/3[1-5]{2}/___/"

################################################################################
# Address and text ranges
################################################################################
echo "
Line 2 : A
Line 3 : B
Line 4 : C
Line 5 : D
Line 6 : E
Line 7 : C
Line 8 : D
Line 9 : E
" > test_file.txt

# Search a specific line number
printf "(16) "; sed -n '2 s/[A-D]/Z/ p' test_file.txt

# Search a specific range of line numbers
echo "(17) "; sed -n '3,5 s/[A-D]/Z/ p' test_file.txt
echo "(18) "; sed -n '3,$ s/[A-D]/Z/ p' test_file.txt

# Search only lines matching a pattern
printf "(19) "; sed -n '/B/ s/[A-D]/Z/ p' test_file.txt

# Search only lines between two points
echo "(20) "; sed -n '6,/D/ s/[A-D]/Z/ p' test_file.txt

rm test_file.txt
################################################################################
# Other
################################################################################
# Multiple commands
echo "(22) This and that" | sed -e 's/This/That/' -e 's/that/this/'

# Writing to file (/w)

# Negate command (!)
