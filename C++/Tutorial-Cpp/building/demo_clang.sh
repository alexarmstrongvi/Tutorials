#!/usr/bin/env bash
################################################################################
# NOTES
# * MacOS offers the `clang` command line tool (a.k.a. driver) for building
#   C/C++ source code.
# * MacOS also seems to offer `gcc` builtin but this really just runs clang. The
#   real GNU gcc compiler must be installed.
# * `clang` is a driver that drives the build process, calling the compiler
#   (also called `clang` but a different executable) and linker (`ld`). Use the
#   verbose option (`-v`) to see all the commands run by the driver.
# * If no main function exists in any object files, a compiler error occurs
################################################################################
function assert_success() {
    [ $? -eq 0 ] || echo "FAILED ${1}"
}
function assert_fail() {
    [ $? -ne 0 ] || echo "FAILED ${1}"
}

################################################################################
# Running `clang` without any options just produces an object file with default
# name `a.out`
# echo 'int main() { return 0; }' > myapp.c
#
# clang myapp.c
# ./a.out
# if [ $? -eq 0 ]; then echo PASS; else echo FAILED; fi
# rm a.out
#
# # Specify output file
# # Usually no extension is given to executables
# clang -o my_executable myapp.c
# ./my_executable
# if [ $? -eq 0 ]; then echo PASS; else echo FAILED; fi
# rm my_executable

################################################################################
# Building files that use code from other files requires telling the compiler
# about the other code. C/C++ handles this by specifiying a path to the file
# with the code which is then copied into the current file. This is done using
# the '#include' preprocessing directive. Compilers will search a predefined set
# of paths for the path in the include directive. So providing the absolute path
# is not necessary.
#
# Common paths are the same directory as the source file and system include
# paths (e.g. /usr/lib/). If the included file is not at one of those paths then
# the user must add directories to the search path using the '-I' flag or by
# setting environment variables (e.g. CPLUS_INCLUDE_PATH)
printf 'int add(int x, int y) { return x + y; }' > mylib.c

# Including files using the absolute path
abs_path="$(realpath mylib.c)"
printf "
#include \"${abs_path}\"
int main() { add(3, 4); }
" > myapp.c
clang myapp.c
assert_success

# Including files in the same directory
printf '
#include "mylib.c"
int main() { add(3, 4); }
' > myapp.c
clang myapp.c
assert_success

# Including files using the '-I' flag
mv mylib.c include
clang myapp.c > /dev/null 2>&1
assert_fail
clang -I include myapp.c
assert_success

rm myapp.c include/mylib.c
rm a.out

# Including source files is bad practice and has several downsides:
#   * Large build times because all source code is compiled after any change
#   * Requires users have access to all source code preventing library authors
#   from providing precompiled binaries that
#       * save users from having to configure a build
#       * hide (potentially proprietary) source code from users
#
# The solution in C/C++ is to define header files (.h, .hpp) that specify the
# interfaces provided by source code files.
# This provide the minimal amount of information needed by the compiler to know
# how to compile myapp.c.
printf 'int add(int x, int y) { return x + y; }' > mylib.c
printf 'int add(int x, int y);' > include/mylib.h
printf '
#include "mylib.h"
int main() { add(3, 4); }
' > myapp.c

# Compiling as before will fail because compiler no longer knows about
# implementation of add(...) defined in mylib.h
clang myapp.c > /dev/null 2>&1
assert_fail 
# Need to tell compiler to compile all source code (order doesn't matter). Under
# the hood, each source file is compiled into an object file and then a linker
# will merge everything into the final executable.
clang myapp.c mylib.c -I include/
assert_success

# ASIDE: Modern compiled languages (e.g. Rust) do not use separate header files.
# The use of headers is a historical decision that made sense decades ago when
# computer memory and processing speeds were much more limited (e.g. single pass
# compilation). 

# To avoid recompiling mylib.c when only myapp.c is changing, we can compile
# mylib.c and save the object file to be used for linking.
clang -c mylib.c
clang myapp.c mylib.o -I include/
assert_success

# TODO: Compile against static library (same as object file?)

# TODO: Compile against dynamic library
# suffix convention per OS is .so (Linux), .dylib (MacOS), and .dll (Windows)
clang -shared -fpic mylib.c -o libmylib.dylib
clang myapp.c libmylib.dylib -I include/
assert_success
# Moving/renaming the dynamic library will break the executable
mv libmylib.dylib libmylib2.dylib
./a.out > /dev/null 2>&1
assert_fail

find . -type f -name 'my*' -delete
rm a.out
rm libmylib2.dylib

# Building files that include libraries requires using linking options of the
# driver. 
# C libraries are linked to by default for `clang`. To link to C++ libraries,
# use the `clang++` driver
printf '
#include <iostream>
int main() {
    std::cout << "Hello World\\n";
    return 0;
}
' > myapp.cpp

# Fails at linking stage because iostream is a C++ std library
clang myapp.cpp > /dev/null 2>&1
assert_fail

# Succeeds
clang++ myapp.cpp
assert_success
./a.out
rm a.out

################################################################################
# Looking under the hood
# printf '
# int main() {
#     int x = 1;
#     int y = x + 1;
#     return 0;
# }
# ' > myapp.cpp
# clang++ -save-temps -ftime-report -v myapp.cpp > compile_verbose.log 2>&1
# echo "Verbose compile log saved"

# Important defaults
# -std=c++11
# -stdlib=libc++

################################################################################
# CLI configuration
# Stage Selection Options
# -c

# Language Selection and Mode Options
# -x
# -std
# -stdlib

# Target Selection Options

# Code Generation Options
# -O0, -O1, -O2, -O3, -Ofast, -Os, -Oz, -Og, -O, -O4
# -g

# Driver Options
# -i
# -ftime-report

# Diagnostics Options

# Preprocessor Options

################################################################################
# Other stuff

# Error and warning messages
# -W: -Wall -Wextra

# Optimization levels (-O)

# CLI tools
# ar - create and maintain groups of object files as an archive
# nm - display name list (symbol table) of object file
# otool
# dtruss
# lldb
# pkg-config


