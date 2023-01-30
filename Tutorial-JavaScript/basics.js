/*******************************************************************************
JavaScript Basics
*******************************************************************************/

const assert = require('assert')

// Hello World
console.log('== START ==');

////////////////////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////////////////////
// Declaration, Scope, and Hoisting

// Declaring
var a1
let b1
let c1, d1
// const c1  // SyntaxError: Missing initializer in const declaration
assert(a1 == undefined && b1 == undefined && c1 == undefined && d1 == undefined)

// Declaring and initializing
a2 = 1
var b2 = 1
let c2 = 1
const d2 = 1
let e2, f2 = 1, g2 = h2 = 1  
assert(e2 == undefined)
assert(a2 == 1 && b2 == 1 && c2 == 1 && d2 == 1 && f2 == 1 && g2 == 1 && h2 == 1)

// Updating/Redeclaring variable declared and initialized with `var`
var x = 1 // Same for `x = 1`
x = 2
var x = 3
// let x = 9   // SyntaxError: Identifier 'x' has already been declared
// const x = 9 // SyntaxError: Identifier 'x' has already been declared

// Updating/Redeclaring variable declared and initialized with `let`
let y = 1
y = 2
// var y = 9   // SyntaxError: Identifier 'y' has already been declared
// let y = 9   // SyntaxError: Identifier 'y' has already been declared
// const y = 9 // SyntaxError: Identifier 'y' has already been declared

// Updating/Redeclaring variable declared and initialized with `const`
const z = 1
// z = 2       // TypeError: Assignment to constant variable.
// var z = 9   // SyntaxError: Identifier 'z' has already been declared
// let z = 9   // SyntaxError: Identifier 'z' has already been declared
// const z = 9 // SyntaxError: Identifier 'z' has already been declared

// Updating/Redeclaring variables declared and initialized with `let` together
let a3, b3 = 1, c3 = d3 = 1, f3
// var a3 = 2 // SyntaxError: Identifier 'a3' has already been declared
// var b3 = 2 // SyntaxError: Identifier 'b3' has already been declared
// var c3 = 2 // SyntaxError: Identifier 'c3' has already been declared
var d3 = 2 // As if declared with `var d3 = 1`
// var f3 = 2 // SyntaxError: Identifier 'f3' has already been declared


// Identifier naming rules
var aA1_$ = 1
var $     = 1
var $a$   = 1
var _     = 1
var _a_   = 1
assert(aA1_$ === 1 && $ == 1 && $a$ == 1 && _ == 1 && _a_ == 1)

var uppercase = 1
var UpperCase = 2
assert(uppercase != UpperCase) // Case sensative variable names

////////////////////////////////////////////////////////////////////////////////
// Built-in types and literals
////////////////////////////////////////////////////////////////////////////////
assert(typeof 5    == 'number')
assert(typeof 5.5  == 'number')
assert(typeof 5e5  == 'number')
assert(typeof NaN  == 'number')
assert(typeof Infinity  == 'number')
assert(typeof '5'  == 'string')
assert(typeof true == 'boolean')
assert(typeof null == 'object') // Bug. Should be null
assert(typeof undefined  == 'undefined')
assert(typeof undefined  == 'undefined')
// Built-ins are not instances of their types 
// see https://stackoverflow.com/questions/899574/what-is-the-difference-between-typeof-and-instanceof-and-when-should-one-be-used
assert(!(5    instanceof Number))
assert(!('5'  instanceof String)) 
assert(!(true instanceof Boolean))

assert(null == undefined)
assert(null !== undefined)

////////////////////////////////////////////////////////////////////////////////
// Operators
////////////////////////////////////////////////////////////////////////////////
// Very similar to C++ except...
// (== and !=) vs. (=== and !==)
assert( (5 ==  5) &&  (5 ==  '5') && !(5 ==  6))
assert( (5 === 5) && !(5 === '5') && !(5 === 6))
assert(!(5 !=  5) && !(5 !=  '5') &&  (5 !=  6))
assert(!(5 !== 5) &&  (5 !== '5') &&  (5 !== 6))

