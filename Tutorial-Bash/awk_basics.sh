#!/usr/bin/env bash

# see https://catonmat.net/awk-one-liners-explained-part-one
# see https://www.grymoire.com/Unix/Awk.html#uh-13
# see http://tuxgraphics.org/~guido/scripts/awk-one-liner.html

echo "Running AWK basics"
# AWK is about looping through lines in a text stream and
# (1) parsing the text into columns according to delimeter
# (2) matching specific lines according to pattern
# (3) performing action(s) on the line
# (4) printing an output

################################################################################
# Basic match and act : sed 'pattern {actions}'
################################################################################
# Print all lines; No pattern defaults to matching all lines
# $0 is a variable storing the line of text
echo "(1) Print this" | awk '{print $0}'
# 'print' cmd with no inputs defaults to 'print $0'
echo "(2) Print this" | awk '{print}'
# Print custom message instead of line
echo "(3) Dont print this" | awk '{print "(3) Print this"}'
# Concatenation
echo "(4)" | awk '{print "(4)" " Print " "th" "is","and","this"}'

# Multiple actions per line
## Multiple action statements per {}-group
echo "(4) Print this with an extra space after" | awk '{print; print ""}'
## Mutiple {}-groups per awk line
echo "(5) Print this with an extra space after" | awk '{print} {print ""}'
## Multiple awk-lines (separated by ;)
echo "(6) Print this with an extra space after" | awk '{print}; {print ""}'
# Combine it all
echo "(7) Print multiple things per line" | awk '{print "(7)\nLine 1"}; {print "Line 2"; print "Line 3"} {print "Line 4"}'

# Built-in variables
## Positional variables
echo "(8) Field2 F3 F4 F5" | awk '{print $1,$4,$3,$2,$5}'
## FS - Field Separator / delimator
echo "(9)|New|field|separator" | awk -F "|" '{print $1,"FS = \""FS"\""}'
## OFS - Output Field Separator (the output delimiter)
echo "(9)|New|field|separator" | awk -F "|" '{OFS=" : "; print $1,"OFS = \""OFS"\""}'
## BEGIN - execute before processing any lines
echo "(10) Print this" | awk 'BEGIN {print "(10) Print this first"}; {print}'
## END - execute after processing all lines
echo "(11) Print this" | awk '{print}; END {print "(11) Print this last"}'
## RS - Record Separator variable (i.e. the text the indicates a new line)
echo "(11) Separate sentences. Not at \n" | awk 'BEGIN {RS="."}; {print}'
## ORS - Output Record Separator variable (i.e. the text appended to each print statement. Defaults to '\n')
echo "(12) Print this" | awk 'BEGIN {ORS=" (ORS) "}; {print; print "Print this on the same line"}'; echo
## NF - Number of Fields
echo "(13) Print this" | awk '{print $0 " (NF = " NF "; $NF = " $NF ")"}'
## NR - Number of Record; Increments over all files
echo -e "(14) Print this\n Print this too" | awk '{print $0 " - Line " NR}'
## FNR - File NumbeR; Restarts for each file
echo -e "(15) Print this\n Print this too" | awk '{print $0 " - Line " FNR}'

################################################################################
# Print all lines; No actions defaults to {print}. pattern=1 -> always true
echo "(5) Print this text" | awk '1'
# Print all lines matching regexp
echo -e "(6) Print this text \nNot this line" | awk '/Print/'
# Multiple patterns and actions per line (use ; to seperate pattern-action pairs)
echo "(7) Print this with an extra space after" | awk '1; {print ""}'

################################################################################
echo "
Line 2  : A1 A2 A3 A4
Line 3  : B1 B2 B3 B4
Line 4  : C1 C2 C3 C4
Line 5  : D1 D2 D3 D4
Line 6  : E1 E2 E3 E4
Line 7  : F1 F2 F3 F4
Line 8  : G1 G2 G3 G4
Line 9  : H1 H2 H3 H4
Line 10 : I1 I2 I3 I4
" >> test_file.txt

awk 'BEGIN {print "(X)"}; / [2-4] / {print $0 " FNR = " FNR "; NR = " NR}' test_file.txt test_file.txt

rm test_file.txt

################################################################################
# Math and logic
################################################################################
# PEMDAS - Mod is done before addition and subtraction
awk 'BEGIN {print "(X) 1 = " 2 ^ 2 / (2 * 4) - 1.5 + 5 % 3}'
# Number concatenation - comes after math
awk 'BEGIN {print "(X) 63 = " (1 + 5 2) + 1}'

# Relational operators
# Arithmatic comparisons
awk 'BEGIN {print "(X) true = " (2 == 2) "; false = " (2 != 2)}'
# String comparisons
awk 'BEGIN {print "(X) true = " (string ~ string) "; false = " (string !~ string)}'
# And / Or / Not
awk 'BEGIN {print "(X) true = " ((1 && 0) || !0)}'

