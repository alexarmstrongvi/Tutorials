
////////////////////////////////////////////////////////////////////////////////
// Containers
// - Sequences
//      - vector
//      - deque
//      - array
//      - list
//      - forward_list
//      - basic_string
// - Associated Containers
//      - Maps: map, multimap (and unordered_* variants)
//      - Sets: set, multiset (and unordered_* variants)
// - Container Adapters
//      - stack
//      - queue
//      - priority_queue
// - Other classes
//      - Allocator - responsible for memory allocation and management
//      - Compare - 
//      - initializer_list<T>
////////////////////////////////////////////////////////////////////////////////

// Project
#include "containers.h"

// STL
#include <iostream>
using std::cout;
#include <iomanip>
using std::setw;
#include <utility>
using std::move;
#include <iterator>
using std::next;

#include <array>
using std::array;
#include <vector>
using std::vector;
#include <deque>
using std::deque;
#include <list>
using std::list;
#include <forward_list>
using std::forward_list;
#include <utility>
using std::pair;
using std::make_pair;
#include <tuple>
using std::tuple;
using std::get;
#include <map>
using std::map;
using std::multimap;
#include <unordered_map>
using std::unordered_map;
using std::unordered_multimap;
#include <set>
using std::set;
using std::multiset;
#include <unordered_set>
using std::unordered_set;
using std::unordered_multiset;
#include <queue>
using std::queue;
using std::priority_queue;
#include <stack>
using std::stack;

#include <cmath>
using std::pow;
using std::log2;

