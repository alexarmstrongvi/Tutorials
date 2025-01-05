--------------------------------------------------------------------------------
-- Prelude
-- https://hackage.haskell.org/package/base-4.18.0.0/docs/Prelude.html
--------------------------------------------------------------------------------
----------------------------------------
-- Basic data types
----------------------------------------

data Bool
(&&)
(||)
not
otherwise

data Maybe a
maybe

data Either a b
either

data Ordering -- = LT | EQ | GT

data Char
type String = [Char]

----------------------------------------
-- Tuples
----------------------------------------
fst
snd
curry
uncurry

----------------------------------------
-- Basic type classes
----------------------------------------
class Eq a where
(==)
(/=)

class Eq a => Ord a where
compare
(<)
(<=)
(>)
(>=)
max
min

class Enum a where
succ
pred
toEnum
fromEnum
enumFrom
enumFromThen
enumFromTo
enumFromThenTo

class Bounded a where
minBound
maxBound

----------------------------------------
-- Numbers
----------------------------------------
-- Numeric types
data Int
data Integer
data Float
data Double
type Rational = Ratio Integer
data Word

-- Numeric type classes
class Num a where
(+)
(-)
(*)
negate
abs
signum
fromInteger

class (Num a, Ord a) => Real a where
toRational

class (Real a, Enum a) => Integral a where
quot
rem
div
mod
quotRem
divMod
toInteger

class Num a => Fractional a where
(/)
recip
fromRational

class Fractional a => Floating a where
pi
exp
log
sqrt
(**)
logBase
sin
cos
tan
asin
acos
atan
sinh
cosh
tanh
asinh
acosh
atanh

-- Numeric functions
subtract
even
odd
gcd
lcm
(^)
(^^)
fromIntegral

-- Semigroup and Monoids
class Semigroup a where
(<>)

class Semigroup a => Monoid a where
mempty
mappend
mconcat

class Functor f where
fmap
(<$)
(<$>)

class Functor f => Applicative f where
pure
(<*>)
liftA2
(*>)
(<*)

class Applicative m => Monad m where
(>>=)
(>>)
return

class Monad m => MonadFail m where
fail
mapM_
sequence_
(=<<)

-- Folds and Traversals
class Foldable t where
foldMap
foldr
foldl
foldr1
foldl1
elem
maximum
minimum
sum
product

class (Functor t, Foldable t) => Traversable t where
traverse
sequenceA
mapM
sequence

-- Miscellaneous functions
id
const
(.)
flip
($)
until
asTypeOf
error
errorWithoutStackTrace
undefined
seq
($!)

-- List operations
map
(++)
filter
head
last
tail
init
(!!)
null
length
reverse
and
or
any
all
concat
concatMap

-- Building lists
scanl
scanl1
scanr
scanr1
iterate
repeat
replicate
cycle

-- Sublists
take
drop
takeWhile
dropWhile
span
break
splitAt

-- Searching lists
notElem
lookup

-- Zipping and unzipping
zip
zip3
zipWith
zipWith3
unzip
unzip3

-- Functions on strings
lines
words
unlines
unwords

-- Converting to and from strings
type ShowS = String -> String

class Show a where
showsPrec
show
showList
shows
showChar
showString
showParen

type ReadS a = String -> [(a, String)]

class Read a where
readsPrec
readList
reads
readParen
read
lex

-- Basic IO
data IO a
putChar
putStr
putStrLn
print
getChar
getLine
getContents
interact

type FilePath = String
readFile
writeFile
appendFile
readIO
readLn

type IOError = IOException
ioError
userError
