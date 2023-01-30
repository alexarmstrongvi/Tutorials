#!/usr/bin/env bash
################################################################################
# Baby steps
################################################################################
# pwd, ls, cd, mkdir, mv, cp, rm, touch

# less

# wc

########################################
echo "===== seq ====="
seq 3
# Print on a single line
seq -s " " -t '\n' 10
# define start, stop, and step size
seq -s " " -t '\n' 0 2 10
# countdown and negatives
seq -s " " -t '\n' 10 -2 -10
# Consistent width
seq -s " " -t '\n' -w 10 -2 -10
# Decimals
seq -s " " -t '\n' 0 0.3 1
echo

echo "===== jot ====="
# Like seq but more features (e.g. random numbers)
# see https://www.networkworld.com/article/3200222/what-the-jot-command-can-do-for-you.html
jot 3
jot -s " " 3
jot -s " " 3 5
jot -s " " 3 5 15
jot -s "" -c - 33 127
jot -s " " -r 10 0 10 1
echo

# rename

################################################################################
# System stuff
################################################################################

# chmod, chown

# du
#du -d 1
#du -h -d 1
#du -h -d 0 */

# file - determine file type

# time
echo "===== time ====="
#time for x in $(seq 100000); do printf ""; done;
echo

################################################################################
# I/O
################################################################################
# read

# readarray / mapfile
# readarray -t array

################################################################################
# Text/File processing
################################################################################
# cat, head, tail
# expand - replace tabs with spaces

########################################
echo "===== tr (translate) ====="
string="abc 123   ABC 123"
# Translate all instances of a single character
echo "$string" | tr '1' '7'
# Translate all instances from a set of characters
echo "$string" | tr '1aA' '7xX' # substitutions must line up
# Translate everything except for a set of characters
echo "$string" | tr -C '1Aa\n' '_' # Remember to add \n so newlines don't get removed
# Delete all characters from a set
echo "$string" | tr -d '1Aa'
# Translate all characters falling in a certain range
echo "$string" | tr '1-3' '7' # substitutions must line up
# Translate all instances of a character class
echo "$string" | tr '[:digit:]' '#'
# Translate upper to lower case
echo "$string" | tr '[:upper:]' '[:lower:]'
# Reduce ("squeeze") duplicate characters to a single character
echo "$string" | tr -s ' '

########################################
# sort

########################################
# uniq

########################################
echo "===== rs (reshape) ====="
seq 50 | rs
seq 9 | rs 3
seq 9 | rs 3 2
# rs -T
echo

########################################
echo "===== column ====="
# BSD column ignores empty entries between delimiters so add a space
echo "
 ,ColumnA,ColumnB,ColumnC
Row1, ,,C1
Row2, ,B2, " | column -t -s ","
echo
# gcolumn = GNU column (non-default for MacOSX)
echo "
,ColumnA,ColumnB,ColumnC
Row1,,,C1
Row2,,B2," | gcolumn -t -s "," -o " | "
echo

########################################
echo "===== cut ====="
echo "12345" | cut -c 1,3-5
echo "1,2,3,4,5" | cut -d ',' -f 1,3-5
echo

########################################
#echo "===== tac and rev ====="

########################################
#echo "===== paste ====="
# paste
# paste - - -
# paste -s
# paste -d ","


########################################
#echo "===== join ====="

########################################
echo "===== cmp ====="
echo "test" > tmp1.txt
echo "test" > tmp2.txt
# Confirm that files are the same
if cmp -s tmp1.txt tmp2.txt; then echo "Same"; else echo "Different"; fi
echo "test2" > tmp2.txt
# Confirm that files are different
if cmp -s tmp1.txt tmp2.txt; then echo "Same"; else echo "Different"; fi
rm tmp1.txt tmp2.txt
echo

########################################
echo "===== diff ====="
# One delete, change, and add
printf "1\n2\n3\n3\n5\n" > tmp1.txt
printf "2\n3\n4\n5\n6\n" > tmp2.txt
# Minimal diff
diff -q tmp1.txt tmp2.txt
printf "\nSimple diff\n"
diff tmp1.txt tmp2.txt # Same as diff --normal
#printf "\nRCS diff\n"
#diff -n tmp1.txt tmp2.txt
printf "\nContext diff\n"
diff -c tmp1.txt tmp2.txt
printf "\nUnified diff\n"
diff -u tmp1.txt tmp2.txt
#printf "\nColumn diff\n"
#diff -y tmp1.txt tmp2.txt
#printf "\ned script diff\n"
#diff -e tmp1.txt tmp2.txt
rm tmp1.txt tmp2.txt
printf "\nDirectory diff\n"
mkdir dir1 dir2
cd dir1
mkdir file1.txt file2.txt
cd ../dir2
mkdir file2.txt file3.txt
cd ..
diff dir1/ dir2/
rm -rf dir1 dir2
echo
# diff *.txt --to-file=compare_to_this.txt

########################################
echo "===== comm ====="
printf "Only 1\nShared\n" > tmp1.txt
printf "Only 2\nShared\n" > tmp2.txt
echo "Full comparison"
comm tmp1.txt tmp2.txt
echo "Unique to file 1"
printf "\t"; comm -23 tmp1.txt tmp2.txt
echo "Unique to file 2"
printf "\t"; comm -13 tmp1.txt tmp2.txt
echo "Shared by both files"
printf "\t"; comm -12 tmp1.txt tmp2.txt
rm tmp1.txt tmp2.txt

########################################
#echo "===== xargs ====="
# blah | xargs echo
# blah | xargs -t echo
# blah | xargs -I{} echo {}

########################################
# tar
