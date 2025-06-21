////////////////////////////////////////////////////////////////////////////////
// Resources
// - https://en.cppreference.com/w/cpp/algorithm
//     - https://en.cppreference.com/w/cpp/algorithm/ranges
// - https://en.cppreference.com/w/cpp/ranges
// - https://hackingcpp.com/cpp/std/algorithms.html
////////////////////////////////////////////////////////////////////////////////
#include <algorithm>
// Available as either normal or constrained algorithms
namespace ranges = std::ranges;
using ranges::all_of, ranges::any_of, ranges::none_of;
using ranges::find, ranges::find_if, ranges::find_if_not;
using ranges::find_end;
using ranges::find_first_of;
using ranges::adjacent_find;
using ranges::count, ranges::count_if;
using ranges::mismatch;
using ranges::equal;
using ranges::search;
using ranges::search_n;


using ranges::lexicographical_compare;

using ranges::binary_search;
using ranges::lower_bound;
using ranges::upper_bound;
using ranges::equal_range;
using ranges::includes;

using ranges::min_element, ranges::max_element, ranges::minmax_element;
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

// Only normal algorithm


// Only constrained algorithms
using ranges::contains, ranges::contains_subrange;
using ranges::find_last, ranges::find_last_if, ranges::find_last_if_not;
using ranges::starts_with, ranges::ends_with;

#include <array>
using std::array;
#include <vector>
using std::vector;
#include <utility>
using std::pair;
#include <cstdio> // printf
#include <iostream>
using std::cout;
#include <cassert>
#include <initializer_list>
using std::initializer_list;

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
constexpr bool isEvenFunction(const int i) {return i%2==0;}
constexpr bool (*isEvenLambda)(const int) = [](int i) {return i%2==0;};
// functors (a.k.a. function classes)
struct IsEvenFunctor {
    constexpr bool operator() (const int i) const {return i%2==0;}
};
struct LessThan {
    const int n;
    LessThan(int val) : n {val} {}
    bool operator() (const int i) const {return i < n;}
};

int main() {
    printf("Running stl_algorithms\n");
    // Types of predicate objects
    {
    constexpr array<int, 4> range {-2,0,4};
    static_assert(all_of(range, isEvenFunction ));
    static_assert(all_of(range, [](int i){return i%2==0;} ));
    static_assert(all_of(range, isEvenLambda ));
    static_assert(all_of(range, IsEvenFunctor()));
    }

    non_modifiying_operations();
    copying_moving_swapping_elements();
    reordering_elements();
    modifiying_elements();
    numeric_operations();
    range_and_iterator_utilties();

    // // Execution policies (C++17)
    // is_execution_policy
    // execution::seq execution::par execution::par_unseq execution::unseq
    // execution::sequenced_policy
    // execution::parallel_policy
    // execution::parallel_unsequenced_policy
    // execution::parallel_unsequenced
    
    // // C library
    // qsort
    // bsearch
    
    // // Operations on uninitialized memory
    // uninitialized_copy
    // uninitialized_move
    // uninitialized_fill
    // uninitialized_copy_n
    // uninitialized_move_n
    // uninitialized_fill_n
    // destroy destroy_n destroy_at
    // construct_at
    // uninitialized_default_construct
    // uninitialized_value_construct
    // uninitialized_default_construct_n
    // uninitialized_value_construct_n
    
    return 1;
}

template<typename T>
using ilist = std::initializer_list<T>;

