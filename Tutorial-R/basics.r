#!/usr/bin/env Rscript
################################################################################
# R Basics
################################################################################
# Loading packages
# library(package)

################################################################################
# Variables
################################################################################
# Assignment
assign("myvar", 1) # variable name must be string
myvar <- 1
1 -> myvar

# Names
a  <- 1
A  <- 1 # case sensative
.  <- 1
a1 <- 1
a_ <- 1
# Invalid variable names : _var , 1var, .1var, or any other special characters

################################################################################
# Built-in types and literals
################################################################################
# typeof()
stopifnot( typeof(1L)   == "integer") # typeof(1)  == "double"
stopifnot( typeof(1.1)  == "double") 
stopifnot( typeof(1+1i) == "complex") 
stopifnot( typeof("A")  == "character")
stopifnot( typeof(TRUE) == "logical") # 'T' can be used but isn't advised
stopifnot( typeof(NaN)  == "double")
stopifnot( typeof(Inf)  == "double")
stopifnot( typeof(NA)   == "logical")
stopifnot( typeof(NULL) == "NULL")

# class() vs typeof() - same except for double/NaN/Inf
stopifnot( class(1.1)   == "numeric")

# mode() vs typeof() - same except for double/NaN/Inf integer
stopifnot( mode(1.1)    == "numeric") 
stopifnot( mode(1L)     == "numeric")


# is.<mode/type>()
stopifnot( is.integer(1L))
stopifnot( is.double(1.1))
stopifnot( is.numeric(1L) && is.numeric(1.1) )
stopifnot( is.complex(1+1i))
stopifnot( is.character("A"))
stopifnot( is.logical(TRUE))
stopifnot( is.nan(NaN) && is.na(NaN) && is.double(NaN))
stopifnot( is.double(Inf))
stopifnot( is.na(NA)   && is.logical(NA))
stopifnot( is.null(NULL))

# str() - print object structure (i.e. repr() in python)
# builtin_types <- list(1L, 1.1, 1i, "A", TRUE, NaN, Inf, NA, NULL)
# for (x in builtin_types) {str(x)}
# > int 1
# > num 1
# > num 1.1
# > cplx 0+1i
# > chr "A"
# > logi TRUE
# > num NaN
# > num Inf
# > logi NA
# > NULL

# Strings


# Equality and arithmatic with special types
stopifnot(TRUE == 1 && FALSE == 0 && TRUE/(TRUE + TRUE) == 0.5)
stopifnot(is.na(NA  == NA )) # x == NA returns NA instead of bool
stopifnot(is.na(NaN == NaN)) # x == NaN returns NA instead of bool
stopifnot(is.nan(0/0))
stopifnot(1/0 == Inf)
stopifnot( Inf +  Inf ==  Inf)
stopifnot(-Inf + -Inf == -Inf)
stopifnot( Inf * -Inf == -Inf)
stopifnot(is.nan(Inf - Inf))
stopifnot(is.nan(Inf / Inf))
suppressWarnings(
    stopifnot(is.nan(sqrt(-1)))
)
stopifnot(sqrt(-1+0i) == 0+1i)

########################################
# Mode conversion (aka type casting)
# as: as.<mode>(x)
stopifnot( as.integer(3.9)   == 3)
stopifnot( as.character(3.9) == "3.9")

################################################################################
# Built-in data structures
################################################################################
stopifnot(class(c())          == "NULL")
stopifnot(class(matrix())     == c("matrix", "array"))
stopifnot(class(data.frame()) == "data.frame")

# unclass
# other types "raw", "list", "closure", "special", "builtin" , "environment", "S4"

########################################
# Vectors (i.e. homogenous lists)

