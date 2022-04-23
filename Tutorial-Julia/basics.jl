# Comments
println("👋 🌎")

# Literals
my_int      = (1234567890,  1_234_567_890)
my_float    = (12345.67890, 12.34e5, 67.8E9, Inf, NaN)
my_float32  = 1f9
my_rational = 2//3
my_complex  = 1 + 9im
my_hex      = (0x19afAF, 0x1p9)
my_oct      = 0o1
my_bin      = 0b10
my_bool     = (true, false)
my_null     = nothing
my_missing  = missing

# Collection literals
my_vector      = [1, 2, 3, 4]
my_matrix      = [1  2; 3  4]
my_tuple       = (1, '2', 3.0)
my_named_tuple = (a=1, b=2, c=3)
my_pair        = "a" => 1
my_unit_range  = 1:4
my_step_range  = 1:1:4

# Boolean Operators
# ==, ===
@assert 1.0 == 1 === 1 !== 1.0 != 1.1
arr = [1,2]
@assert [1,2] == arr === arr !== [1,2] != [2,1] 
@assert !true === false 
@assert (true || false) === true 
@assert (true && false) === false 

# Integer representations
@assert( UInt8(65) === 0x41 === 0o101 === 0b1000001 !== 65 )

# Variables
x  = 3
π  = 3.14159
a,b = [1,2]
@assert a === 1 && b === 2
a,b,c = 1:3
@assert a === 1 && b === 2 && c === 3
a,b = "AB"
@assert a === 'A' && b === 'B'
_,b,_,d = 1:10
@assert b === 2 && d === 4
a,b... = 1:5
@assert a === 1 && b == [2,3,4,5]


function demo_type_declarations()
    # This style of type declarations cannot occur in global scope
    my_uint   :: UInt    = 19
    my_flt32  :: Float32 = 1.9
    my_bigint :: BigInt  = 10^19
end
#demo_type_declarations()

# Type Conversions: T(x) or convert(T,x)
my_uint   = UInt(19)
my_flt32  = Float32(1.9)
my_bigint = BigInt(10^19)

my_bigint = big(10^19)
my_bigflt = big(10.1^19)

@assert([ typemin(Int8),     typemax(Int8)]    == [-128, 127])
@assert([ typemin(Int16),    typemax(Int16)]   == [-32768, 32767])
@assert([ typemin(Int32),    typemax(Int32)]   == [-2147483648, 2147483647])
@assert(  typemin(Int64)  === -9223372036854775808)
@assert(  typemax(Int64)  ===  9223372036854775807)
@assert(  typemin(Int128) === -170141183460469231731687303715884105728)
@assert(  typemax(Int128) ===  170141183460469231731687303715884105727)

@assert([ typemin(UInt8),    typemax(UInt8)]   == [0, 255])
@assert([ typemin(UInt16),   typemax(UInt16)]  == [0, 65535])
@assert([ typemin(UInt32),   typemax(UInt32)]  == [0, 4294967295])
@assert([ typemin(UInt64),   typemax(UInt64)]  == [0, 18446744073709551615])
@assert([ typemin(UInt128),  typemax(UInt128)] == [0, 340282366920938463463374607431768211455])

@assert(typemax(Int) + 1 == typemin(Int))

println("DONE 😄")

# eps(), nextfloat(), prevfloat()
# zero(), one()

# Arithmetic Operators
@assert( 3 + 2 == 5   )
@assert( 3 - 2 == 1   )
@assert( 3 * 2 == 6   )
@assert( 3 / 2 == 2 \ 3 == 1.5 )
@assert( 3 ÷ 2 == 1 )
@assert( 3 ^ 2 == 9   )
@assert( √(3*3) == √9 == 3)
@assert( 3 % 2 == 1)

@assert( 1/Inf   === 0.0  )
@assert( 1/0     === Inf  )
@assert( -1/0    === -Inf )
@assert( Inf + 9 === Inf  )
@assert( Inf - 9 === Inf  )
@assert( Inf * 9 === Inf  )
@assert( Inf / 9 === Inf  )
@assert( 9 - Inf === -Inf )
@assert( 9 / Inf === 0    )
@assert( isnan(0/0)       )
@assert( isnan(Inf - Inf) )
@assert( isnan(Inf / Inf) )
@assert( isnan(0 * Inf)   )
@assert( NaN != NaN       )

# Comparison operators (and chaining)
@assert( 1 < 2 <= 2 ≤ 3 != 4 == 4 ≠ 3 ≥ 2 >= 2 > 1)

# Bitwise Operaters
# binary literals default to type UInt8 so all 8 bits are considered below
@assert( ~0b1111_0000 == 0b0000_1111 )
@assert(  0b0000_0011 &  0b0000_0101 == 0b0000_0001 )
@assert(  0b0000_0011 |  0b0000_0101 == 0b0000_0111 )
@assert(  0b0000_0011 ⊻  0b0000_0101 == 0b0000_0110 == xor( 0b0000_0011, 0b0000_0101))
@assert(  0b0000_0011 ⊼  0b0000_0101 == 0b1111_1110 == nand(0b0000_0011, 0b0000_0101))
@assert(  0b0000_0011 ⊽  0b0000_0101 == 0b1111_1000 == nor( 0b0000_0011, 0b0000_0101))
@assert(  0b1111_0000 >>> 3 == 0b00011110)  # logical shift right
@assert(   Int8(-2^7) >>  3 == Int8(-2^4))  # arithmetic shift right
@assert(  0b0001_1110 <<  3 == 0b1111_0000) # logical/arithmetic shift left

