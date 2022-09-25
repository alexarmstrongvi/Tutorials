////////////////////////////////////////////////////////////////////////////////
// Resources
// - https://hackingcpp.com/cpp/std/algorithms.html
////////////////////////////////////////////////////////////////////////////////
#include "containers.h"

#include <algorithm>
using std::all_of, std::any_of, std::none_of;
using std::count, std::count_if;
using std::find, std::find_if, std::find_if_not, std::find_first_of;

using std::equal;
using std::mismatch;
using std::lexicographical_compare;

using std::binary_search;
using std::lower_bound;
using std::upper_bound;
using std::equal_range;
using std::includes;

using std::min_element, std::max_element, std::minmax_element;
using std::min, std::max, std::minmax, std::clamp;

using std::is_sorted, std::is_sorted_until;
using std::is_partitioned;
using std::partition_point;
using std::is_permutation;
using std::is_heap, std::is_heap_until;

using std::copy, std::copy_n, std::copy_backward, std::copy_if;
using std::move, std::move_backward;

using std::distance;
using std::for_each, std::for_each_n;
using std::sort;

#include <vector>
using std::vector;
#include <utility>
using std::pair;
#include <cstdio> // printf
#include <iostream>
using std::cout;

/* NOTES
- Algorithms generally follow the signatures 
    algo(InputIt first, InputIt last, Predicate p)
- Predicate is an object that takes in arguments and returns a boolean
    - UnaryPredicate takes in 1 argument while BinaryPredicate takes in 2
    - The object can be a function pointer or functors (a.k.a. function class)
- Many of the using statements above for the algorithm library are not necessary
  because argument-dependent lookup will cause the linker to look in the std
  namespace for function name given that the vector iterator arguments are
  already in the std namespace. I include them anyway for clarity and
  portability.
*/

void non_modifiying_operations();
void copying_moving_swapping_elements();
void reordering_elements();
void modifiying_elements();
void numeric_operations();
void range_and_iterator_utilties();

// Predicate objects
// function pointers
bool isEvenFunction(const int i) {return i%2==0;}
bool (*isEvenLambda)(const int) = [](int i) {return i%2==0;};
// functors (a.k.a. function classes)
struct IsEvenFunctor {
    bool operator() (const int i) const {return i%2==0;}
};
struct LessThan {
    const int n;
    LessThan(int val) : n {val} {}
    bool operator() (const int i) const {return i < n;}
};

int main() {
    // printf("Running stl_algorithms\n");
    // Types of predicate objects
    {
    vector<int> c {-2,0,4};
    assert(all_of(c.cbegin(), c.cend(), isEvenFunction ));
    assert(all_of(c.cbegin(), c.cend(), isEvenLambda ));
    assert(all_of(c.cbegin(), c.cend(), [](int i){return i%2==0;} ));
    assert(all_of(c.cbegin(), c.cend(), IsEvenFunctor()));
    }

    non_modifiying_operations();
    copying_moving_swapping_elements();
    reordering_elements();
    modifiying_elements();
    numeric_operations();
    range_and_iterator_utilties();
    
    return 1;
}

