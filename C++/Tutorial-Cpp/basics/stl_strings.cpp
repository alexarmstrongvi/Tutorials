// C++ stdlib
#include <iostream>
using std::cout;
#include <string>
using std::string;
#include <string_view> // C++17
using std::string_view;
#include <sstream>
using std::stringstream;

// C libraries
#include <cmath> // INFINITY, abs
using std::log2;
#include <cstdio> // printf

int main() {
    ////////////////////////////////////////////////////////////////////////////
    // Literals
    {
    using namespace std::literals; // operator""s and operator""sv
    string      str1 = "ab\0cd";   // C-style string
    string      str2 = "ab\0cd"s;  // string
    string_view str3 = "ab\0cd"sv; // string_view

    assert(str1 == "ab");
    assert(str2 == str3);
    assert(str2.size() == 5);
    }

    ////////////////////////////////////////////////////////////////////////////
    // Initialization
    {
    string str1;                // default
    string str2 {"123456789"};  // move or c-string copy
    string str3 {str2};         // copy
    string str4(str2, 3,6);     // substring copy
    string str5("12345", 3);    // buffer copy
    string str6a(5,'A');        // fill w/ char
    string str6b(5,0x41);       // fill w/ int
    string str7 {'1','2','3'};  // initializer list
    string str8(str2.begin(), str2.end()); // range/iterator

    assert(str1  == "");
    assert(str2  == str3);
    assert(str4  == "456789");
    assert(str5  == "123");
    assert(str6a == "AAAAA");
    assert(str6a == str6b);
    assert(str7  == "123");
    assert(str8  == str2);
    }

    ////////////////////////////////////////////////////////////////////////////
    // Attributes
    {
    string str {"123456789"};
    assert(str.size() == str.length() && str.size() == 9);
    assert(!str.empty());
    assert(str.capacity() >= str.size());
    assert(str.max_size() <= string::npos);
    assert(log2(str.max_size()) == 64);
    }

    // Demo: Memory allocation
    {
    string str;
    size_t cap = 0;
    cout << "Capacity increments: ";
    for (int i = 0; i < 7; i++) {
        // Capacity tends to double to accomodate increased size
        int increase = str.capacity() - cap;
        double p_increase = cap > 0 ? (str.capacity()-1)/double(cap) : INFINITY;
        cap = str.capacity();
        cout << cap << " [+" << increase << ";x" << p_increase << "], ";
        str.append(increase + 1, 'A');
    }
    cout << '\n';
    }

    ////////////////////////////////////////////////////////////////////////////
    // Access
    {
    string str = "123456789";
    assert(str[3] == str.at(3) && str[3] == '4');
    assert(str.front() == str.at(0));
    assert(str.back()  == str.at(str.size()-1));
    assert(str.c_str() == &str[0] && str.c_str() == str.data());
    // str.get_allocator()
    }

    // Iterating
    {
    string str = "0123456789";
    // Iterating (3 ways)
    for (size_t i = 0; i < str.size(); i++) {
        char c = str.at(i);
        assert(c == std::to_string(i)[0]);
    }
    for (char c : str) {
        assert('0' <= c and c <= '9');
    }
    for (string::iterator it = str.begin()+1; it != str.end()-1; ++it) {
        char c = *it;
        assert('0' < c and c < '9');
    }
    }

    // Extracting substrings
    {
    const string str {"123456789"};

    assert(str.substr(2,3) == "345");

    // copy()
    size_t len {5}, pos {3};
    char buffer[10];
    size_t length = str.copy(buffer, len, pos); // Note the switched pos and len args
    buffer[length] = '\0';
    assert(length == len);
    assert(strcmp(buffer, str.substr(pos, len).c_str()) == 0);
    }

    // Comparisons
    {
    string compared_str {"123"};
    assert(compared_str.compare(compared_str) == 0);
    // >0 if compared string would be sorted before
    assert(compared_str.compare("12") > 0);
    assert(compared_str.compare("11") > 0);
    // <0 if compared string would be sorted after
    assert(compared_str.compare("13") < 0);
    assert(compared_str.compare("1234") < 0);
    }

    // String searching
    {
    string str {"012345678901234567890"};
    assert(str.find('3') == 3);
    assert(str.find("34") == 3);
    assert(str.find('3', 10) == 13);
    assert(str.find('X') == string::npos);
    assert(str.find("3400", 4, 2) == 13);

    assert(str.rfind('3') == 13);

    assert(str.find_first_of("AB3C") == 3);
    assert(str.find_last_of("AB3C") == 13);
    assert(str.find_first_not_of("012") == 3);
    assert(str.find_last_not_of("4567890")  == 13);
    }

    ////////////////////////////////////////////////////////////////////////////
    // Operations
    {
        string str1 {"Hello"}, str2 {" "}, str3 {"World"};
        assert(str1 + str2 + str3 == "Hello World");

        string str;
        str += str1 + str2 + str3;
        assert(str == "Hello World");

        using namespace std::literals;
        assert("Hello"s + " "s + "World"s == "Hello World");
    }

    ////////////////////////////////////////////////////////////////////////////
    // Modify
    // Many of these functions have similar overloading as the contstructors
    // (e.g. the arguments can be strings, c-strings, ranges, repeated chars,
    // initializer lists, etc.)
    // Overwrite
    {
    string str1, str2;
    str1 = "123456";        // assignment operator
    str2.assign(str1, 2,3); // assignment method
    assert(str2 == "345");
    }

    // Update and Swap
    {
    string str;
    str.push_back('1');    // append char
    str.append("267");     // append string
    str.insert(2, "3XX");  // insert string anywhere
    str.replace(3,2,"45"); // replace string with string
    assert(str == "1234567");

    string str_swap {"ABC"};
    str_swap.swap(str);
    assert(str_swap == "1234567" && str == "ABC");
    swap(str, str_swap);
    assert(str == "1234567" && str_swap == "ABC");
    }

    // Resize
    {
    string str {"12345"};
    str.resize(3);
    assert(str == "123");
    str.resize(5, 'X');
    assert(str == "123XX");
    }

    // Memory
    {
    string str {"12345"};
    assert(str.capacity() < 1000);
    str.reserve(1000);
    assert(str.capacity() >= 1000);
    str.shrink_to_fit();
    assert(str.capacity() >= str.size());
    }

    // Removing
    // str.pop_back();
    // str.erase();
    // str.clear()

    // Type conversions
    {
    int i                  = std::stoi("123");
    long l                 = std::stol("123");
    long long ll           = std::stoll("123");
    unsigned int ul        = std::stoul("123");
    unsigned long long ull = std::stoull("123");
    float f                = std::stof("1.23");
    double d               = std::stod("1.23");
    long double ld         = std::stold("1.23");

    assert(i == l && l == ll && ll == ul && ul == ull);
    assert(abs(f - d) < 0.001); // Not exact
    assert(abs(d - ld) < 0.001);

    string s = std::to_string(1.23);
    assert(s == "1.230000");
    }

    ////////////////////////////////////////////////////////////////////////////
    // C string formatting (printf)
    double pi = 3.14159265359;
    long double pi_l = 3.14159265359l;
    // Format specifier prototype
    // %[flags][width][.precision][length]specifier
    printf ("Format specifier types\n");
    printf ("\t     Specifier :| %f |\n",      pi);   // 3.141593
    printf ("\t add Length    :| %Lf |\n",     pi_l); // 3.141593
    printf ("\t add Precision :| %.3Lf |\n",   pi_l); // 3.142
    printf ("\t add Width     :| %8.3Lf |\n",  pi_l); //    3.142
    printf ("\t add Flags     :| %08.3Lf |\n", pi_l); // 0003.142

    // Specifiers
    printf ("Specifiers\n");
    printf ("\t Characters : %c %c \n", 'a', 65);
    printf ("\t Decimals   : %d %ld\n", 1977, 650000L);
    printf ("\t Radices    : %d %x %o %#x %#o \n", 100, 100, 100, 100, 100);
    printf ("\t Floats     : %f %e %E \n", 3.1416, 3.1416, 3.1416);
    printf ("\t %s \n", "String");

    // Length

    // Precision

    // Width

    // Flags

    ////////////////////////////////////////////////////////////////////////////
    // IO manipulation
    // resetiosflags()
    // setiosflags()
    // setbase()
    // setfill()
    // setprecision()
    // setw()
    // get_money()
    // put_money()
    // get_time()
    // put_time()
    // quoted()

    ////////////////////////////////////////////////////////////////////////////
    // String views (C++17)
    {
    string str {"12345"};
    string str_copy(str);
    string_view str_view(str);
    assert(&str[0] != &str_copy[0]);
    assert(&str[0] == &str_view[0]);

    constexpr string_view strv {"12345"};
    static_assert(strv == "12345");
    }

    ////////////////////////////////////////////////////////////////////////////
    // C-string functions
    // Copying:
    // memcpy()
    // memmove()
    // strcpy()
    // strncpy()

    // Concatenation:
    // strcat()
    // strncat()

    // Comparison:
    // memcmp()
    // strcmp()
    // strcoll()
    // strncmp()
    // strxfrm()

    // Searching:
    // memchr()
    // strchr()
    // strcspn()
    // strpbrk()
    // strrchr()
    // strspn()
    // strstr()
    // strtok()

    // Other:
    // memset()
    // strerror()
    // strlen()

    ////////////////////////////////////////////////////////////////////////////
    // Other
    // UTF-8, UTF-16, UTF-32

    // Stream interactions
    // cin >> str
    // cout << str
    // getline(cin, str)

    return 0;
}
