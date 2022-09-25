// Project
#include "basics.h"
using std::numeric_limits;
using std::cout;
using std::setw;

// STL
#include <sstream>
using std::stringstream;

// C Libs
#include <cmath> // INFINITY, NAN
using std::isnan;
#include <cstddef> // size_t


int main() {
    ////////////////////////////////////////////////////////////////////////////
    // Types
    ////////////////////////////////////////////////////////////////////////////
    cout << "Main types\n";
    type_summary<bool>("bool");
    type_summary<char>("char");
    type_summary<short>("short");
    type_summary<int>("int");
    //type_summary<signed>("signed");
    type_summary<unsigned>("unsigned");
    type_summary<long>("long");
    type_summary<long long>("long long");
    type_summary<size_t>("size_t");
    type_summary<float>("float");
    type_summary<double>("double");
    type_summary<long double>("long double");
    cout << '\n'; 

    // Style and efficiency preferences
    // Integers: Use int unless you have memory constraints
    // Signed vs Unsigned: Avoid unsigned unless you cannot
    // Floats: Default to double unless memory footprint is an issue

    ////////////////////////////////////////////////////////////////////////////
    // Literals
    ////////////////////////////////////////////////////////////////////////////
    
    // void
    void *p = nullptr;
    assert(p == 0);

    ////////////////////////////////////////
    // bool
    bool is_true  = true;
    bool is_false = false;
    assert(is_true and not is_false);

    ////////////////////////////////////////
    // integers
    int n_dec = 4847;
    int n_bin = 0b1001011101111;
    int n_oct = 011357;
    int n_hex = 0x12ef;
    assert(n_bin==n_oct and n_oct==n_dec and n_dec==n_hex);

    // Multiple ways to initialize types and order doesn't matter
    // short == short int == signed int == signed short int == short signed int
    
    // Literal seperators
    assert(1'000'000'000'000 == 1000000000000);

    // Integer suffixes: u, l, ll (use case?)
    stringstream ss1, ss2;
    ss1 << -1ull;
    ss2 << numeric_limits<unsigned long long>::max();
    assert(ss1.str() == ss2.str());    

    ////////////////////////////////////////
    // character
    char c = 'A';
    char c1 = '\x41';
    assert(c == c1);
    
    // Strings as character arrays
    char str1[] = "Hello, world!";
    const char* str2 = "Hello, world!";

    assert(str1[1] == 'e');
    assert(str2[1] == 'e');

    // Unicode
    // char16_t c16 =;
    // char32_t c32 =;

    // functional uint8 for when memory really matters
    // unsigned char

    ////////////////////////////////////////
    // floats
    double dbl1 = 123.456;
    double dbl2 = 1.23456e2;
    assert(dbl1==dbl2);
    float flt1 = 123.456f;
    float flt2 = 1.23456e2f;
    assert(flt1==flt2);
    long double ldbl1 = 123.456l;
    long double ldbl2 = 1.23456e2l;
    assert(ldbl1==ldbl2);

    // Special 
    double inf = INFINITY;
    assert(1.0/ 0.0 ==  inf and 1.0/ inf ==  0.0);
    assert(1.0/-0.0 == -inf and 1.0/-inf == -0.0);

    double nan = NAN;
    assert(isnan(nan));
    assert(isnan(0.0/0.0));

    // Value categories
    // Copy vs Move
    // https://en.cppreference.com/w/cpp/language/value_category
          int   lval           = 5; // literals are rvalues
          int&  lval_ref       = lval;
    const int&  const_lval_ref = 5;
          int&& rval_ref       = 5;
    
    (void)lval_ref;
    (void)const_lval_ref;
    (void)rval_ref;

    ////////////////////////////////////////////////////////////////////////////
    // Operators
    
    ////////////////////////////////////////////////////////////////////////////
    // Pointers
    
    ////////////////////////////////////////
    return 0;
}
