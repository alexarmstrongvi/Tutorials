--------------------------------------------------------------------------------
-- Haskell Basics
--------------------------------------------------------------------------------
-- Raise exception if expression is false, otherwise do nothing
import qualified Control.Exception
assert = flip Control.Exception.assert (pure ())

-- Replace assert with below to see line number of raised exception
-- import Control.Exception (assert)
-- end = pure ()
-- Before: assert $ expr
-- After : assert (expr) end

--------------------------------------------------------------------------------
-- Literals
--------------------------------------------------------------------------------
myInt    = 65
myIntBin = 0b1000001
myIntOct = 0o101
myIntHex = 0x41
myFloat  = 1.2
myBool   = True
myChar   = 'c'
myString = "string"

-- Collections
myList = [1,2,3]
myPair = (1, '2')
myTuple = (1, '2', 3.0, "4.0")

--------------------------------------------------------------------------------
-- Operators (and related typeclass methods)
--------------------------------------------------------------------------------
demoOperators = do
    -- Boolean
    assert $ not False
    assert $ True && True
    assert $ False || True
    assert $ otherwise == True

    -- Equality (class Eq)
    assert $ 5 == 5
    assert $ 5 /= 6

    -- Ordered (class Ord)
    assert $ 5 <  6
    assert $ 5 <= 5
    assert $ 6 >  5
    assert $ 6 >= 6
    assert $ compare 5 6 == LT && compare 6 5 == GT && compare 5 5 == EQ
    assert $ max 5 6 == 6
    assert $ min 5 6 == 5

    -- Enumerable (class Enum)
    assert $ succ 1 == 2
    assert $ pred 2 == 1

    -- All numbers (class Num)
    assert $ 2 + 3       == 5
    assert $ 2 - 3       == -1
    assert $ 2 * 3       == 6
    assert $ negate 2    == -2
    assert $ abs (-2)    == 2
    assert $ signum (-2) == -1

    -- Rational (class Fractional)
    assert $ 4 / 2 == 2.0
    assert $ recip 2 == 0.5

    -- Real (class Floating)
    assert $ 2 ** 3 == 8.0
    -- pi,
    -- exp, log, sqrt, logBase,
    -- sin, cos, tan,
    -- asin, acos, atan,
    -- sinh, cosh, tanh,
    -- asinh, acosh, atanh

    -- Integers (class Integral)
    assert $ quot    (-9) 4 == -2
    assert $ rem     (-9) 4 == -1
    assert $ quotRem (-9) 4 == (-2,-1)
    assert $ div     (-9) 4 == -3
    assert $ mod     (-9) 4 == 3
    assert $ divMod  (-9) 4 == (-3,3)

    -- Other Numeric
    assert $ 2.5 ^ 2 == 6.25 -- Num ^ non-negative Integral [bad 2^(-3) or 2^pi]
    assert $ 2.0 ^^ (-2) == 0.25 -- Num ^^ Integral [bad: 2 ^^ pi]
    assert $ subtract 2 3 == 1 -- same as 3 - 2
    assert $ even 2
    assert $ odd 3
    assert $ gcd 20 15 == 5
    assert $ lcm 20 15 == 60

    -- List operators
    assert $ [1,2] ++ [3,4] == [1,2,3,4]
    assert $ "Hello" ++ " " ++ "World" == "Hello World"
    assert $ lex "  Hello World. I'm Haskell " == [("Hello", " World. I'm Haskell ")]

    -- Order of operations (the following is evaluated right to left)
    assert $ False || True && 6 == 5 + 4 / 2 ^ subtract 7 9

--------------------------------------------------------------------------------
-- Collections
--------------------------------------------------------------------------------
-- Creation
myRange         = [1..10]
myStepRange     = [1,3..10]
myInvStepRange  = [10,8..1]
myCharRange     = ['A'..'F'] -- ['Y'..'b']
myASCIIRange    = ['\NUL'..'\DEL'] -- ['\0'..'\127']
myConstantRange = replicate 4 'A' -- ['A', 'A', 'A', 'A']
myInfRange1     = [1..]
myInfRange2     = repeat 4 -- [4,4,..]
myInfRange3     = iterate (2-) 4 -- [4, 2-4, 2-(2-4), 2-(2-(2-4)), ...]
myInfRange4     = cycle [1,2,3] -- [1,2,3,1,2,3,1,2, ...]

