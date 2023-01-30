/*******************************************************************************
JavaScript Flow Control
*******************************************************************************/

const assert = require('assert')

////////////////////////////////////////////////////////////////////////////////
// For loop
////////////////////////////////////////////////////////////////////////////////
// For loops same as C++
for (i=0;i<5;i++) {/*do stuff*/}

////////////////////////////////////////
// for/in loops
var result = []
for (key in {"A":1,"B":3,"C":5}) {
    result.push(key)
}
assert(result[0] === 'A' && result[1] === 'B' && result[2] === 'C')

var result = []
for (idx in [1,3,5]) {
    result.push(idx)
}
// NOTE: index order is not guaranteed by for/in loop over arrays
assert(result[0] === '0' && result[1] === '1' && result[2] === '2')

var result = []
for (idx in 'Str') {
    result.push(idx)
}
assert(result[0] === '0' && result[1] === '1' && result[2] === '2')

////////////////////////////////////////
// for/of loops
//var obj = {"A":1,"B":3,"C":5}
//for (let val of obj) {} // TypeError: obj is not iterable

var result = []
var iterable = [1,3,5]
for (let val of [1,3,5]) {
    result.push(val)
}
assert(result[0] === 1 && result[1] === 3 && result[2] === 5)

var result = []
for (let char of 'Str') {
    result.push(char)
}
assert(result[0] === 'S' && result[1] === 't' && result[2] === 'r')

////////////////////////////////////////////////////////////////////////////////
// While loop
////////////////////////////////////////////////////////////////////////////////
var x = 0
while (x < 5) {
    x++
}
assert(x == 5)

do {
    x++
}
while (x < 5)
assert(x == 6)

////////////////////////////////////////////////////////////////////////////////
// If-else
////////////////////////////////////////////////////////////////////////////////
var array = [0,1,2,3]
var result = []
for (let x of array) {
    if (x == 1) {
        result.push(1)
    } else if (x == 2) {
        result.push(2)
    } else {
        result.push('E')
    }
}
assert(result.toString()=="E,1,2,E")
    
////////////////////////////////////////////////////////////////////////////////
// Switch
////////////////////////////////////////////////////////////////////////////////
var array = [0,1,2,3,'3','string',4]
var result = []
for (let expression of array) {
    switch (expression) {
        case 0:
            result.push(0) 
            break;
        case 1:
            result.push(1) 
        case 2:
            result.push(2) 
            break;
        case '3':
            result.push("'3'") // will match '3' but not 3 as '===' is used
            break;
        case 'string': // case can be any value comparable with ===
            result.push("'string'") 
            break;
        case 0:
            result.push('0b') // Will never happen. First match always used
            break;
        default:
            result.push('D') 
            // do stuff
    }
}
assert(result.toString()=="0,1,2,2,D,'3','string',D")

////////////////////////////////////////////////////////////////////////////////
// Break/Continue in labeled blocks
////////////////////////////////////////////////////////////////////////////////
var result = 0
mylabel : {
    result = 1
    // break  // SyntaxError: Illegal break statement
    break mylabel
    result = 2
}
assert(result == 1)

var result = []
outer:
for (let x of [1,2,3]) {
    middle:
    for (let y of [1,2,3]) {
        inner:
        for (let z of [1,2,3,4,5]) {
            if (y == 3 && z == 2) { break outer }
            if (y == 2 && z == 2) { continue middle }
            if (z == 3) { continue }
            if (z == 4) { break }
            result.push([x,y,z])
        }
    }
}
assert(
    /*                          x                  y                  z */ 
    /* Entry 1 */ result[0][0]==1 && result[0][1]==1 && result[0][2]==1 && // = [1,1,1]
    /* Entry 2 */ result[1][0]==1 && result[1][1]==1 && result[1][2]==2 && // = [1,1,2]
    /* Entry 3 */ result[2][0]==1 && result[2][1]==2 && result[2][2]==1 && // = [1,2,1]
    /* Entry 4 */ result[3][0]==1 && result[3][1]==3 && result[3][2]==1    // = [1,3,1]
)
