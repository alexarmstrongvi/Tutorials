# see https://www.shell-tips.com/bash/math-arithmetic-calculation/

echo "Running math basics"
################################################################################
# Math with magic numbers
################################################################################
# expr - deprecated
echo "(1) 1 + 1 = $(expr 1 + 1)"
# $(( )) - Arithmetic Expansion
echo "(2) Numberical constant interpretation"
echo -e "\tDecimal (default) =" $((255))
echo -e "\tOctal (0N) =" $((0377))
echo -e "\tHexadecimal (0xN) =" $((0xff))
echo -e "\tCustom (B#N) =" $((8#377)) # Same as octal
echo -e "\tCustom (B#N) =" $((2#011111111))

echo "(3) math operations"
echo -e "\t5 + 2 =" $((5 + 2))
echo -e "\t5 - 2 =" $((5 - 2))
echo -e "\t5 * 2 =" $((5 * 2))
echo -e "\t5 / 2 =" $((5 / 2))
echo -e "\t5 ^ 2 =" $((5 ** 2))
echo -e "\t5 % 2 =" $((5 % 2))

echo "(4) bit operations"
echo -e "\t0b10 =" $((2#10))
echo -e "\t2 << 2 =" $((2 << 2))
echo -e "\t8 >> 2 =" $((8 >> 2))
echo -e "\t~2 =" $((!2))

echo "(5) logical operations"
echo -e "\t!0 = $((!0)); !1 = $((!1)); !2 = $((!2)); !1.5 = invalid"
echo -e "\t1 && 0 =" $((1 && 0))
echo -e "\t1 || 0 =" $((1 || 0))

################################################################################
# Using variables
################################################################################
# Quotes don't really matter for assignment; all bash variables are strings
x=5
y="2"
# Set before evaluation
z1=x+y # treats x+y as "x+y"
# Set after evaluation
let z2=x+y
declare -i z3=x+y
z4=$((x+y))
echo "(4) [x, y, z1, z2, z3, z4] = [$x, $y, $z1, $z2, $z3, $z4] = [$((x)), $((y)), $((z1)), $((z2)), $((z3)), $((z4))]"

z=$((x+y))
echo "(6)"
echo -e "\tz = $z"
echo -e "\tz++ = $((z++)) but for future evaluations z = $z"
echo -e "\tz-- = $((z--)) but for future evaluations z = $z"
echo -e "\t++z =" $((++z))
echo -e "\t--z =" $((--z))
echo -e "\tz+=2 =" $((z+=2))
echo -e "\tz-=2 =" $((z-=2))
echo -e "\tz*=2 =" $((z*=2))
echo -e "\tz/=2 =" $((z/=2))

################################################################################
# Floating point math 
################################################################################
# Bash has not built-in capabilities for floating point arithmatic
# so other tools must be used, mainly 'bc'

# Use -l option for full precision
printf "(7) 3/2 = "; echo "3/2" | bc -l

# Example of printing percentages
nCurrent=20
nTotal=30
printf "(8) [$nCurrent/$nTotal] = %.2f%% complete\n" "$(echo "${nCurrent}/${nTotal} * 100" | bc -l)"


################################################################################
# Other
################################################################################
# factor (non-standard)
# gfactor 60