demoListComprehension = do
    assert $ [x+1     | x <- [1,2]]                    == [2,3]
    assert $ [(x,-x)  | x <- [1,2]]                    == [(1,-1), (2,-2)]
    assert $ [x       | x <- [1..100], x <= 2]         == [1,2]
    assert $ [(x,y)   | x <- [1,2], y <- [3,4]]        == [(1,3),(1,4),(2,3),(2,4)]
    assert $ [[x,-x,y]| x <- [1,3], y <- [2,4], x > y] == [[3,-3,2]]
jack and jill 
demoListFunctions = do
    -- Properties
    assert $ length [1,2,3] == 3
    assert $ maximum [3,5,2] == 5
    assert $ minimum [3,5,2] == 2
    assert $ null [] == True
    assert $ or [False, True, False] == True
    assert $ and [False, True, False] == False
    assert $ elem 3 [1..5] == True
    assert $ notElem 3 [1..5] == False -- useful for infinite lists
    assert $ lookup 3 [(1,'A'), (3,'B')] == Just 'B'
    assert $ any even [1,2,3,4] == True
    assert $ all even [1,2,3,4] == False

    -- Access
    assert $ [5,3,1] !! 1 == 3
    assert $ head [5,3,1] == 5
    assert $ tail [5,3,1] == [3,1]
    assert $ init [5,3,1] == [5,3]
    assert $ last [5,3,1] == 1
    assert $ take 3 [1,2,3,4,5] == [1,2,3]
    assert $ drop 3 [1,2,3,4,5] == [4,5]
    assert $ takeWhile (<=3) [2,3,4,0,1] == [2,3]
    assert $ dropWhile (<=3) [2,3,4,0,1] == [4,0,1]

    -- Concatenate and Join
    let list = [3,4]
    assert $ list ++ [5,6] == [3,4,5,6]
    assert $ [1,2] ++ list == [1,2,3,4]
    assert $ 0 : list == [0,3,4]
    assert $ 0 : 1 : 2 : list == [0,1,2,3,4]
    assert $ concat [[1,2], [3], [4,5]] == [1,2,3,4,5]
    assert $ zip [1,2,3] [4,5,6] == [(1,4),(2,5),(3,6)]
    
    -- Split
    assert $ splitAt 2  [2,3,4,0,1] == ([2,3], [4,0,1])
    assert $ span (<=3) [2,3,4,0,1] == ([2,3], [4,0,1])
    assert $ break (>3) [2,3,4,0,1] == ([2,3], [4,0,1])

    -- Transform
    assert $ map (*2) [1,2,3] == [2,4,6]
    assert $ filter even [1..5] == [2,4]
    assert $ reverse [1,2,3] == [3,2,1]

    -- Reduce
    assert $ sum     [3,5,2] == 10
    assert $ product [3,5,2] == 30
    assert $ foldl (-) 0 [1,2,3] == (((0 - 1) - 2) - 3)
    assert $ foldr (-) 0 [1,2,3] == (1 - (2 - (3 - 0))) 
    assert $ foldl1 (-) [1,2,3] == ((1 - 2) - 3)
    assert $ foldr1 (-) [1,2,3] == (1 - (2 - 3)) 

    -- Derive lists
    assert $ scanl (-) 0 [1,2,3] == [0, 0-1, (0-1)-2, ((0-1)-2)-3]
    assert $ scanr (-) 0 [1,2,3] == [1-(2-(3-0)), 2-(3-0), 3-0, 0]
    assert $ scanl1 (-) [1,2,3] == [1, 1-2, (1-2)-3]
    assert $ scanr1 (-) [1,2,3] == [1-(2-3), 2-3, 3]
    assert $ concatMap (take 2) [[1..], [10..], [100..]] == [1,2,10,11,100,101]
    assert $ zipWith (+) [1, 2, 3] [4, 5, 6] == [5,7,9]
    assert $ unzip [(1,4),(2,5),(3,6)] == ([1,2,3], [4,5,6])
    
    -- Strings
    assert $ lines "Line1\nLine2" == ["Line1", "Line2"]
    assert $ unlines ["Line1", "Line2"] == "Line1\nLine2\n"
    assert $ words "Word1 Word2\n Word3" == ["Word1","Word2","Word3"]
    assert $ unwords  ["Word1","Word2","Word3"] == "Word1 Word2 Word3"

