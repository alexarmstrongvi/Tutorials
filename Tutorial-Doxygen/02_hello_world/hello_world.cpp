////////////////////////////////////////////////////////////////////////////////
/// Copyright (c) Jan 2019 by Jon Doe
///
/// @file hello_world.cpp
/// @brief Brief file description
///
/// An optional detailed description follows, separated from the brief
/// description by one empty line in the source code.
/// It can stretch across several lines
/// if needed to give all the details one thinks is necessary
/// 
/// @author Jon Doe <jon.doe@service.domain>
/// @date 1 Jan 2019
///
////////////////////////////////////////////////////////////////////////////////

#include <iostream>
using std::cout;
using std::endl;

#include <string>
using std::string;


////////////////////////////////////////////////////////////////////////////////
// Function declaration
////////////////////////////////////////////////////////////////////////////////
void print_msg(string s);

/// @brief Extended function description
///
/// Everything in this comment block will be considered documentation for the 
/// function directly below it. 
///
/// There are several ways to create a block comment but my preference is 
/// for this style, backslash bars on the top and bottom with 3 backslashes
/// indicating the comment (only visible in source code)
///
/// @param argc The number of command line arguments
/// @param argv The command line arguments
/// @return status code
int main(int argc, char* argv[]) {
    // Double backslash comments will be ignored by doxygen

    print_msg("Hello World");
    return 0;
}

/// @brief Function description: print message to stdout
/// @param s message to print
/// @param nonexistentparam doxygen will assume this is a param even if it isn't in the source code
///        but it will print out a warning
void print_msg(string s) {
    cout << s << endl;
}