void non_modifiying_operations() {
    ////////////////////////////////////////////////////////////////////////////
    // Existence queries
    ////////////////////////////////////////////////////////////////////////////
    {
    vector<int> container {-2, 0, 4, 4, 4, 100};
    auto cb = container.cbegin();
    auto ce = container.cend();
    auto isEven = [](const int i){return i%2==0;};
    auto isOdd  = [](const int i){return i%2==1;};

    assert(  all_of(cb, ce, isEven));
    assert(  any_of(cb, ce, isEven));
    assert( none_of(cb, ce,  isOdd));
    assert(   count(cb, ce,      4) == 3);
    assert(count_if(cb, ce, isEven) == 6);
    }

    ////////////////////////////////////////////////////////////////////////////
    // Finding/Locating Elements
    ////////////////////////////////////////////////////////////////////////////
    {
    vector<int> container {-2,0,4,6,10};
    auto cb = container.cbegin();
    auto ce = container.cend();

    // Finding single elements
    // find()
    // find_if()
    // find_if_not()
    vector<int> t1 {4, 5, 6};
    const auto result = find_first_of(cb, ce, t1.cbegin(), t1.cend());
    assert(*result == 4);

    // Finding consecutive runs of elements
    // adjacent_find()
    // search_n()

    // Find subranges
    // search()
    // find_end()
    }

    ////////////////////////////////////////////////////////////////////////////
    // Comparing ranges
    ////////////////////////////////////////////////////////////////////////////
    {
    vector<int> container {1,2,3};
    auto cb = container.cbegin();
    auto ce = container.cend();
    
    assert(equal(cb, ce, cb));
    assert(equal(cb, ce, cb, ce));

    pair<vector<int>::const_iterator, vector<int>::const_iterator> result;
    vector<int> t {1,4,3};
    result = mismatch(cb,ce,t.cbegin(), t.cend());
    assert(*result.first == 2 && *result.second == 4);

    assert(lexicographical_compare(cb, ce, t.cbegin(), t.cend()));
    }

    ////////////////////////////////////////////////////////////////////////////
    // Binary Search of Sorted Ranges
    ////////////////////////////////////////////////////////////////////////////    ////////////////////////////////////////////////////////////////////////////
    {
    vector<int> container {0,2,4,6,8,8,8,10};
    auto cb = container.cbegin();
    auto ce = container.cend();

    assert(
       binary_search(cb, ce, 4)
    && *lower_bound(cb, ce, 5) == 6
    && *upper_bound(cb, ce, 5) == 6
    && *lower_bound(cb, ce, 4) == 4
    && *upper_bound(cb, ce, 4) == 6
    );
    pair<vector<int>::const_iterator, vector<int>::const_iterator> result;
    result = equal_range(cb, ce, 8);
    int idx = distance(cb, result.first);
    int range_size = distance(result.first, result.second);
    assert(
       *result.first == 8 
    && *result.second == 10
    && idx == 4 
    && range_size == 3
    );

    vector<int> t1 {2,6,8};
    vector<int> t2 {2,5,8};
    assert(
        includes(cb, ce, t1.cbegin(), t1.cend())
    && !includes(cb, ce, t2.cbegin(), t2.cend())
    );
    }
    ////////////////////////////////////////////////////////////////////////////
    // Minimum / Maximum
    ////////////////////////////////////////////////////////////////////////////
    {
    vector<int> container {0,2,4,6,8,8,8,10};
    auto cb = container.cbegin();
    auto ce = container.cend();
    // min_element(cb, ce)
    // max_element(cb, ce)
    pair<vector<int>::const_iterator, vector<int>::const_iterator> result;
    result = minmax_element(cb, ce);
    assert(*result.first == 0 && *result.second == 10);

    assert(
        min(1,2) == 1
     && min({1,2,3}) == 1
     && max(1,2) == 2
     && max({1,2,3}) == 3
     && minmax(2,1).first == 1
     && minmax({3,2,1}).second == 3
     && clamp(5,1,3) == 3
     && clamp(-5,1,3) == 1
    );
    }
    ////////////////////////////////////////////////////////////////////////////
    // Structural Properties
    ////////////////////////////////////////////////////////////////////////////
    {
    vector<int> container {1,2,4,3};
    auto cb = container.cbegin();
    auto ce = container.cend();
    vector<int> t {3,4,1,2};
    LessThan is_less_than_3(3);
    assert(
        !is_sorted(cb,ce)
     //&& *is_sorted_until(cb,ce) == 4
     && is_partitioned(cb, ce,is_less_than_3)
     && *partition_point(cb,ce,is_less_than_3) == 4
     && is_permutation(cb,ce, t.cbegin())
    );
    // is_heap(cb,ce, );
    // is_heap_until(cb,ce, );
    }
    ////////////////////////////////////////////////////////////////////////////
    // Traversing Ranges
    ////////////////////////////////////////////////////////////////////////////
    {
    // for_each(cb, ce, )
    // for_each_n(cb, 3)
    // next(cb, 2)
    // prev(cb, 2)
    }
}

void copying_moving_swapping_elements() {
    ////////////////////////////////////////////////////////////////////////////
    // Copy
    ////////////////////////////////////////////////////////////////////////////
    {
    vector<int> container {1,2,3,4,5};
    auto cb = container.cbegin();
    auto ce = container.cend();
    vector<int> t(container.size()+1, -1);
    copy(cb, ce, t.begin());
    assert(equal(cb, ce, t.cbegin(), t.cend()-1));
    // copy_n
    // copy_backward
    // copy_if
    }
    
    ////////////////////////////////////////////////////////////////////////////
    // Move
    ////////////////////////////////////////////////////////////////////////////
    {
    vector<int> container {1,3,5,7,9,11};
    auto cb = container.begin();
    auto ce = container.end();
    vector<int> t(container.size(),0);
    printf("Move\n");
    printf("Before: %s -> %s\n", to_string(container).c_str(), to_string(t).c_str());
    move(cb, ce, t.begin());
    printf("After : %s -> %s\n", to_string(container).c_str(), to_string(t).c_str());
    // move_backward(cb, ce, );
    }


    ////////////////////////////////////////////////////////////////////////////
    // Sampling
    ////////////////////////////////////////////////////////////////////////////
    // sample(cb, ce, );

    ////////////////////////////////////////////////////////////////////////////
    // Swapping
    ////////////////////////////////////////////////////////////////////////////
    // iter_swap(cb, ce, );
    // swap_ranges(cb, ce, );
};
void reordering_elements() {

};
void modifiying_elements() {

};
void numeric_operations() {

};
void range_and_iterator_utilties() {

};
////////////////////////////////////////////////////////////////////////////
// Unsorted
////////////////////////////////////////////////////////////////////////////

// mismatch()
// auto print = [](const int i){printf("%d, ", i);};
// for_each(c.cbegin(), c.cend(), print);
// printf("\n");
// for_each_n(c.cbegin(), 2, print);
// printf("\n");

// vector<int> vec {1,3,2,4,3,5,4,6};
// sort(vec.begin()+3, vec.end());
// for (int i : vec) { printf("%d, ", i);}