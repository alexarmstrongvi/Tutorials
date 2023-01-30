#!/usr/bin/env bash

# see https://www.grymoire.com/Unix/Regular.html

echo "Running 01 Regular Expressions (RegEx) basics"

echo "(1) Match this" | grep 'this'

# Backreference
echo "(2) Match aa and bb but not ab" | grep "\([a-z]\)\1" 
echo "(3) Match the 5-letter pallendromes : radar and kayak" | grep "\([a-z]\)\([a-z]\)[a-z]\2\1"

lower="abcdefghijklmnopqrstuvwxyz"
upper="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digit="0123456789"
punct_for_echo="\!\"#$%&'()*+,-./:;<=>?@[\\]^_\`{|}~"
punct_for_printf="\!\"#$%%&'()*+,-./:;<=>?@[\\]^_\`{|}~"
space=' \t\r\n\v\f'
# [[:lower:]]
# [[:upper:]]
# [[:alpha:]]
# [[:digit:]]
# [[:xdigit:]]
# [[:alnum:]]
# [[:word:]]
# [[:punct:]]
# [[:blank:]]
# [[:space:]]

# [[:cntrl:]]
# [[:ascii:]]
# [[:print:]]
# [[:graph:]]

# Regex comparison [ A =~ B ]
