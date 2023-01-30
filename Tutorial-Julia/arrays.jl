n = 5
type = Int
initializer = undef
ndim = 1
arr_foo = Array{type}(initializer, n)
typeof(arr_foo) == Array{type, ndim}

arr_int  = [1,2,3]
arr_flt  = [1,2,3.1, pi]
arr_char = ['A','1','!']
arr_str  = ["AB", "12", "!?"]
arr_fun  = [sin, cos, tan]
arr_any  = [1, 1.1, 'A', "AB", sin, pi]

# Constructors
# zeros(), ones(), fill(), fill!()
# trues(), falses(), 
# rand(), randn()
# repeat()
# copy(), similar()

#######################################
# Multidimensional arrays
# reshape()