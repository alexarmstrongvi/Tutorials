module test_types
import Test

function main()
    println("Testing types")

    # Type assertions
    @assert typeof(2) == Int64
    x = 2
    @assert typeof(x) == Int64
    x = 2::Int64
    @assert typeof(x) == Int64
    @Test.test_throws TypeError 2::Int16

    # Type declarations
    my_int16::Int16 = 2
    @assert typeof(my_int16) === Int16 
    my_int64 = 2
    # declarations apply to whole scope, even before the declaration 
    @assert typeof(my_int64) != Int64 
    my_int64::Float32 = 3
    @assert typeof(my_int64) === Float32
    local my_float32::Float32
    my_float32 = 3
    @assert typeof(my_float32) === Float32

    # Creating types
    @assert Int64 <: Signed <: Integer <: Real <: Number <: Any
    @assert Float64 <: AbstractFloat <: Real


end

# Type creation: Abstract, Concrete, Primitive
abstract type MyAbstractType end
abstract type MyAbstractIntType <: Integer end

primitive type My8BitPrimitiveType 8 end
primitive type My8BitIntType <: Signed 8 end

main()

end

