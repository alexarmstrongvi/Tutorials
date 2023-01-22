#include <vector>
using std::vector;
#include <iostream>
using std::cout;
#include <string>
using std::string;
#include <array>
using std::array;
#include <set>
using std::set;
#include <iterator>
using std::next;
#include <string>
using std::string;
#include <utility>
using std::pair;
#include <map>
using std::map;
#include <unordered_map>
using std::unordered_map;

////////////////////////////////////////////////////////////////////////////////
// Notes
// - Function vs Class vs Variable templates
// - Function template vs template function
// - template parameter categories: type, non-type (e.g. value), and template 
// - Default parameters
// - Parameter packs
// - Template specialization: explicit, fill, partial
// - SFINAE, template metaprogramming, and compile time introspection
// - decltype, declval
// - Aliases: typedef [old] vs using [new]
// - class [old] vs typename [new]
// - parameter type deduction rules
// - The standard which introduced all the above features: C++20 concepts
//
// Resources
// - https://www.internalpointers.com/post/quick-primer-type-traits-modern-cpp
// - https://jguegant.github.io/blogs/tech/sfinae-introduction.html
////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////
// Motivation 1) If you find yourself writing identifical functions or classes
// just to cover different types, use templates.
////////////////////////////////////////////////////////////////////////////////
int     add(    int x,     int y) {return x + y;}
double  add( double x,  double y) {return x + y;}
template<typename Type> 
Type add(Type x, Type y) {return x + y;}

class IntRectangle {
    int x;
    int y;
  public:
    IntRectangle(int x, int y) : x(x), y(y) {}
    int area() const {return x * y;}
};

template<typename Type>
class Rectangle {
    Type x;
    Type y;
  public:
    Rectangle(Type x, Type y) : x(x), y(y) {}
    Type area() const {return x * y;}
};

void demo_basic_templates() {
    using namespace std::literals;
    assert(add(1,2) == 3);
    assert(add(1.5, 2.0) == 3.5);
    assert(add("A"s, "B"s) == "AB");
    // If the compiler will not deduce the correct type, you can declare the
    // type explicitly 
    assert(add<string>("A", "B") == "AB");
    assert(add<float>(1, 2) == 3.0);

    IntRectangle intRectangle(2,3);
    assert(intRectangle.area() == 6);

    Rectangle intRectangle2(2,3);
    assert(intRectangle2.area() == 6);
    Rectangle dblRectangle(1.5, 2.0);
    assert(dblRectangle.area() == 3.0);
}

////////////////////////////////////////////////////////////////////////////////
// Function template syntex
////////////////////////////////////////////////////////////////////////////////
// The syntax is "template < parameter-list > declaration"

// Declaration:
// - Same as for a normal function but it can make use of the template parameters
// - If the parameter is not an argument, explicit specialization is needed when
//   calling the function as the compiler has no way to deduce the type
template <typename Type> int template_param_never_used() {return 99;}
template <typename Type> int template_param_used(Type t) {return t + 1 + Type();}

// Parameter list
// - comma separated list of 1 or more parameters
// - parameter names can be anything though there are conventions (e.g. 'T')
// - 3 categories of template parameters:
//      1) type     template parameter [most common]
//      2) non-type template parameter
//      3) template template parameter

// Type template parameters
// - type parameter key : 'typename' (preferred) or 'class' (old)
// - default types
// - parameter packs (...)
template <typename>                 int nParams0(int t)          {return t;}
template <typename = void>          int nParams0_wDefault(int t) {return t;}
template <typename T>               int nParams1(T t)            {return t;}
template <class T>                  int nParams1_class(T t)      {return t;}
template <typename T1, typename T2> int nParams2(T1 t1, T2 t2)   {return t1 + t2;}
template <typename ...Ts>           int nParamsN()               {return 99;}

// Non-type template parameters
template <int n> int nonTypeIntegral() {return n + 1;}
template <int n> int constexpr nonTypeIntegral_constexpr() {return n + 1;}

// Template template parameters (TODO: Is there a good use case for function templates?)
// template < template <typename> typename TT> int templateTemplateParam() {return TT<int>();}

