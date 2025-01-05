-- import qualified Data.List
import qualified Data.List.NonEmpty
import Data.List.NonEmpty (NonEmpty, NonEmpty( (:|) ) )
import Data.Semigroup (sconcat, stimes)
-- import qualified Data.Monoid
-- import qualified Data.Functor
-- import qualified Data.Foldable

import qualified Control.Exception
assert = flip Control.Exception.assert (pure () :: IO ())

--------------------------------------------------------------------------------
-- Semigroup
--------------------------------------------------------------------------------
mySemigroupFunc :: (Semigroup a) => NonEmpty a -> a -> a
mySemigroupFunc xss x = stimes 2 (x <> sconcat xss)

demoSemigroups = do
    -- Lists
    let nonEmptyList = [3,4] :| [[5,6], [7]]
    assert $ mySemigroupFunc nonEmptyList [1,2] == [1..7] ++ [1..7]

    ---------------------------------------- 
    -- Semigroups that are not Monoids
    ---------------------------------------- 
    -- Either a b
    let nonEmptyEither = Left 'A' :| [Right 1, Right 2]
    assert $ mySemigroupFunc nonEmptyEither (Left 'B') == Right 1
    
    -- NonEmpty a
    let x = Data.List.NonEmpty.fromList [1,2]
    let y = Data.List.NonEmpty.fromList [3,4]
    let xy = Data.List.NonEmpty.fromList [x,y]
    assert $ mySemigroupFunc xy x == 1 :| [2,1,2,3,4,1,2,1,2,3,4]

    -- Void
    -- Bits a => Semigroup (And a)
    -- Ord a => Semigroup (Max a)
    -- Ord a => Semigroup (Min a)
    
--------------------------------------------------------------------------------
-- Monoid
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
main = do
    putStrLn "main START"
    demoSemigroups
    putStrLn "main END"
