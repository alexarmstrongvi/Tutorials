module CollectionsTutorial
export main

function main()
    println("Testing Collections")
    ############################################################################
    # Literals
    ############################################################################
    vector      = [1, 2, 3, 4]
    matrix      = [1  2; 3  4]
    tuple       = (1, '2', 3.0)
    named_tuple = (a=1, b=2, c=3)
    pair        = "a" => 1
    unit_range  = 1:4
    step_range  = 1:1:4
    
    typeof(vector) === Vector{Int} === Array{Int, 1}
    typeof(matrix) === Matrix{Int} === Array{Int, 2}
    typeof(tuple) === Tuple{Int, Char, Float64}
    typeof(named_tuple) === NamedTuple{(:a, :b, :c), Tuple{Int64, Int64, Int64}}
    typeof(pair) === Pair{String, Int}
    typeof(unit_range) === UnitRange{Int}
    typeof(step_range) === StepRange{Int, Int}
    
    # Type inference
    typeof([1,2,3.0])   == Vector{Float64}
    typeof(["1","23"])  == Vector{String}
    typeof(['1',"23"])  == Vector{Any}
    typeof([1,'2',3.0]) == Vector{Any}

    typeof((1,))            == Tuple{Int}
    typeof((1,'2'))         == Tuple{Int, Char}
    typeof((1,'2',3.0))     == Tuple{Int, Char, Float64}
    typeof((1,'2',3.0,"4")) == Tuple{Int, Char, Float64, String}
    typeof((1,2,3,4,5,6,7)) == NTuple{7, Int}

    # Type specification
    arr_int = Int8[1,2,3]
    arr_flt = Float64[1,2,3]
    try Int64[1,2.2]; catch InexactError; end

    ############################################################################
    # Constructors
    ############################################################################
    
    Vector{Int}()
    Matrix{Int}()
    Array{Int,3}()
    
    Tuple{}()
    NamedTuple()

    UnitRange(1,10)   === range(1,10)           === 1:10
    StepRange(1,2,10) === range(1,10, step=2)   === 1:2:10
    LinRange(1,10,3)  ==  range(1,10, length=3) === 1.0:4.5:10.0

    # Dictionary
    dict1 = Dict("A"=>1, "B"=>2)
    dict2 = Dict([("A",1), ("B",2)])
    dict3 = Dict{String, Int}("A"=>1, "B"=>2)
    dict1 == dict2 == dict3
    typeof(Dict('A' => 1, 2 => "B", (1,2) => [3, 4])) == Dict{Any, Any}
    
    # Set
    itr = [1,2,3,2] # 1:3; (1,2,3,2);
    Set(itr) == Set{Int}(itr) == Set([1,2,3]) == Set([3,1,2])

    # Speciality Variants
    # BitArray()
    # BitVector()
    # BitMatrix()
    # BitSet()

    # DenseArray()
    # DenseVector()
    # DenseMatrix()

    # StepRangeLen()

    # IdDict()
    # WeakKeyDict()
    # Base.ImmutableDict()
    # Base.EnvDict()

    ############################################################################
    # General collections
    ############################################################################
    
    # Properties
    coll = Set(1:10)
    length(coll)  === 10
    length(99)    === 1
    isempty(coll) === (length(coll) === 0)
    # checked_length

    # Modification
    coll = Set(1:10)
    empty!(coll)
    coll == Set{Int}()
    
    ############################################################################
    # Iterable collections (are there non-iterable collections?)
    ############################################################################
    
    # Attributes
    Vector{eltype(itr)} === typeof(itr)
    step(range(1,10,length=5)) === 2.25 

    # Checks/Tests
    itr = [1,2,3]

    1 in itr
    1  ∈ itr
    99 ∈ 99
    ([1,2,4]  ∈  itr  ) === false
    ([1,4,2] .∈  itr  ) == [true, false, false]
    ([1,4,2] .∈ (itr,)) == [true, false, true ]

    (-1 ∉ itr) === !(-1 in itr) === true

    allunique([1,2,3])
    # any(), all()
    
    # Properties
    # maximum(), minimum(), extrema(), argmax(), argmin(), findmax(), findmin()
    # findall(), findfirst(), findlast(), findnext(), findprev()
    unique([1,2,1]) == [1,2]
    unique(abs, [1,-1,-3,3,4]) == [1,-3,4]
    # first()
    # last()
    Base.front((1,2,3)) == (1,2)
    Base.tail( (1,2,3)) == (2,3)
    
    # Comparisons
    a = [4,6,5,4,9]
    b = [4,5,6]
    indexin(a, b) == [findfirst(isequal(x),b) for x in a] == [1,3,2,1,nothing]

    # Functionals
    # sum(), prod()
    reduce(*, [2,3,4])          ===  24 # Order of reduction not guaranteed
    reduce(*, [2,3,4], init=-1) === -24
    f = (x,y) -> "f($x,$y)"
    foldl(f ,[2,3,4], init=1) === "f(f(f(1,2),3),4)"
    foldr(f ,[2,3,4], init=1) === "f(2,f(3,f(4,1)))"
    # count(f, itr, init)
    f  = (x...) -> "f($(join(x,",")))"
    op = (x...) -> "$(join(x,"+"))"
    # foreach()
    map(f, 1:3)             ==  ["f(1)", "f(2)", "f(3)"]
    map(f, 1:2, 3:4, 5:100) ==  ["f(1,3,5)", "f(2,4,6)"]
    mapreduce(f, op, 1:3)             === "f(1)+f(2)+f(3)"
    mapreduce(f, op, 1:2, 3:4, 5:100) === "f(1,3,5)+f(2,4,6)"
    # mapfoldl(), mapfoldr()
    filter(isodd, 1:5) == [1,3,5]
    replace([1, 3, 2, 1], 1=>0, 2=>4, count=2) == [0,3,4,1]

    # Transformations/Conversions
    collect(1:2:5) == [1,3,5]
    collect(Float64, 1:2:5) == [1.0,3.0,5.0]
    
    # Other
    # rest()

    ############################################################################
    # Indexable collections
    ############################################################################
    # getindex
    # setindex!
    # firstindex
    # lastindex
    
    # Viewing/Indexing/Slicing
    SubArray

    ############################################################################
    # Dictionaries
    ############################################################################
    # haskey
    # get
    # get!
    # getkey
    # delete!
    # pop!
    # keys
    # values
    # pairs
    # merge
    # mergewith
    # merge!
    # mergewith!
    # sizehint!
    # keytype
    # valtype

    ############################################################################
    # Sets
    ############################################################################
    # union
    # union!
    # intersect
    # setdiff
    # setdiff!
    # symdiff
    # symdiff!
    # intersect!
    # issubset
    # ⊈
    # ⊊
    # issetequal
    # isdisjoint

    ############################################################################
    # Dequeues
    ############################################################################
    # push!
    # pop!
    # popat!
    # pushfirst!
    # popfirst!
    # insert!
    # deleteat!
    # keepat!
    # splice!
    # resize!
    # append!
    # prepend!

    ############################################################################
    # Other
    ############################################################################
    # Missing values
    x = Union{Missing, Int}[1, missing, 3]
    y = skipmissing(x)

    ismissing(sum(x))
    sum(y) == 4
    
    y[1] == x[1] == 1
    try y[2]; catch MissingException; end

    ismissing([1, missing] == [1, missing])
    ([1, missing] == [2, missing]) === false



end # main()

end # module CollectionTutorials