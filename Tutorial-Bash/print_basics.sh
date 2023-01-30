#!/usr/bin/env bash

################################################################################
# echo - its stupid and simple
################################################################################
echo Hello world
echo Hello \t World # \ treated as multi line
echo "Hello \t World" # does not interpret
echo -e "Hello \t World" # does interpret

################################################################################
# printf
################################################################################
# Basic print
printf "(X) Hello world\n"
# Ignores additional inputs
printf "(X) Hello world\n" "Ignore this"
# Concatenates everything up to first unquoted space or end of line
printf "(X) ""Hello ""world. "This" is the number "123"\n" "Ignore this"

########################################
# Specifiers

# Strings
# Formating strings with specifiers
printf "(X) %s\n" "Hello world"
# Format specifier applied to each argument
printf "(X) %s\n" "Hello" "world"
# Multiple specifiers look for multiple arguments 
printf "(X) %s. This is %s\n" "Hello" "world" "Hi" "program"
# Specifier set to empty string if no arguments left
printf "(X) %s %s.\n" "Hello" "world" "Hi"
# b - like s but it interprets escape characters
printf "(X) Print tab \'%s\'. Interpret tab \'%b\'.\n" "\t" "\t"

# Integers
printf "(X) %d %i %o %u %X %x\n" -255 -255 0377 255 0xFF 0xff
# Passing negative argument to unsigned int wraps around
printf "(X) Max uint (dec) = %u\n" -1
printf "(X) Max uint (oct) = %o\n" -1
printf "(X) Max uint (hex) = %x\n" -1
# Base conversions
printf "(X) %x (hex) -> %d (dec) -> %o (oct)\n" 0xff 0xff 0xff
# Math expressions will not be evaluated during substitution
#printf "(X) %d\n" 1+1
# Formatting
# Leave space for or forcing sign
printf "(X) |% d|% d|%+d|%+d|\n" 1 -1 1 -1
# Padding (only space or zero padding available?)
printf "(X) |%3d|%03d|%-3d|\n" 1 1 1
# Combine (- overrides 0; + overides " ")
printf "(X) |% -5d|%+05d|\n" 1 1

# Floats
printf "(X) f = %f\n" 123456789.123456789
printf "(X) e = %e\n" 1.23456789e-8
printf "(X) g = %g or %g\n" 1.23456e+5 1234567.89
# Capitals are the same except for built-in text values (NaN and inf)
printf "(X) [f,F,e,E,g,G] = [%f,%F,%e,%E,%g,%G]\n" iNf iNf iNf iNf iNf iNf
printf "(X) [f,F,e,E,g,G] = [%f,%F,%e,%E,%g,%G]\n" NaN NaN NaN NaN NaN NaN
#Formatting
# Leave space for or forcing sign
printf "(X) |% f|% f|%+f|%+f|\n" 1.5 -1.5 1.5 -1.5
# Padding (only space or zero padding available?)
printf "(X) |%10f|%010f|%-10f|\n" 1.5 1.5 1.5
# Precision
printf "(X) |%10.2f|%010.2f|%-10.2f|\n" 1.559 1.559 1.559


