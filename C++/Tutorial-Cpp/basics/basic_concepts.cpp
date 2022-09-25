////////////////////////////////////////////////////////////////////////////////
// Resources
// - https://en.cppreference.com/w/cpp/language/basic_concepts
// - https://en.cppreference.com/w/cpp/language/expressions
// - https://en.cppreference.com/w/cpp/language/value_category
// - 
////////////////////////////////////////////////////////////////////////////////

#include <iostream>
using std::cout;
#include <string>
using std::string;


// "A C++ program is a sequence of text files that contain declarations."
// "Declarations introduce names into the C++ program."
// Names function as identifiers for the various C++ entity types (e.g. functions, variables, classes, etc.)
// All C++ programs run by executing the function declared with the name "main"

// Declarations
int function_declaration_name();
extern int variable_declaration_name;
class class_declaration_name;


// Definitions are a type of declaration that specify how to use the entities identified by the name (i.e. how to call/run it)
void function_definition() {} // function that does nothing 
int variable_definition; // uninitialized but still memory allocated
class class_definition {}; // empty class

// Definitions usually create objects in memory whereas declarations simply add names to the namespace

// Each of the above lines of code is referred to as a statement
// "Statements are fragments of the C++ program that are executed in sequence"
// There are several types of statments.
// In most cases they are marked by the ending semicolon ';'.
// The exception is block statements
// The lines above contain declaration statements, which are basically just declarations but in the context of a program

// Another type of statement is the empty or null statement
;

// The remaining types of statements only work within a function definition
void statement_types() {
    int x; // Declaration statement
    
    // The most common type of statement is an expression statement
    // "An expression is a sequence of operators and their operands, that specifies a computation"
    1;      // Literal expression
    x = 1;  // Assignment expression    [operator=]
    x + 1;  // Arithmetic expression    [operator+]
    x == 1; // Comparison expression    [operator==]
    &x;     // Member access expression [operator&]
    x++;    // Increment expression     [operator++]
    // Expressions ending with a semicolon are expressions statements 
    // see expressions() for more details
    
    // Flow control involves a few other common statements
    // Selection statments
    if (true) 
        cout << "if statement\n";
    else 
        cout << "else clause of if statment\n";

    switch (1) 
        case 1: cout << "switch statement\n";

    // Iteration statements
    while (true) 
        break;
    cout << "while loop\n";

    do cout << "do-while loop\n"; while (false);
    for (cout << "init-statement -> "; 
         cout << "condition -> ";
         cout << "iteration expression: ")
        break;
    cout << "for loop\n";

    // Jump and label statements (e.g. break, continue, return, goto)
    x = 2;
    label_statement:;
    cout << "label statement and ";
    if (--x > 0)
        goto label_statement;
    cout << "goto statement\n";


    // Several other types of statements remain but the above are the main ones
    // Finally, all these statements can be combined into a compound statement using curly braces {}
    // This entire function is really just a function declaration followed by a compound statement that gets run anytime the function name is called.
    // Compound statements do not need to end in a semi-colon
}

// A function definition can now be understood as a function declaration statement combined with a compound statement defining how the function is used.

void expressions() {
    int x;
    // Expressions are where the actual computation of programs is done.
    // Declarations and statements are simply about setting up and steering the program to the right expressions.
    // The building blocks of expressions are primary expressions
    // 1. Literals
    1;
    "strings";
    // 2. Identifiers
    x; // unqualified
    std::cout; // qualified (by std::)
    // 3. lambda expressions
    // etc...

    // Primary expressions get combined with operators to build more complex expressions
    1 + 1;
    
    cout << "x = " << x << '\n';
    (x = 2) = 3;
    cout << "x = " << x << '\n';

    // Any expression, whether primary or compound, evaluates to a single value
    // That value is categorized by a type and a value category

    
}

int main() {
    statement_types();
    expressions();
    return 0;
}