////////////////////////////////////////////////////////////////////////////////
// Functions (similar to Python)
////////////////////////////////////////////////////////////////////////////////
function myFunc(a, b = 3) {
    var c = a + b
    return c
}
assert(typeof myFunc == 'function')
assert(myFunc instanceof Function)
assert(myFunc(1,3) == 4)
assert(myFunc(1) == 4)

// Arrow functions (like lambda functions)
myFunc = (a, b=3) => { return a + b }
myFunc = (a, b=3) => { a + b }
myFunc = (a, b=3) => a + b
assert(typeof myFunc == 'function')
assert(myFunc instanceof Function)
assert(myFunc(1,3) == 4)
assert(myFunc(1) == 4)

myFunc = a => a + 3;
assert(myFunc(1) == 4)

////////////////////////////////////////////////////////////////////////////////
// Numbers
////////////////////////////////////////////////////////////////////////////////
assert(NaN != NaN)
assert(isNaN(NaN))
assert(Infinity + 5 == Infinity)
assert(1 / 0  == Infinity)
assert(-1 / 0 == -Infinity)
//Number.MAX_VALUE
//Number.MIN_VALUE
assert(Number.POSITIVE_INFINITY == Infinity)
assert(Number.NEGATIVE_INFINITY == -Infinity)
assert(isNaN(Number.NaN))

////////////////////////////////////////////////////////////////////////////////
// Strings
////////////////////////////////////////////////////////////////////////////////
var s = "0123456789012"
assert(s.length == 13)
assert(s[1] == "1")
assert(s[s.length - 1] == "2")

assert(s.indexOf("12") == 1) // first occurance
assert(s.lastIndexOf("12") == 11) // last occurance
assert(s.indexOf("12", 5) == 11)
assert(s.lastIndexOf("12", 5) == 1)
assert(s.indexOf("A") == -1) // If text not found

// Regex (see regex.js for more)
assert(s.search("[3-9]") === 3) // first occurance
assert(s.search(/[3-9]/) === 3) // first occurance
assert(s.match(/[3-9]/).index === 3) // returns { '3', index: 3, input: ... }
assert(s.match(/[3-9]/)[0] === '3')
assert(s.match(/[3-9]/g).length == 7)

// Arithmatic
assert("Answer is " + 5 + 2 == "Answer is 52")
assert("Answer is " + (5 + 2) == "Answer is 7")
assert(5 + 2 + " is the answer" == "7 is the answer")
assert("100" / "5" ==  "20")
assert("100" / "5" !== "20")
assert("100" / "5" === 20)
assert("100" / 5   === 20)
assert( 100  / "5" === 20)
assert("100" * 5   === 500)
assert("100" - 5   === 95)
assert(isNaN("100"*"A"))

// Other methods
//.split(sep, limit)

////////////////////////////////////////////////////////////////////////////////
// Arrays
////////////////////////////////////////////////////////////////////////////////
myFunc = (a, b=3) => a + b
var array = [5, '5', true, [1, 2], {"A" : 1}, myFunc]
assert(typeof array == 'object')
assert(array instanceof Array)
assert(Array.isArray(array))
assert(array.length == 6)
assert(array[1] == '5')
assert(array[4]["A"] == 1)
assert(array[5](1,2) == 3)

// Comparing arrays (you cant)
var arr1 = [1,2,3]
var arr2 = [1,2,3]
assert(arr1 != arr2)

// Modifying arrays
var array = [0,1,2,3]
var len = array.push(4)
assert(len == array.length)
assert(array.pop() == 4)
var len = array.unshift(-1)
assert(array.shift() == -1 && array[0] == 0) // pop_left
delete array[3]
assert(array[3] == undefined)
array[array.length] = 4
array[array.length + 1] = 6
assert(array[4] == 4 && array[5] == undefined && array[6] == 6)

// Sort (in place and returns)
var array = [0,2,1]
var arr2 = array.sort()
assert(arr2[0]  == 0 && arr2[2]  == 2)
assert(array[0] == 0 && array[2] == 2)
var arr2 = array.reverse()
assert(arr2[0]  == 2 && arr2[2]  == 0)
assert(array[0] == 2 && array[2] == 0)