demoTupleFunctions = do
    -- Access
    assert $ fst (5,'A') == 5
    assert $ snd (5,'A') == 'A'

-- demoFoldAndTraversalFunctions = do
    -- Foldable
    -- foldMap
    
    -- Traversable
    -- traverse
    -- sequenceA
    -- mapM
    -- sequence

-- Data.Dict

----------------------------------------
-- Functions
----------------------------------------
myAdd a b = a + b

numPatternMatching 0 = 0
numPatternMatching 1 = 1
numPatternMatching x = numPatternMatching(x - 1) + numPatternMatching(x - 2)

listPatternMatching [] = "0 elements"
listPatternMatching [x] = "1 element"
listPatternMatching [x,y] = "2 elements"
-- listPatternMatching (x:y:[]) = "2 elements"
listPatternMatching (x:xs) = "1+ elements"
-- listPatternMatching (x:y:xs) = "2+ elements"
-- listPatternMatching (x0:xs@(x1:_)) = "2+ elements. y elem xs"

funcGuards x
  | x == 0 = 0
  | x == 1 = 1
  | otherwise = funcGuards (x - 1) + funcGuards (x - 2)

-- TODO: Pattern Matching
    -- (&) as-patterns; var@pattern
    -- mixing guards and pattern matching

myAnonymousFuncResult = map (\x -> x ^ x) [1..3]

-- `where` - like in SQL
whereFunc x y
    | x / y <= 10          = "foo" -- no use of where expressions
    | ratio <= upperLimit  = "bar" -- use where expressions
    | otherwise            = "baz"
    where
        ratio      = x / y
        upperLimit = 30

-- TODO: let .. in

-- Composition

-- curry and uncurry

-- Common functions
-- zip, zipWith
-- scanl, scanr
-- replicate
-- splitAt
-- findIndex
-- sort, sortBt, sortOn, comparing, on
-- id
-- const
-- flip
-- until
-- asTypeOf
-- error
-- errorWithoutStackTrace
-- undefined
-- seq
-- ($!)

--------------------------------------------------------------------------------
-- User types
--------------------------------------------------------------------------------
-- Record syntax
data MyType = MyType {
    name :: String,
    x :: Float,
    y :: Float
}
-- Multiple value constructors
data MyEnum = Red | Blue | Green

-- Multiple value constructors with multiple fields (no record syntax)
data MyVector =
    -- Value constructors for all possible values of type
      Vector2D Float Float
    | Vector3D Float Float Float
    | Vector4D Float Float Float Float

-- demoEnum = do
--     let x = Red
--     assert $ x == Red

-- Instantiating data types
myInstance = MyType {name = "test", x = 1.1, y = 2.2}
myEnum     = Red
myVector   = Vector3D 3.1 4.1 5.1

-- Composite types
-- data Maybe a = Nothing | Just a
myOptionalVal1 = Just 5 
myOptionalVal2 = Nothing

squareWithDefault1 :: Maybe Int -> Int
squareWithDefault1 (Just x) = x^2
squareWithDefault1 Nothing = 0

-- More easily define myOptionalFunc1 with 'maybe' function
squareWithDefault2 = maybe 0 (^2) 

demoOptionalValues = do
    assert $ squareWithDefault1 (Just 5) == 5^2
    assert $ squareWithDefault1 Nothing == 0
    assert $ squareWithDefault2 (Just 5) == 5^2
    assert $ squareWithDefault2 Nothing == 0


