Built-in C++ Tutorial
=======================

# Running a C++ program
1. **Write** - Follow a C++ standard (C++98, 03, 11, 14, 17, 20)
1. **Build** - Choose a compiler compatible with your hardware/OS and that accepts your C++ standard 
1. **Execute** - Run the resulting executable(s)
1. **Debug** - Build and run with debugging tools to inspect program operations

# Steps in building a program 
1. Preprocessing 
    * Output = preprocessed file (`.ii`)
1. Parsing and Semantic Analysis
    * Output = Abstract Syntax Tree (AST)
1. Code Generation and Optimization
    * Output = assembly file (`.s`)
1. Assembler
    * Output = object file (`.o`)
1. Linker
    * Output = executable (`a.out`) or dynamic library (`.dylib`, `.so`)
1. Other
    * Bitstream (`.bc`) - clang specific binary file

# Setup
* Choosing a compiler
    * At first it mainly depends on your OS
        * MacOS - Clang (`clang++`)
        * Linux - GCC (`g++`)
        * Windows - Visual C++ (`cl`)
    * For more advanced users, additional factors become relevant
        * Standardization support
        * Efficiency of generated code
        * Build and debugging tools
        * Licensing
    * A comprehensive comparison of compilers is on (wikipedia)[`https://en.wikipedia.org/wiki/List_of_compilers#C++_compilers`]
* Writing source code
    * File extensions: .cc, .cpp, .cxx, .C
        * Generally doesn't matter unless you are dealing with picky IDEs or compilers

# Statement Types
* Declaration statements
* Jump statements
* Expression statements
* Compound statements
* Selection statements (conditionals)
* Iteration statements (loops)
* Try blocks

# Conventions
* {}-initialization

# Todo
* STL algorithms
* Functions, especially lambda functions
* Structs and classes
* Debugging (gdb and VSCode integrated debugger)
* Building projects (make, CMake)
* Logging
* Executables and user cmd lind args
* Style conventions and documentation
* Other
    * casting: static, dynamics, narrow
    * Boost library
    * templates and metaprogramming
    * constexpr and compile-time programming
    * I/O for data in CSV, JSON, XML, or binary (e.g. HDF) formatting
    * Documentation generation


## Viewing non-text files
* `od`, `hexdump`, `xxd`