void non_modifiying_operations() {
    ////////////////////////////////////////////////////////////////////////////
    // Existence queries
    ////////////////////////////////////////////////////////////////////////////
    constexpr auto isEven = [](const int i){return i%2==0;};
    constexpr auto isOdd  = [](const int i){return i%2==1;};

    {
    constexpr static auto range = {-2, 0, 4, 4, 4, 100};
    static_assert(all_of  (range, isEven));
    static_assert(any_of  (range, isEven));
    static_assert(none_of (range, isOdd));
    static_assert(count   (range, 4)      == 3);
    static_assert(count_if(range, isEven) == 6);
    static_assert(contains(range, 100));
    static_assert(contains_subrange(range, initializer_list{4,4}));
    static_assert(starts_with(range, initializer_list{-2,0}));
    static_assert(ends_with(range, initializer_list{4,100}));
    }

    ////////////////////////////////////////////////////////////////////////////
    // Finding/Locating Elements
    ////////////////////////////////////////////////////////////////////////////
    {
    constexpr static auto range    = {-2,0,4,4,4,6,4,6,10};
    constexpr        auto end      = range.end();

    // Finding single elements
    static_assert(*find(         range, 4)        == 4);
    static_assert( find(         range, 3)        == end);
    static_assert(*find_if(      range, isEven)   == -2);
    static_assert( find_if(      range, isOdd)    == end);
    static_assert(*find_if_not(  range, isOdd)    == -2);
    static_assert( find_if_not(  range, isEven)   == end);
    static_assert(*find_first_of(range, initializer_list{3,4,5,6}) == 4);
    static_assert( find_first_of(range, initializer_list{3,5}) == end);
    // NB: find_last returns subrange view from match to end
    static_assert(*find_last(       range, 4     ).begin() == 4);
    static_assert( find_last(       range, 4     ).end()   == end);
    static_assert( find_last(       range, 3     ).begin() == end);
    static_assert(*find_last_if(    range, isEven).begin() == 10);
    static_assert( find_last_if(    range, isOdd ).begin() == end);
    static_assert(*find_last_if_not(range, isOdd ).begin() == 10);
    static_assert( find_last_if_not(range, isEven).begin() == end);

    // Finding consecutive runs of elements
    static_assert(*adjacent_find(range) == 4);
    static_assert(*search_n(range, 2, 4).end() == 4);
    static_assert(*search_n(range, 3, 4).end() == 6);
    static_assert( search_n(range, 4, 4).begin() == end);

    // Find subranges
    static_assert(*search(range, initializer_list{4,6}).begin() == 4);
    static_assert(*find_end(range, initializer_list{4,6}).begin() == 4);
    }

    ////////////////////////////////////////////////////////////////////////////
    // Comparing ranges
    ////////////////////////////////////////////////////////////////////////////
    {
    constexpr static auto range1 = {1,2,3};
    constexpr static auto range2 = {1,2,1,4};
    
    static_assert(equal(range1, range1));

    constexpr auto result = mismatch(range1, range2);
    static_assert(*result.in1 == 3 && *result.in2 == 1);

    static_assert(lexicographical_compare(range2, range1));
    }

    ////////////////////////////////////////////////////////////////////////////
    // Binary Search of Sorted Ranges
    ////////////////////////////////////////////////////////////////////////////    ////////////////////////////////////////////////////////////////////////////
    {
    constexpr static auto range = {0,2,4,6,8,8,8,10};

    static_assert(
       binary_search(range, 4)
    && *lower_bound(range, 5) == 6
    && *upper_bound(range, 5) == 6
    && *lower_bound(range, 4) == 4
    && *upper_bound(range, 4) == 6
    );
    
    constexpr auto result     = equal_range(range, 8);
    constexpr int  idx        = distance(range.begin(), result.begin());
    constexpr int  range_size = distance(result.begin(), result.end());
    static_assert(
           *result.begin() == 8 
        && *result.end() == 10
        && idx == 4 
        && range_size == 3
    );

    static_assert(
            includes(range, initializer_list{2,6,8}) 
        && !includes(range, initializer_list{2,5,6})
    );
    }
    ////////////////////////////////////////////////////////////////////////////
    // Minimum / Maximum
    ////////////////////////////////////////////////////////////////////////////
    {
    constexpr static auto range = {0,2,4,6,8,8,8,10};
    static_assert(*min_element(range) == 0);
    static_assert(*max_element(range) == 10);
    constexpr auto result = minmax_element(range);
    static_assert(*result.min == 0 && *result.max == 10);

    static_assert(
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
    vector container {1,2,4,3};
    auto cb = container.cbegin();
    auto ce = container.cend();
    vector t {3,4,1,2};
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

// Transformation operations
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
    // printf("Move\n");
    // printf("Before: %s -> %s\n", to_string(container).c_str(), to_string(t).c_str());
    move(cb, ce, t.begin());
    // printf("After : %s -> %s\n", to_string(container).c_str(), to_string(t).c_str());
    // move_backward(cb, ce, );
    }


    ////////////////////////////////////////////////////////////////////////////
    // Sampling
    ////////////////////////////////////////////////////////////////////////////
    // sample(cb, ce, );

    ////////////////////////////////////////////////////////////////////////////
    // Swapping
    ////////////////////////////////////////////////////////////////////////////
    // swap
    // iter_swap(cb, ce, );
    // swap_ranges(cb, ce, );
};
void reordering_elements() {
    // ++ Sorting and related operations
    // Partitioning operations
    // partition partition_copy 
    // stable_partition
    // is_partitioned
    // partition_point
    // // Sorting operations
    // sort stable_sort
    // partial_sort partial_sort_copy
    // is_sorted is_sorted_until
    // nth_element
    // // Binary search operations (on partitioned ranges)
    // lower_bound upper_bound
    // equal_range
    // binary_search
    // // Set operations (on sorted ranges)
    // includes
    // set_union
    // set_intersection
    // set_difference
    // set_symmetric_difference
    // // Merge operations (on sorted ranges)
    // merge inplace_merge
    // // Heap operations
    // push_heap pop_heap make_heap sort_heap is_heap is_heap_until
    // // Minimum/maximum operations
    // max min minmax
    // max_element min_element minmax_element
    // clamp

    // // Lexicographical comparison operations
    // lexicographical_compare
    // lexicographical_compare_three_way
    // // Permutation operations
    // next_permutation
    // prev_permutation
    // is_permutation

};
void modifiying_elements() {
    // replace replace_if
    // transform
    // replace_copy replace_copy_if
    
    // // Generation operations
    // fill fill_n
    // generate generate_n
    // // Removing operations
    // remove remove_if
    // unique
    // remove_copy remove_copy_if
    // unique_copy
    // // Order-changing operations
    // reverse reverse_copy
    // rotate rotate_copy
    // random_shuffle shuffle
    // shift_left shift_right

};
void numeric_operations() {
    // // Numeric operations
    // iota
    // inner_product
    // adjacent_difference
    // accumulate
    // reduce
    // transform_reduce

    // partial_sum
    // inclusive_scan
    // exclusive_scan
    // transform_inclusive_scan
    // transform_exclusive_scan
};
void range_and_iterator_utilties() {

};
////////////////////////////////////////////////////////////////////////////
// Unsorted
////////////////////////////////////////////////////////////////////////////

// auto print = [](const int i){printf("%d, ", i);};
// for_each(c.cbegin(), c.cend(), print);
// printf("\n");
// for_each_n(c.cbegin(), 2, print);
// printf("\n");

// vector<int> vec {1,3,2,4,3,5,4,6};
// sort(vec.begin()+3, vec.end());
// for (int i : vec) { printf("%d, ", i);}
