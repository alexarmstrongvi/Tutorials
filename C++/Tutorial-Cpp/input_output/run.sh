#!/usr/bin/env bash
clang++ \
    -Wall -Wextra -Wpedantic \
    -Werror \
    -pedantic-errors \
    -std=c++17 \
    -stdlib=libc++ \
    input_output.cxx

if [ $? -eq 0 ]; then
    printf "====== RUNNING ======\n"
    ./a.out
    printf "\nINFO :: Remove outputs: `rm a.out test_output_file*txt\n`"
    printf "\n====== DONE ======\n"
else
    printf "\n====== FAILED ======\n"
fi