struct MyDummyType {};
void demo_function_template_syntax() {
    // template_param_never_used(); // error: no matching function
    assert(template_param_never_used<MyDummyType>() == 99);
    assert(template_param_used(98) == 99);
    //nParams0(99) == 99; // error
    assert(nParams0<MyDummyType>(99) == 99);
    assert(nParams0_wDefault(99) == 99);
    assert(nParams0_wDefault<MyDummyType>(99) == 99);
    assert(nParams1(99) == 99);
    assert(nParams2(98, 1) == 99);
    assert(nParamsN() == 99);
    assert(nParamsN<MyDummyType>() == 99);
    bool result = nParamsN<MyDummyType, int, double, char>() == 99;
    assert(result);

    assert(nonTypeIntegral<5>() == 6);
    const int x {5};
    assert(nonTypeIntegral<x>() == 6);
    static_assert(nonTypeIntegral_constexpr<5>() == 6);

    //cout << "TEST " << templateTemplateParam<nParamsN>() << '\n';

}

////////////////////////////////////////////////////////////////////////////////
// Class template syntex
////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////
// Template instantiation and type deduction
////////////////////////////////////////////////////////////////////////////////
// - types, cv qualifiers, pointers, references, value categories
template <typename T> void cv_test(T const& t) { cout << __PRETTY_FUNCTION__ << '\n';}



////////////////////////////////////////////////////////////////////////////////
// Motivation X) If the function needs to take a varying number of arguments,
// used template parameter packs
template <typename T1, typename T2>   T1 sum(T1 t1, T2 t2) {return t1 + t2;}
template <typename T, typename... Ts> T  sum(T t, Ts... ts) {return t + sum(ts...);}
void demo_parameter_packs() {
    assert(sum(1,2,3,4) == 10);
}

////////////////////////////////////////////////////////////////////////////////
// Motivation X) If the function need to behave differently depending on the
// type, use template metaprogramming and type traits 
template<typename T> string type_string(T t) {

    if constexpr(std::is_integral_v<T>) {
        return "integral : " + std::to_string(t);
    } else if constexpr(std::is_floating_point_v<T>) {
        return "floating point : " + std::to_string(t);
    }
    return "Unknown";
}
void demo_type_traits() {
    assert(type_string(1)        == "integral : 1");
    assert(type_string(1.1)      == "floating point : 1.100000");
    //assert(type_string<int>(1.1) == "integral : 1"); // warning: implicit conversion
}


////////////////////////////////////////////////////////////////////////////////
// Class templates
////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////
// Demo python-like print template functions
// template<typename T>
// void print(const T container) {
//     std::cout << "{";
//     for (auto it = container.cbegin(); it != container.cend(); ++it) {
//         std::cout << *it;
//         if (std::next(it) != container.cend()) {
//             std::cout << ", ";
//         } else {
//             std::cout << "}\n";
//         }
//     }
// }

// //template<template <typename...> typename Map, typename K, typename V>
// //void print(const Map<K, V> m) {
// template<typename T>
// void print(const T associative_arr) {
//     std::cout << "{";
//     for (auto it = associative_arr.cbegin(); it != associative_arr.cend(); ++it) {
//         std::cout << "{" << it->first << ", " << it->second << "}";
//         if (std::next(it) != m.cend()) {
//             std::cout << ", ";
//         } else {
//             std::cout << "}\n";
//         }
//     }
// }

template<typename T1, typename T2>
void print(const std::pair<T1, T2> p) {
    std::cout << "{" << p.first << ", " << p.second << "}\n";
}

void demo_print() {
    vector<int> vec_int {1,2,3,4,5};
    vector<double> vec_dbl {1.1,2.2,3.3,4.4,5.5};
    array<int, 5> arr_int {1,2,3,4,5};
    set<int> set_int {1,2,3,4,5,4,3,2,1};
    pair<string, int> pair_str_int {"A", 1};
    map<string, int> map_str_int {{"A", 1}, {"B", 2}, {"C", 3}};
    unordered_map<string, int> umap_str_int {{"A", 1}, {"B", 2}, {"C", 3}};
    // print<vector<int>>(vec_int);
    // // print(vec_dbl);
    // // print(arr_int);
    // // print(set_int);
    // print(pair_str_int);
    // print(map_str_int);
    // print(umap_str_int);
    // // print(vec_vec_int);
}

int main() {
    demo_basic_templates();
    demo_function_template_syntax();
    demo_parameter_packs();
    demo_type_traits();
    // demo_print():

    cv_test(1.5);
    
    return 0;
}