-- data Either a b = Left a | Right b
myEitherVal1 = Left 5
myEitherVal2 = Right 'A'

myEitherFunc1 :: Either String Float -> Int
myEitherFunc1 (Left s) = length s
myEitherFunc1 (Right f) = round f
-- More easily define myEitherFunc with either
myEitherFunc2 = either length round

demoEither = do
    assert $ myEitherFunc1 (Left "Hello") == 5
    assert $ myEitherFunc1 (Right pi) == 3
    assert $ myEitherFunc2 (Left "Hello") == 5
    assert $ myEitherFunc2 (Right pi) == 3

--------------------------------------------------------------------------------
-- Type system
--------------------------------------------------------------------------------
-- Specified types
mySignedInt   :: Int      = -(2^63)
myUnsignedInt :: Word     = 2^64 - 1
myBigInt      :: Integer  = 2^100     -- Arbitrary precision integer
myFloat32     :: Float    = 3.14
myDouble64    :: Double   = 3.15
myRational    :: Rational = 0.1 + 0.2 -- Arbitrary precision rational
-- warning: [-Woverflowed-literals]
-- -9223372036854775809 :: Int -- 'Literal X is out of the Int range'

demoTypeConversion = do
    ---------------------------------------- 
    -- Integral <-> Num (fromInteger, toInteger, fromIntegral)
    ---------------------------------------- 
    let xInteger :: Integer = 2^100     
    assert $ (fromInteger xInteger :: Int) == 0 -- to Integral then Int [modulo wrapping]
    assert $ (fromInteger xInteger :: Word) == 0 -- to Integral then Word [modulo wrapping]
    -- Error: x / 2 -> No instance for (Fractional Int) arising from a use of ‘/’
    assert $ (fromInteger xInteger / 2) == 2^99 -- to Fractional then Double
    assert $ sqrt (fromInteger xInteger) == 2^50 -- to Floating then Double

    let xInt  :: Int  = -(2^63)
    let xWord :: Word = 2^64 - 1
    assert $ toInteger xInt * 2 == -(2^64)
    assert $ toInteger xWord + 1 == 2^64

    -- fromIntegral is defined as fromInteger . toInteger
    assert $ fromIntegral xInt == (fromInteger . toInteger) xInt

    ---------------------------------------- 
    -- Num -> Rational (toRational)
    ---------------------------------------- 
    let int10 :: Int = 10
    assert $ 1 / toRational int10 + 2 / toRational int10 == 0.3
    assert $ 1 / fromIntegral int10 + 2 / fromIntegral int10 /= 0.3 -- to Fractional Double
    let dbl10 :: Double = 10
    assert $ 1 / dbl10 + 2 / dbl10 /= 0.3
    assert $ 1 / toRational dbl10 + 2 / toRational dbl10 == 0.3

    ---------------------------------------- 
    -- Rational -> Fractional (fromRational)
    ---------------------------------------- 
    -- fromRational
    let x :: Rational = 1/3
    -- Error: sin x -> No instance for (Floating Rational)
    assert $ sin (fromRational x) >= -1

    ---------------------------------------- 
    -- Show -> String (show)
    ---------------------------------------- 
    assert $ show 1 == "1"
    assert $ show (1/3) == "0.3333333333333333"
    assert $ show 'A' == "'A'"
    assert $ show "String" == "\"String\""
    -- showsPrec, shows
    -- showList, showChar, showString, showParen

    ---------------------------------------- 
    -- String -> Read (read)
    ---------------------------------------- 
    assert $ (read "1" :: Int) == 1
    assert $ (read "1" :: Float) == 1.0
    assert $ (read "3.14" :: Double) == 3.14
    assert $ (read "'A'" :: Char) == 'A'
    assert $ (read "\"String\"" :: String) == "String"
    -- readsPrec, reads
    -- readList, readParen

    
    ---------------------------------------- 
    -- Enum <-> Int
    ---------------------------------------- 
    assert $ fromEnum True == 1
    assert $ fromEnum 'A'  == 65
    assert $ fromEnum EQ   == 1
    assert $ fromEnum 1.9  == 1
    assert $ fromEnum 2.1  == 2

    assert $ (toEnum 0  :: Bool)     == False
    assert $ (toEnum 66 :: Char)     == 'B'
    assert $ (toEnum 0  :: Ordering) == LT
    assert $ (toEnum 2  :: Float)    == 2.0

    assert $ enumFrom EQ == [EQ ..]
    assert $ enumFromTo 'a' 'z' == ['a'..'z']
    assert $ enumFromThen LT GT == [LT, GT ..]
    assert $ enumFromThenTo 1 3 10 == [1,3..10]

