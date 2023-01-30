const assert = require('assert')

console.log('== Running scope.js ==');
/*******************************************************************************
Notes
- All variables are either global or local scope
    - Local scope is broken into local block, function, and module scope
    - Global variables are not imported from modules unless explicitely exported
- Declarations
    - `var` declares or redeclares a variable as global except for in functions
    - `let` declares a variable locally and prevents redeclaration
    - `const` declares a variable locally and prevents redeclaration or modification
    - No keyword depends
        -  
*******************************************************************************/
// Globals
g1       = 1
var g2   = 1
let g3   = 1
const g4 = 1

////////////////////////////////////////////////////////////////////////////////
// Block Scope (if, for, while, or just {})
{
    g1 = 2
    g2 = 2
    g3 = 2
    // g4 = 2 // TypeError: Assignment to constant variable.
    new_g1 = 2
}
assert(g1 == 2 && g2 == 2 && g3 == 2) // Updated
assert(g4 == 1) // Not updated
assert(new_g1 == 2) // New
{
    var g1 = 3
    var g2 = 3
    // var g3 = 3 // SyntaxError: Identifier 'g3' has already been declared
    // var g4 = 3 // SyntaxError: Identifier 'g4' has already been declared
    var new_g2 = 3
}
assert(g1 == 3 && g2 == 3) // Updated
assert(g3 == 2 && g4 == 1) // Not updated
assert(new_g2 == 3) // New

{
    let g1 = 4
    let g2 = 4
    let g3 = 4
    let g4 = 4
    assert(g1 == 4 && g2 == 4 && g3 == 4 && g4 == 4) // New
    let new_g3 = 4
}
assert(g1 == 3 && g2 == 3 && g3 == 2 && g4 == 1) // Not updated
// assert(new_g3 == 1) // ReferenceError: new_g3 is not defined

{
    const g1 = 5
    const g2 = 5
    const g3 = 5
    const g4 = 5
    assert(g1 == 5 && g2 == 5 && g3 == 5 && g4 == 5) // New
    const new_g4 = 5
}
assert(g1 == 3 && g2 == 3 && g3 == 2 && g4 == 1) // Not updated
// assert(new_g4 == 1) // ReferenceError: new_g4 is not defined

////////////////////////////////////////////////////////////////////////////////
// Function Scope
function testScope() {
    // Everything is the same as block scope except for var
    var g1 = 2
    var g2 = 2
    var g3 = 2 // Wasn't possible before
    // g4 = 2
    assert(g1 == 2 && g2 == 2 && g3 == 2 && g4 == 1) // New
    var new_g2_f = 2
}
testScope()
assert(g1 == 3 && g2 == 3 && g3 == 2 && g4 == 1) // Not updated
// assert(new_g2_f == 2) // ReferenceError: new_g2_f is not defined

////////////////////////////////////////////////////////////////////////////////
// Module Scope

console.log('== END ==');
