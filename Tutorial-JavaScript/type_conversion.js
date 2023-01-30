const assert = require('assert')

////////////////////////////////////////////////////////////////////////////////
// Number to String
//toString()
//toExponential()
//toFixed()
//toPrecision()

////////////////////////////////////////////////////////////////////////////////
// String to Number
//Number()
assert(Number(true)    == 1)
assert(Number(false)   == 0)
assert(Number("10")    == 10)
assert(Number(" 10  ") == 10)
assert(Number("10.33") == 10.33)
assert(isNaN(Number("10,33")))
assert(isNaN(Number("10 33")))
assert(isNaN(Number("John")))

//parseInt()
//parseFloat()

////////////////////////////////////////////////////////////////////////////////
// Base N: Decimal, Octal, Hexidecimal, Binary, etc..
//