--------------------------------------------------------------------------------
-- Semigroups and Monoids
--------------------------------------------------------------------------------
-- class Semigroup a where
--     (<>) :: a -> a -> a
--     sconcat :: 
--     {-# MINIMAL (<>) | sconcat #-}

demoSemigroups = do
    -- Lists: semigroup under concatenation
    -- instance Semigroup [a] where
    --     (<>) = (++)
    assert $ [1,2] <> [3,4] == [1,2,3,4]
    assert $ mySemigroupFunc [1,2] [3] [4,5] == [1,2,3,4,5]

    -- Either: semigroup under 'evaluate to 1st input unless it is a Left type'
    -- instance Semigroup (Either a b) where
    --     Left _ <> b = b 
    --     a      <> _ = a
    assert $ Left 1 <> Left 2 <> Right '3' <> Right '4' <> Left 5 == Right '3'

mySemigroupFunc :: (Semigroup a) => a -> a -> a -> a
mySemigroupFunc x y z = x <> (y <> z)


demoMonoids = do
    -- Lists - monoid under concatenation with empty list as identity element
    -- instance Monoid [a] where
    --     mempty  = []
    --     mconcat xss = [x | xs <- xss, x <- xs]
    assert $ mempty <> [1, 2] <> mempty == [1, 2]
    assert $ mconcat [[1,2], [3], [4,5]] == [1,2,3,4,5]
    assert $ myMonoidFunc [1,2] == [1,2,1,2]
    
    assert $ myMonoidFunc [1,2] == [1,2,1,2]

myMonoidFunc :: (Monoid a) => a -> a
myMonoidFunc x = mconcat [x, mempty, x <> mempty]

--------------------------------------------------------------------------------
-- Functors, Foldables, and Traversables
--------------------------------------------------------------------------------
demoFunctors = do
    -- fmap
    assert $ fmap (2*) [1,2,3] == [2,4,6]    
    assert $ fmap (2*) (Just 3) == Just 6
    assert $ fmap (2*) Nothing == Nothing
    assert $ fmap (2*) (Left 3) == Left 3
    assert $ fmap (2*) (Right 3 :: Either String Int) == Right 6
    assert $ fmap (2*) ('A', "B", 3.1, 3) == ('A', "B", 3.1, 6)

    -- (<$>) == `fmap` but with lower precedence
    assert $ ((2*) <$> [1,2,3]) == [2,4,6] 

    -- (<$)
    assert $ ("Hi" <$ [1,2,3]) == ["Hi", "Hi", "Hi"]

    assert $ myFunctorFunc (Just 3) == Just "Hi"

myFunctorFunc :: (Functor f) => f Int -> f String
myFunctorFunc x = "Hi" <$ fmap (2*) x

-- demoFoldables
-- demoTraversables

--------------------------------------------------------------------------------
-- Monads and Applicative Functors
--------------------------------------------------------------------------------
-- Applicative Functors
demoApplicatives = do
    -- Mapping over functors with functors of functions
    assert $ ((*) <$> Just 2 <*> Just 3) == Just 6
    assert $ (Just (2*) <*> Just 3)      == Just 6
    assert $ (Just (2*) <*> Nothing)     == Nothing
    assert $ (pure 3 :: Maybe Int)       == Just 3
    assert $ (pure (*) <*> Just 2 <*> Just 3) == Just 6
    assert $ (Just (2*)  *> Just 3)      == Just 3
    assert $ (Just  2   <*  Just 3)      == Just 2

    assert $ ([(2*), (2+)] <*> [1,3]) == [2*1, 2*3, 2+1, 2+3]

    assert $ myApplicativeFunc (Just (^)) (Just 3) 2 == Just 9
    assert $ myApplicativeFunc Nothing (Just 3) 2 == (Nothing :: Maybe ())
    assert $ myApplicativeFunc [(++)] ["AB", "CD"] "EF" == ["ABEF","CDEF"]

myApplicativeFunc :: (Applicative f) => f (a -> a -> b) -> f a -> a -> f b
myApplicativeFunc func x y = func <*> x <*> pure y  

-- Monads
maybeSqrt :: Float -> Maybe Float
maybeSqrt x = if x >= 0 then Just (sqrt x) else Nothing

maybeInvert :: (Fractional a, Ord a) => a -> Maybe a
maybeInvert x = if x /= 0 then Just (1 / x) else Nothing

ascii = ['\0'..'\255']
idxToASCII = flip lookup (zip [0..] ascii)
asciiToIdx = flip lookup (zip ascii [0..])

demoMonads = do
    assert $ maybeSqrt 4    == Just 2
    assert $ maybeSqrt (-1) == Nothing
    assert $ maybeInvert 2  == Just 0.5
    assert $ maybeInvert 0  == Nothing
    assert $ asciiToIdx 'B'  == Just 66
    assert $ idxToASCII 66   == Just 'B'
    assert $ idxToASCII 999  == Nothing

    assert $ (Just 0.25 >>= maybeInvert >>= maybeSqrt)  == Just 2
    assert $ (Just (-5) >>= maybeInvert >>= maybeSqrt)  == Nothing
    assert $ (Just 0    >>= maybeInvert >>= maybeSqrt)  == Nothing
    assert $ (Nothing   >>= maybeInvert >>= maybeSqrt)  == Nothing
    assert $ (Just 66   >>= idxToASCII  >>= asciiToIdx) == Just 66
    assert $ (Just 999  >>= idxToASCII  >>= asciiToIdx) == Nothing
    assert $ (Nothing   >>= idxToASCII  >>= asciiToIdx) == Nothing

    assert $ (return 3 :: Maybe Int) == (pure 3 :: Maybe Int) -- return = pure
    assert $ (return 3 :: Maybe Int) == Just 3

    assert $ myMonadFunc (Just 16) maybeSqrt == Just 2

    
myMonadFunc :: (Monad m) => m a -> (a -> m a) -> m a
myMonadFunc x f = x >>= f >> x >>= f >>= return >>= f

--------------------------------------------------------------------------------
-- IO
--------------------------------------------------------------------------------
myIOAction = putStrLn "Demoing IO" -- Nothing printed to stdout

demoIO = do
    myIOAction -- Now putStrLn IO action is executed
    -- putChar, putStr
    print (1 + 2 == 3) -- print defined as (putStrLn . show)

    -- TODO: Why does the >>= syntax cause the second getLine to be skipped
    -- putStrLn "Enter a character: "
    -- let c = getChar
    -- c >>= (putStrLn . ("You entered: " ++) . show)

    putStrLn "Enter a line: "
    l <- getLine -- Simpler way of doing l = getLine; l >>= 
    putStrLn ("You entered: " ++ l)
    

    -- getContents
    -- interact

    putStrLn "Done demoing IO"

--------------------------------------------------------------------------------
-- Other
--------------------------------------------------------------------------------
-- Modules
    -- Data.List
        -- group
    -- System.Random

--------------------------------------------------------------------------------
main = do
    putStrLn "main START"
    demoOperators
    demoListComprehension
    demoListFunctions
    demoTupleFunctions
    demoTypeConversion
    demoSemigroups
    demoMonoids
    demoFunctors
    -- demoFoldables
    -- demoTraversables
    demoApplicatives
    demoMonads
    demoIO
    putStrLn "main END"