# Creating
vec <- c(1, 2, 3) # 'c' for concatenate
stopifnot(c(1.1, 2.1, 3L) == c(1.1, 2.1, 3.0)) # int converted to double
stopifnot(c(1, "2", "3") == c("1", "2", "3")) # num converted to char
# colon operator 'from:to' (stepsize = 1)
stopifnot(1:3 == c(1,2,3))
stopifnot(3:1 == c(3,2,1))
stopifnot(1.5:4 == c(1.5,2.5,3.5))
# seq(from, to, by/length/along)
stopifnot(seq(1,3,0.5) == c(1.0, 1.5, 2.0, 2.5, 3.0)) # default is 'by'
stopifnot(seq(1,3,0.5) == seq(1,3,length=5))
stopifnot(seq(along=vec) == 1:length(vec)) # true for any vec
stopifnot(seq(3,10,along=vec) == seq(3,10,length=length(vec))) # true for any to, from, and vec
# rep(vec, times/each/length.out)
stopifnot(rep(c(1,2,3),            2) == c(1,2,3,1,2,3)) # default is 'times'
stopifnot(rep(c(1,2,3),       each=2) == c(1,1,2,2,3,3))
stopifnot(rep(c(1,2,3), length.out=7) == c(1,2,3,1,2,3,1)) 
# paste(**args, sep) - always transforms into strings
stopifnot(paste(1:3, 4:5, "X", sep=":") == c("1:4:X","2:5:X","3:4:X"))
# type constructors
len <- 3
stopifnot(integer(len)   == rep(0L, len))
stopifnot(double(len)    == rep(0, len))
stopifnot(numeric(len)   == rep(0, len))
stopifnot(complex(len)   == rep(0i, len))
stopifnot(character(len) == rep("", len))
stopifnot(logical(len)   == rep(FALSE, len))


# Indexing
vec <- 1:10
stopifnot(vec[1] == 1)
stopifnot(vec[c(1,3)] == c(1,3)) 
stopifnot(vec[1:3] == 1:3)
stopifnot(vec[-(1:3)] == 4:10) # negative index means exclude
#stopifnot(vec[9:12] == c(9,10,NA,NA)) # can't check NA
stopifnot(vec[vec > 7] == 8:10) # logical vector as index vector
stopifnot(vec[c(TRUE, FALSE)] == c(1,3,5,7,9)) # recycles logical vector

# Modifying
vec <- 1:10
vec[10] <- 11
vec[12] <- 12

stopifnot(length(vec) == 12 && is.na(vec[11]))
stopifnot(sort(10:1) == 1:10) # sort returns new vector

# Operators
stopifnot(1:3 + 1   == c(2,3,4))
stopifnot(1:3 + 3:1 == c(4,4,4))
stopifnot(1:3 + 6:1 == c(7,7,7,4,4,4)) # shorted vector "recycled"
suppressWarnings(
    # Vector lengths need not be multiples though warning will be printed
    # "longer object length is not a multiple of shorter object length"
    stopifnot(1:3 + 6:2 == c(7,7,7,4,4))
)
# Other arithmetic operators behave similarly: - * / ^ 
stopifnot((1:3 >= 2) == c(FALSE,TRUE,TRUE))

# Builtin arithmetic functions
stopifnot(sqrt(c(1,4,9,16)) == 1:4)
# an so on: log, exp, sin, cos, tan, etc...

# Built-in statistical functions
stopifnot(range(10:1) == c(1,10))
stopifnot( max(1:3, 4:2) == 4)
stopifnot( pmax(1:3, 4:2) == c(4,3,3)) # max per index
# and so on: sum, min, mean, var, sd, etc...

########################################
# Factors
# factors(vec)
# ordered(vec)
# levels(vec_factors)
# tapply()

########################################
# Arrays

########################################
# Matrices


# Creating
data <- c(1,2,3,4,5,6)
mtx <- matrix(data, nrow=2, ncol=3)
# > print(mtx)
#      [,1] [,2] [,3]
# [1,]    1    3    5
# [2,]    2    4    6

# Adding dimension names (aka headers)

# Attributes
# attributes(mtx)

# Indexing

# Modifying
# attr(mtx, "dim") <- c(10,10)

########################################
# Lists (a.k.a. maps)
lst <- list(key='val', int=1, dbl=1.1, str='A', bool=FALSE)
stopifnot(lst$key == 'val')

########################################
# Data Frames

# Creating
df <- data.frame(c('00','10'), c('01','11'))
#print(df)

# Indexing

################################################################################
# Flow Control 
################################################################################
# If-Then-Else
if (FALSE) {
    # code
} else if (FALSE) {
    # code
} else {
    stopifnot(TRUE)
}

# For Loop
for (x in 1:10) { }
mylist <- 1:10
for (x in mylist) { }

# While Loop
a <- 0
while (a < 10) {a <- a + 1}

################################################################################
# Functions
################################################################################
myfunc <- function(a, b=2, c=1) { return(a + b - c) }
stopifnot(myfunc(1,1,1) == 1)
stopifnot(myfunc(1) == 2)
stopifnot(myfunc(c=1, 2, b=3) == 4)

################################################################################
# S3 and S4
################################################################################

