#include<iostream>
using std::cout;
#include<string>
using std::string;

////////////////////////////////////////////////////////////////////////////////
// Notes
// - Function vs Class template
// - Function template vs template function
// - SFINAE, template metaprogramming, and compile time intropspection
// - decltype, decval
// - typedef
//
// Resources
// - https://jguegant.github.io/blogs/tech/sfinae-introduction.html
////////////////////////////////////////////////////////////////////////////////

template<typename T>
T add(T x, T y) { return x + y; }


int main() {
    cout << add<double>(1,2) << '\n';
    cout << add(1,2) << '\n';
    cout << add(1.1, 2.2) << '\n';
    cout << add<string>("A", "B") << '\n';
    return 0;
}