// Constant arrays
const const_arr = [1, 2, 3]
// const_arr = [4, 5, 6] // TypeError: Assignment to constant variable.
const_arr[0] = 4
const_arr.push(4)
const_arr[const_arr.length + 1] = 9
assert(const_arr[8] == undefined)

// Slice, Splice, and Concatenate
var array = [0,1,2,3,4,5]
var start = 2, stop = 4
var arr1 = array.slice(start, stop)
assert(array.length == 6 && arr1[0] == 2 && arr1[1] == 3)

var n = 2
var add1 = 7, add2 = 8, add3 = 9
var arr2 = array.splice(start, n, add1, add2, add3) // add as many elements, first they replace removed elements
assert(array.length == 7 && arr2[0] == 2 && arr2[1] == 3)

var arr1 = [1,2], arr2 = [3,4], arr3 = [5,6]
var arr4 = arr1.concat(arr2, arr3)
assert(arr1.length == 2 && arr4.length == 6)

// Iterating
//.map          - apply function to each element and return new array
//.forEach      - applies map in-place
//.filter       - new array from passing elements
//.reduce       - return value from reducing each pair of elements (e.g. sum)
//.reduceRight  - reduce from the right
//.every        - test if every element passes check
//.some         - test if any elements pass check
//.indexOf      - first index of exact match
//.lastIndexOf  - last index of exact match
//.find         - first element passing check
//.findIndex    - index of first element passing check

// Other methods
var array = [1, 2, 3]
assert(array.toString() == "1,2,3")
assert(array.join(", ") == "1, 2, 3")

////////////////////////////////////////////////////////////////////////////////
// Objects
////////////////////////////////////////////////////////////////////////////////
var obj = {
    property1 : "val1", 
    property2 : "val2",
    method1   : function() { return this.property1 + "_" + this.property2 }
}
assert(typeof obj == 'object')
assert(obj instanceof Object)
assert(Object.keys(obj).length == 3)
assert(obj["property1"] == "val1")
assert(obj.property2 == "val2")
assert(obj.method1() == "val1_val2")

var obj1 = {a : "A"}
var obj2 = {a : "A"}
assert (obj1 != obj2) // Different objects are never equal

////////////////////////////////////////////////////////////////////////////////
// Classes (i.e. object templates)
////////////////////////////////////////////////////////////////////////////////
class MyClass {
    constructor(x,y=5) {
        this._x = x
        this._y = y
        this._z = 0
    }
    method() {
        this._z++
    }
    get x() { return this._x }
    set x(x) { this._x = x }
    get y() { return this._y }
    set y(y) { this._y = y }
    get z() { return this._z }
    set z(z) { this._z = z }
}
var my_instance = new MyClass(3)
my_instance.method()
assert(my_instance.x == 3 && my_instance.y == 5 && my_instance.z == 1)

// Inheritance
class MySubclass extends MyClass {
    constructor(x, y=4, a) {
        super(x, y)
        this._a = 0
    }
    get a() { return this._a }
    set a(a) { this._a = a }
}
var my_sub = new MySubclass(2)
my_sub.method()
assert(my_sub.x == 2 && my_sub.y == 4 && my_sub.z == 1 && my_sub.a == 0)

////////////////////////////////////////////////////////////////////////////////
// Errors
////////////////////////////////////////////////////////////////////////////////
result = []
try {
    result.push(0)
    throw "MyErrorText"
    result.push(1)
} catch (err) {
    if (err instanceof TypeError) {
        result.push(2)
    } else if (err === 'MyErrorText') {
        result.push(3)
    } else {
        result.push(4)
    }
} finally {
    result.push(5)
}
assert(result[0] == 0 && result[1] == 3 && result[2] == 5)

// Error names
// EvalError      - An error has occurred in the eval() function
// RangeError     - A number "out of range" has occurred
// ReferenceError - An illegal reference has occurred
// SyntaxError    - A syntax error has occurred
// TypeError      - A type error has occurred
// URIError       - An error in encodeURI() has occurred

////////////////////////////////////////////////////////////////////////////////

/* 
 * Remaining Questions 
 * What are the semicolon conventions (https://www.codecademy.com/resources/blog/your-guide-to-semicolons-in-javascript/)
 * How does importing modules work?
 * When to allocate with `new`? Makes something an object type instead of primary type
 */

