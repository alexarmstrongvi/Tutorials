Built-in C++ Tutorial
=======================

# TODO
* preprocessor directives
* linking object files
* creating and linking to a library
* VSCode IDE

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
    * File extensions: .cc, .cpp, .C
        * Generally doesn't matter unless you are dealing with picky IDEs or compilers

# Statement Types
* Declaration statements
* Jump statements
* Expression statements
* Compound statements
* Selection statements (conditionals)
* Iteration statements (loops)
* Try blocks

# Other

## Viewing non-text files
* `od`, `hexdump`, `xxd`