////////////////////////////////////////////////////////////////////////////////
int main() { 
    const int n = 5;
    ////////////////////////////////////////////////////////////////////////////
    // C-array
    cout << "===== C arrays =====\n"; 
    // Empty initialization (no guarantee of initialized values)
    int arr1[n]; // {?, ?, ?, ?, ?}
    // Partial initialization
    int arr2[n] = {1}; // {1, ?, ?, ?, ?}
    int arr3[n] = {1,3,5}; // {1, 3, 5, ?, ?}
    assert(arr2[n-1] == 0 and arr3[n-1] == 0); // Is this always true?
    // Full initialization
    int arr4[n] = {1,3,5,7,9};
    int arr5[] = {1,3,5,7,9};
    int arr6[] {1,3,5,7,9};
    assert_arrays_equal(arr4, arr5, n);
    assert_arrays_equal(arr4, arr6, n);
    // Multi-dimensional
    int arr7[3][3] = {{1,2,3}, {4,5,6}, {7,8,9}};

    cout << "int arr[" << n << "]: \n";
    for (int i=0; i<n; i++) {
        cout << "\t[" << i << "] " << &arr1[i] << " -> " << arr1[i] << '\n';
    }

    // Properties
    assert(sizeof(arr6)/sizeof(arr6[0]) == n);
    assert(arr6 == &arr6[0]);
    // Access
    assert(arr6[0] == 1 and arr6[n-1] == 9);
    assert(arr7[1][1] == 5); 
    for (int i=0; i<n; i++) {
        assert(arr6[i] == *(arr6 + i));
        assert(arr6[i] == *(i + arr6));
        assert(arr6[i] == i[arr6]); // Wierd
    }

    // Assignment
    arr6[0] = 99;
    assert(arr6[0] == 99);
    
    ////////////////////////////////////////
    // Character C-arrays (a.k.a. C strings)
    // Lots of functions are overloaded to behave differently when passed 
    // char arrays compared to other arrays as it assumes a char array is
    // a string
    char char_arr0[n];
    int char_to_int_arr[n];
    for (int i=0; i<n; i++) { char_to_int_arr[i] = static_cast<int>(char_arr0[i]); }
    cout << "Uninitialized char arr[] -> " << to_string(char_to_int_arr, n) << '\n';
    char char_arr1[n] = {'a', 'b', 'c', 'd', 'e'};
    for (int i=0; i<n; i++) { char_to_int_arr[i] = static_cast<int>(char_arr1[i]); }
    cout << "'cout << char_arr' prints string: " << char_arr1 << '\n';
    cout << "'cout << int_arr' prints address: " << char_to_int_arr << '\n';
    char char_arr2[] = "ab";
    char char_arr3[] = {'a','b','\0'};
    assert_arrays_equal(char_arr2, char_arr3, 3);

    ////////////////////////////////////////////////////////////////////////////
    // C++ array
    ////////////////////////////////////////////////////////////////////////////
    cout << "\n\n===== C++ arrays =====\n";
    // Initialization
    array<int, n> cpp_arr {0, 2, 4, 6, 8};
    // Properties
    assert(not cpp_arr.empty());
    assert(cpp_arr.size()     == n);
    assert(cpp_arr.max_size() == cpp_arr.size());
    // Access
    assert(cpp_arr[1]         == 2);
    assert(cpp_arr.at(1)      == cpp_arr[1]);
    assert(cpp_arr.front()    == cpp_arr[0]);
    assert(cpp_arr.back()     == cpp_arr[n-1]);
    // Iterators
    assert(cpp_arr.begin()    == &cpp_arr.front()); 
    assert(cpp_arr.end()      == &cpp_arr.back() + 1); 
    assert(*cpp_arr.rbegin()  == cpp_arr.back()); 
    assert(&*cpp_arr.rend()   == &cpp_arr.front() - 1); 
    // Constant iterators (same as above but cannot modify elements)
    // cpp_arr.cbegin() cend() crbegin() crend()

    // Iterating (3 ways)
    for (size_t i = 0; i < cpp_arr.size(); i++) {
        int val = cpp_arr.at(i);
        assert(val == static_cast<int>(2*i));
    }
    for (int val : cpp_arr) {
        assert(0 <= val and val <= 8 and val%2==0);
    }
    for (array<int, n>::iterator it = cpp_arr.begin(); it != cpp_arr.end(); it++) {
        int val = *it;
        assert(0 <= val and val <= 8 and val%2==0);
    }

    // Operations
    array<int, n> cpp_arr2 {0, 0, 0, 0, 0};
    assert(cpp_arr2[0] == 0 and cpp_arr2[4] == 0);
    cpp_arr2.fill(9);
    assert(cpp_arr2[0] == 9 and cpp_arr2[4] == 9);

    array<int, n> cpp_arr3 {0, 0, 0, 0, 0};
    cpp_arr3.swap(cpp_arr2);
    assert(cpp_arr3[0] == 9 and cpp_arr3[4] == 9);
    assert(cpp_arr2[0] == 0 and cpp_arr2[4] == 0);

    // Operators(==; until C++17 !=,<,<=,>,>=; C++20 <=>)
    array<int, n> cpp_arr4 = cpp_arr; // copy
    assert(cpp_arr == cpp_arr4);
    assert(cpp_arr <= cpp_arr4);
    assert(cpp_arr >= cpp_arr4);

    ////////////////////////////////////////////////////////////////////////////
    // vector
    ////////////////////////////////////////////////////////////////////////////
    cout << "\n\n===== Vectors =====\n";
    // Initialization (same as std::array)
    {
    // Same options as std::array as well as others
    vector<int> vec1(5);
    assert(vec1.size() == 5 and vec1.front() == int());
    
    vector<int> vec2(5, 9);
    assert(vec2.size() == 5 and vec2.front() == 9);
    
    vector<int> vec3(vec2.begin()+1, vec2.end()-1);
    assert(vec3.size() == 3 and vec3.front() == 9);

    vector<int> vec4(vec3); // copy constructor
    assert(vec4 == vec3);
    
    vector<int> vec5({1,2,3}); // move constructor
    assert(vec5.size() == 3 and vec5.front() == 1 and vec5.back() == 3);
    }
    
    
    vector<int> vec {1,3,5,7,9};
    //////////////////////////////////////// 
    // Properties
    // same as array: empty, size
    assert(vec.size() == 5);
    assert(vec.size() <= vec.capacity());
    assert(vec.capacity() < vec.max_size());
    assert(vec.max_size() < pow(2,64));

    //////////////////////////////////////// 
    // Access - same as C++ arrays
    
    //////////////////////////////////////// 
    // Modification

    // Capacity
    vec.reserve(10);
    assert(vec.capacity() == 10 and vec.size() == 5);
    
    vec.shrink_to_fit();
    assert(vec.capacity() == vec.size());
    
    vec.resize(11); // Fills extra space with zeros
    assert(vec.size() == 11 and vec.back() == 0 and vec.capacity() == 11);
    vec.resize(5); // Removes elements to fit within new size
    assert(vec.size() == 5 and vec.capacity() == 11);
    
    // Removing elements
    vec.pop_back(); // Remove last element
    assert(vec.size() == 4 and vec.back() == 7 and vec.capacity() == 11);

    vec.erase(vec.begin()+1); // Remove element at or between iterators
    assert(vec.size() == 3 and vec.at(1) == 5);
    vec.erase(vec.begin()+1, vec.end());
    assert(vec.size() == 1 and vec.at(0) == 1);

    vec.clear(); // remove all elements
    assert(vec.empty());

    // Adding elements
    vec.push_back(1); // add to back
    vec.insert(vec.end(), {5,7}); // add 1+ elements at position
    vec.emplace_back(9); // provide constructor args and a new instance will be added to the back
    vec.emplace(vec.begin()+1, 3); // emplace before a specific element
    vector<int> vec_answer {1,3,5,7,9};
    assert(vec == vec_answer);
    
    // Changing elements
    vec.assign({0,2,4,6}); // Overwrite
    assert(vec.size() == 4 and vec.back() == 6);

    vector<int> vec2 {1,3,5,7,9};
    vec.swap(vec2); // Swap identifies (no move or copy)
    assert(vec2.front() == 0 and vec2.back() == 6);
    assert(vec.front()  == 1 and vec.back()  == 9);

    //////////////////////////////////////// 
    // Iterators
    // Same as std::array but be aware of memory reallocation invalidating 
    // pointers and iterators.
    
    ////////////////////////////////////////
    // Demo: Memory reallocation
    // When vectors run out of capacity to store an element, memory is 
    // allocated for a larger array and the contents of the current vector
    // are copied over to the new location
    //cout << "Memory reallocation:\n";
    //vec.clear();
    //vec.shrink_to_fit();
    ////vec.reserve(10); // Change how capacity increases
    //vec.push_back(0);
    //const int *ptr = &vec[0];
    //size_t prev_capacity = 0;
    //for (int i=1; i<100; i++) {
    //    if (vec.capacity() != prev_capacity) {
    //        prev_capacity = vec.capacity();
    //        cout << "\tReallocation: size = " << setw(2) << vec.size() << "; " 
    //             << "capacity = " << setw(3) << vec.capacity() << "; "
    //             << "&vec[0] = " << &vec[0] << "; "
    //             << "address shift = " << &vec[0] - ptr << "; "
    //             << '\n';
    //        }
    //    vec.push_back(i);
    //}
    //cout << '\n';

    ////////////////////////////////////////
    // Demo: The max size of a vector depends on its type
    vector<bool> vec_bool;
    vector<char> vec_char;
    vector<int> vec_int;
    vector<double> vec_double;
    vector<std::string> vec_string;
    vector<vector<double>> vec_double2;
    cout << "vec.max_size(): "
         << "bool (2^"    << log2(vec_bool.max_size())    << ") "
         << "char (2^"    << log2(vec_char.max_size())    << ") "
         << "int (2^"     << log2(vec_int.max_size())     << ") "
         << "double (2^"  << log2(vec_double.max_size())  << ") "
         << "string (2^"  << log2(vec_string.max_size())  << ") "
         << "double2 (2^" << log2(vec_double2.max_size()) << ") "
         << '\n';

    ////////////////////////////////////////
    // Demo: emplace saves move operations when adding structs
    

    ////////////////////////////////////////////////////////////////////////////
    // deque
    ////////////////////////////////////////////////////////////////////////////
    cout << "\n\n===== Deque =====\n";
    // Initialization (same as vector)
    
    // Properties (subset of vector; no capacity())
    
    // Access (same as array)
    
    // Modification
    //  - lots of overlap with vector
    //  - can't reserve()
    //  - can push_front() and emplace_front()
    
    // Iterators (same as array)
    
    // Demo: Show allocation of discontiguous blocks
    //deque<int> deq {0};
    //cout << "Memory reallocation\n";
    //int n_blocks = -1;
    //for (int i = 1; i < 1500; i++) {
    //    int n_blocks2 = n_deque_blocks(deq);
    //    if (n_blocks != n_blocks2) {
    //        n_blocks = n_blocks2;
    //        cout << "\tReallocation: size = " << setw(4) << deq.size() << "; "
    //             << "n_blocks = " << n_blocks << "; "
    //             << '\n';

    //    }
    //    deq.push_back(i);
    //    deq.push_front(i);
    //}
    //cout << "Final size :" << deq.size() << '\n';
   
    ////////////////////////////////////////////////////////////////////////////
    // forward_list
    ////////////////////////////////////////////////////////////////////////////
    // Initialize (same as vector)

    // Properties
    // - flist.empty()
    // - flist.max_size()

    // Access (only front(), no operator[] or at())
    // - flist.front()

    // Iterators
    // - flist.before_begin()
    
    // Modify
    
    ////////////////////////////////////////////////////////////////////////////
    // list
    ////////////////////////////////////////////////////////////////////////////

    ////////////////////////////////////////////////////////////////////////////
    // pair, tuple, tie, ignore
    ////////////////////////////////////////////////////////////////////////////
    cout << "\n\n===== Pairs =====\n";
    // Initialization
    {
        // Default constructor
        pair<char, int> pair1;

        // Initializer list
        pair<char, int> pair2 {'A', 1};
        pair<char, int> pair3({'A', 1});

        // make_pair
        auto pair4 = make_pair('A', 1);

        // Copy constructor
        pair<char, int> pair5(pair2);

        // Move constructor
        pair<char, int> pair6(move(pair2));

        assert(pair1.first == char() and pair1.second == int());
        assert(pair2 == pair3);
        assert(pair4 == pair2);
        assert(pair5 == pair2);
        assert(pair6 == pair2);
    }
    pair<char, int> pair1 {'A', 1};
    assert(get<0>(pair1)    == pair1.first);
    assert(get<char>(pair1) == pair1.first);
    assert(get<1>(pair1)    == pair1.second);
    assert(get<int>(pair1)  == pair1.second);


    {
        tuple<bool, char, int, double> tup1;
        tuple<bool, char, int, double> tup2 {true, 'A', 1, 1.1};
        tuple<bool, char, int, double> tup3({true, 'A', 1, 1.1});
        (void)tup1;
        (void)tup2;
        (void)tup3;
        // TODO: convert tuple to string;
    }
    ////////////////////////////////////////////////////////////////////////////
    // maps: map, unordered_map, multimap, unordered_multimap
    // Optimizations
    // - When to use ordered vs unordered
    // - When to use operator[] vs insert vs emplace
    ////////////////////////////////////////////////////////////////////////////
    cout << "\n\n===== Map =====\n";
    // Initialization
    {
        // Default constructor
        map<char, int> map1;
        
        // Initializer list
        map<char, int> map2 {{'A',1}, {'B',2}};
        map<char, int> map3({{'A',1}, {'B',2}});
        
        // Range constructor
        map<char, int> map4(map3.find('B'), map3.end());
        
        // Copy constructor
        map<char, int> map5(map2);
        
        // Move constructor
        map<char, int> map6(move(map5));
        
        assert(map1.empty());
        assert(map2 == map3);
        assert(map4.size() == 1 and map4.at('B') == 2);
        assert(map5.empty());
        assert(map6 == map2);
    }

    ////////////////////////////////////////
    map<char, int> map1 {
        {'A', 1},
        {'B', 2},
        {'C', 3},
    };
    cout << map_to_string(map1) << '\n';
    
    ////////////////////////////////////////
    // Properties
    // empty, size, max_size
    
    ////////////////////////////////////////
    // Access
    assert(map1['A'] == 1);
    assert(map1.at('A') == 1);

    assert(map1.count('A') == 1);
    assert(map1.count('X') == 0);

    { // find()
        map<char, int>::iterator it = map1.find('A');
        assert(it->first == 'A' and it->second == 1);
        pair<const char, int> p = *map1.find('A');
        assert(*it == p);
        assert(map1.find('X') == map1.end());
    }
    
    // equal_range(), lower_bound(), upper_bound()

    ////////////////////////////////////////
    // Iterate
    map<char, int>::iterator it;
    for (it = map1.begin(); it != map1.end(); it++) {
        assert(map1.at(it->first) == it->second);
    }

    // C++11
    for(const pair<const char, int>& p : map1) {
        assert(map1.at(p.first) == p.second);
    }

    // C++17
    for(const auto& [key, val] : map1) {
        assert(map1.at(key) == val);
    }
    
    ////////////////////////////////////////
    // Modify
    {
        map<char, int> map1;
        // cout << "Modify = " << map_to_string(map1) << '\n';
        // operator[] inserts default initialized value
        assert(map1['A'] == int());
        assert(map1.at('A') == 0);
        map1['A'] = 1;
        assert(map1.at('A') == 1);
        
        // ----- map::insert() ----- //
        // Insert a new element
        pair<map<char, int>::iterator, bool> rv1 = map1.insert({'B', 2});
        assert(map1.at('B') == 2);
        assert(rv1.first == map1.find('B'));
        assert(rv1.second == true);

        // Insert to an already existing key will fail
        auto rv2 = map1.insert({'A', 2});
        assert(map1.at('A') == 1);
        assert(rv2.first == map1.find('A'));
        assert(rv2.second == false);
        
        // Insert after a specific element
        auto hint = map1.find('B');
        auto it1 = map1.insert(hint, {'C', 3});
        assert(map1.at('C') == 3);
        assert(*it1 == *next(hint));

        // Insert a range of values (useful for combining maps)
        map<char, int> map2 {{'X', 8}, {'Y',9}};
        map2.insert(map1.begin(), map1.end());
        assert(map2.size() == 5);

        // Insert from initializer list. Will not overwrite
        map1.insert({{'D', 4}, {'A', 9}});
        assert(map1.at('D') == 4 and map1.at('A') == 1);
        
        // Overwrite a map element like operator[] but with some returned info
        auto rv3 = map1.insert_or_assign('E', 5);
        assert(rv3.first == map1.find('E'));
        assert(rv3.second == true);
        rv3 = map1.insert_or_assign('E', 6);
        assert(rv3.first == map1.find('E'));
        assert(rv3.second == false);

        // ----- map::emplace() ----- //
        map1.emplace('F', 6); 
        map1.emplace_hint(map1.find('B'), 'X', 9);
        map1.try_emplace('G', 7);
        
        // Nodes
        // extract() and insert()

        // Erase
        map1.erase(map1.find('X'));
        assert(map1.count('X') == 0);
        // erase_if(map1)
        map1.clear();
        
        // Transfer elements from one map to another unless key already exists
        // map1.merge(map2);
        
        // Swap contants between maps
        // map1.swap(map2)
        // swap(map1, map2)
    }
    
    cout << "\n\n===== Unordered Map =====\n";
    // For when you want to preserve insertation order 
    // or for quicker look up time with large maps
    {
        map<char, int> omap {{'C',3}, {'A',5}, {'E',1}};
        unordered_map<char, int> umap {{'C',3}, {'A',5}, {'E',1}};
        assert(omap.begin()->first == 'A' and (--omap.end())->first == 'E');
        assert(umap.begin()->first == 'E'); // no 

        omap.insert({{'B', 4}, {'D', 2}});
        umap.insert({{'B', 4}, {'D', 2}});
        assert(omap.begin()->first == 'A' and (--omap.end())->first == 'E');
        assert(umap.begin()->first == 'D');

        //cout << "  ordered: " << map_to_string(omap) << '\n';
        //cout << "unordered: " << map_to_string(umap) << '\n';

        // Demo: Bucket and hash properties
        //unordered_map<int, int> umap2;
        //cout << umap2.max_load_factor() << " max load factor; "
        //     << "2^" << log2(umap2.max_bucket_count()) << " max buckets\n";
        //size_t prev_bucket_count = 999;
        //for (int i = 0; i < 5000; i++) {
        //    if (umap2.bucket_count() != prev_bucket_count) {
        //        cout << setw(4) << umap2.size() << " elements; "
        //             << setw(4) << umap2.bucket_count() << " buckets; "
        //             << umap2.load_factor() << " avg elements/bucket; "
        //             << '\n';
        //        prev_bucket_count = umap2.bucket_count();
        //    }
        //    umap2.insert({i, 2*i});
        //}
    }

    cout << "\n\n===== Multimap =====\n";
    {
        multimap<char, int> mmap {{'A',1},{'B',1},{'B',2},{'B',3},{'C',1}};
        //cout << map_to_string(mmap) << '\n';
        auto it    = *mmap.find('B');
        auto it_lo = *mmap.lower_bound('B');
        auto it_up = *mmap.upper_bound('B');
        auto it_eq_lo = *(mmap.equal_range('B').first);
        auto it_eq_up = *(mmap.equal_range('B').second);
        assert(it_lo == it and it_lo == it_eq_lo);
        assert(it_up == it_eq_up);
    }


    ////////////////////////////////////////////////////////////////////////////
    // sets: set, unordered_set, multiset, unordered_multiset
    ////////////////////////////////////////////////////////////////////////////
    cout << "\n\n===== Set =====\n";
    set<int> set1 {1,2,2,3,2};
    cout << set_to_string(set1) << '\n';
    assert(set1.size() == 3);
    
    ////////////////////////////////////////////////////////////////////////////
    // queue, priority_queue, stack
    ////////////////////////////////////////////////////////////////////////////
    
    ////////////////////////////////////////////////////////////////////////////
    return 0;
} 
