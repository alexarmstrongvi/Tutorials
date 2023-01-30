#!/usr/bin/env bash
################################################################################
# String manipulation
#
# I find the syntax to be very sensative to bash version
################################################################################

echo "Running $(which bash) (v$BASH_VERSION)"

# see https://www.gnu.org/software/bash/manual/bash.html#Shell-Parameter-Expansion 

################################################################################
# Variable expansion
################################################################################
string=0123456789
printf "(X) string = %10s\n" "${string}"
# Use string from index 4 onward (python string[4:])
printf "(X) string = %10s\n" "${string: 4}"
# Use string from index N-4 onward (python string[-4:])
printf "(X) string = %10s\n" "${string: -4}"
# Use string from index 4 to index 4+4 (python string[4:8])
printf "(X) string = %8s\n" "${string: 4: 4}"
# Use string from index N-4 to index N-4+3 (python string[-4:-1]
printf "(X) string = %9s\n" "${string: -4:3}"
# Use string from index 4 to index N-4 (python string[4:-4])
# - Only possible in some bash versions
printf "(X) string = %6s\n" "${string: 4:-4}"
# Use string from index N-4 to index N-3 (python string[-4:-3])
# - Only possible in some bash versions
printf "(X) string = %7s\n" "${string: -4:-3}"
echo

################################################################################
# Array expansion
################################################################################
array=(0 1 2 3 4 5 6 7 8 9)
# Print specific array element
echo "(X) array = ${array}" # defaults to index=0
echo "(X) array = ${array[0]}"
# Print entire array
# Note: '*' or '@' only differ in expanding inside double quotes.
#       '*' expands to a single string while '@' expands to separate strings.
#       This is useful for looping over expansion
n=$(for x in "${array[*]}"; do echo $x; done | wc -l)
echo "(X) array = ${array[*]} (n = ${n})"
n=$(for x in "${array[@]}"; do echo $x; done | wc -l)
echo "(X) array = ${array[@]} (n = ${n})"
# Print indexes with !. Happen to match the values in this case
echo "(X) array = ${!array[@]}" 
echo "(X) array = ${!array[*]}"
# Print subset of array
echo "(X) array = ${array[@]: 4:4}"
#echo "(X) array = ${array[@]: 4:-4}" # negative length not allowed
echo "(X) array = ${array[@]: -4:3}"
#echo "(X) array = ${array[@]: -4:-3}" # negative length not allowed
echo

################################################################################
# Associative array expansion
################################################################################
declare -A map=([a]=1 [b]=2 [c]=3 [d]=4)
# Values
echo "(X) map = ${map[*]}"
echo "(X) map = ${map[@]}"
# Keys
echo "(X) map = ${!map[*]}"
echo "(X) map = ${!map[@]}"

################################################################################
# Positional argument expansion
################################################################################
# Aside : how to manually set the positional bash argument variables with 'set'
set -- 01234 2 3 4 5 6 7 8 9
echo "args \$1 = $1; \$@ = ${@}"

echo "(X) Parse a single argument : ${1:3}"
echo "(X) Select subset of args   : ${@: 4:4}"
#echo "(X) Select subset of args   : ${@: 4:-4}" # negative length not allowed
echo "(X) Select subset of args   : ${@: -4:3}"
#echo "(X) Select subset of args   : ${@: -4:-3}" # negative length not allowed
echo


################################################################################
# Special variable properties 
################################################################################
echo "(X) Length of string : ${#string}"
echo "(X) Length of array : ${#array[@]}"
echo "(X) Length of map : ${#map[@]}"
echo "(X) Number of positional args : ${#*}"
echo "(X) Number of positional args : ${#@}"
echo

# Select substring

# Remove substring from beginning
printf "(X) string = %10s\n" ${string#01234}
printf "(X) string = %10s\n" ${string#*[3-5]} # One '#' looks for shortest match
printf "(X) string = %10s\n" ${string##*[3-5]} # Two '#' looks for longest match
# Remove substring from end
echo "(X) string = ${string%56789}"
echo "(X) string = ${string%[5-7]*}" # One '%' looks for shortest match
echo "(X) string = ${string%%[5-7]*]}" # Two '%' looks for longest match
# Remove substring from anywhere
echo "(X) string = ${string/456}"
echo "(X) string = ${string/[4-6]}"
echo "(X) string = ${string//[4-6]}"
echo "(X) string = ${string/[4-6]*}"
echo "(X) string = ${string/*[4-6]}"
# Replace string
echo "(X) string = ${string/456/___}"
echo "(X) string = ${string//[257]/_}"

# Change case
string2=abcdefghi
echo "(X) string = ${string2^[afi]}"
echo "(X) string = ${string2^^[afi]}"
string3=ABCDEFGHI
echo "(X) string = ${string3,[AFI]}"
echo "(X) string = ${string3,,[AFI]}"

echo "(X) Print all bash environment vars : ${!BASH*}"
echo "(X) Print all bash environment vars : ${!BASH@}" 

