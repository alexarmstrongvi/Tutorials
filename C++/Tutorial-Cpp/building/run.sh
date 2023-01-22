#!/usr/bin/env bash
################################################################################
# NOTES
# * MacOS offers the `clang` command line tool (a.k.a. driver) for building
#   C/C++ source code.
# * MacOS also seems to offer `gcc` builtin but this really just runs clang. The
#   real GNU gcc compiler must be installed.
# * `clang` is a driver that drives the build process, calling the compiled
#   (also called `clang` but a different executable) and linker (`ld`). Use the
#   verbose option (`-v`) to see all the commands run by the driver.
# * If no main function exists in any object files, a compiler error occurs
################################################################################

################################################################################
# Running `clang` without any options just produces an object file with default name `a.out`
echo 'int main() { return 0; }' > my_source_code.cpp

clang my_source_code.cpp
./a.out
if [ $? -eq 0 ]; then echo PASS; else echo FAILED; fi
rm a.out

# Specify output file
# Usually no extension is given to executables
clang -o my_executable my_source_code.cpp
./my_executable
if [ $? -eq 0 ]; then echo PASS; else echo FAILED; fi
rm my_executable

################################################################################
# Building files that include libraries requires using linking options of the driver.
# C libraries are linked to by default for `clang`. To link to C++ libraries, use the `clang++` driver
printf '
#include <iostream>
int main() {
    std::cout << "Hello World\\n";
    return 0;
}
' > my_source_code.cpp

# Fails at linking stage because iostream is a C++ std library
clang my_source_code.cpp > /dev/null 2>&1
if [ $? -ne 0 ]; then echo PASS; else echo FAILED; fi

# Succeeds
clang++ my_source_code.cpp
if [ $? -eq 0 ]; then echo PASS; else echo FAILED; fi
./a.out

################################################################################
# Looking under the hood
printf '
int main() {
    int x = 1;
    int y = x + 1;
    return 0;
}
' > my_source_code.cpp
clang++ -save-temps -ftime-report -v my_source_code.cpp > compile_verbose.log 2>&1
echo "Verbose compile log saved"

# Important defaults
# -std=c++11
# -stdlib=libc++

################################################################################
# Other stuff

# Error and warning messages
# -W: -Wall -Wextra

# Optimization levels (-O)
echo "Remove generated code when done: rm my_source_code* a.out compile_verbose.log"