# Updating operatires
# +=  -=  *=  /=  \=  ÷=  %=  ^=  &=  |=  ⊻=  >>>=  >>=  <<=

# Missing (https://docs.julialang.org/en/v1/manual/missing/)
(missing == missing) === missing
ismissing(missing == 1)
ismissing(missing + missing)
ismissing(missing / missing)
ismissing(missing > 1)

isequal(missing, missing)
isless(Inf, missing)

(true  |  missing) === true
(false &  missing) === false
ismissing(false | missing)
ismissing(true  & missing)

(true  || missing) === true
(false && missing) === false
ismissing(false || missing)
ismissing(true && missing)
try missing && true; catch TypeError; end
try missing || false; catch TypeError; end

# Dot operators
@assert( [1,2,3] .+ 2 == [3,4,5])
@assert( )

# Numerica literal coefficients
x = 3
@assert( 2x == 2 * x )
@assert( 2x^2 == 2(x^2))
@assert( 2^2x == 2^(2x))
@assert( 6/2x == 6/(2x))
@assert( (x-1)x == (x-1)*x )
# x(1-x) -> MethodError: objects of type T are not callable
xf = e1 = 5
@assert( 2xf == 10 )
@assert( 0xf != 0  && 0xf == 15 ) # Ambiguities with literals resolved in favor of literals
@assert( 2e1 != 10 && 2e1 == 20 )

# Math functions
# isequal(), isless(), isfinite(), isinf(), isnan()
# round(), floor(), ceil(), trunc()
# div(), fld(), cld(), rem()
# mod(), mod1(), mod2pi(), divrem(), fldmod()
# gcd(), lcm()
# abs(), abs2(), sign(), signbit(), copysign(), flipsign()
# sqrt(), cbrt(),
# exp(), expm1(), ldexp(), log(), log(), log2(), log10(), log1p()
# exponent(), significand()
# hypot()
# sin    cos    tan    cot    sec    csc
# sinh   cosh   tanh   coth   sech   csch
# asin   acos   atan   acot   asec   acsc
# asinh  acosh  atanh  acoth  asech  acsch
# sinc   cosc
# sinpi  cospi
# sind   cosd   tand   cotd   secd   cscd
# asind  acosd  atand  acotd  asecd  acscd

#######################################
# Functions

# Declaration
function funcA(x, y)
    sum = x + y
    return sum
end
function funcB(x, y)
    x + y
end
funcC = (x,y) -> x + y
funcD(x, y) = x + y
funcE = funcD
@assert funcE === funcD
@assert funcA(2, 3) === funcE(2, 3) === 5

# Type specification
funcF(x::Int, y::Float64) = x + y
funcF(1, 1.1) === 2.1
try funcF(1.1, "string"); catch MethodError; end

funcG(x, y)::Int = x + y
funcG(2.5, 1.5) === 4
try funcG(1.1, 1); @assert false; catch MethodError; end

funcH((x,y), z) = x + y + z
@assert funcH((1,2),3) === 6

# Varargs and splatting
funcI(a,b,c...) = "func($a, $b, $c)"
@assert funcI(1,2)       === "func(1, 2, ())"
@assert funcI(1,2,3)     === "func(1, 2, (3,))"
@assert funcI(1,2,3,4,5) === "func(1, 2, (3, 4, 5))"

funcJ(a,b,c) = "func($a, $b, $c)"
@assert funcJ(1,(2,3)...) === funcJ((2,3)...,1) === "func(1, 2, 3)"

# defaults, keyword, varargs, and kwargs
funcK(a, b=2, args...; c, d=4, kwargs...) = "func($a, $b, $args, $c, $d, $kwargs)"
@assert funcK(8, c=9) === "func(8, 2, (), 9, 4, Base.Pairs{Symbol, Union{}, Tuple{}, NamedTuple{(), Tuple{}}}())"
@assert funcK(6,7,c=8,d=9) === "func(6, 7, (), 8, 9, Base.Pairs{Symbol, Union{}, Tuple{}, NamedTuple{(), Tuple{}}}())"
@assert funcK(6,7,c=8,d=9) === funcK(6,d=8,7,c=9)
@assert funcK(1,2,3,4,a=5,b=6,c=7,d=8,z=9) === "func(1, 2, (3, 4), 7, 8, Base.Pairs(:a => 5, :b => 6, :z => 9)"

a,b,c = (7,8,9)
funcL(a=1, b=c, c=b) = "func($a, $b, $c)"
@assert funcL() === "func(1, 9, 9)"

# do blocks
funcM(a,b) = "f($a, $b)"
apply(f::Function, x, y) = f(x,y) 
x = apply(funcM,1,2)
y = apply((a,b)->"f($a, $b)",1,2)
z = apply(1,2) do a, b 
    "f($a, $b)"
end
@assert x === y === z

# Composition
funcN = (sqrt ∘ abs ∘ +)
funcN(-2, -3, -4) === 3.0
(titlecase ∘ reverse ∘ strip)(" cba\n") === "Abc"
[1,4,9] .|> sqrt .|> Int |> sum === 6

#######################################
# Comprehensions