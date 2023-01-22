#include <iostream>

using std::cout;

template<typename T>
T twice(T t) {
    return t * 2;
}
template <bool, typename T = void>
struct enable_if
{};

template<typename T>
struct enable_if<true, T> {
    T var;
    enable_if(){cout << "Created a true version with type " << typeid(var).name() << '\n';}
};
template<>
struct enable_if<true, int> {
    int var;
    enable_if(){cout << "Created a special true version with int type? " << typeid(var).name() << '\n';}
};
template<typename T>
struct enable_if<false, T> {
    T var;
    enable_if(){cout << "Created a false version with type " << typeid(var).name() << '\n';}
};

int main() {
    cout << "RUNNING MAIN\n";
    unsigned int u = 2;
    int i = -2;
    float f = 2.1;
    double d = 2.00001;
    cout << "Twice " << u << " = " << twice(u) << '\n';
    cout << "Twice " << i << " = " << twice(i) << '\n';
    cout << "Twice " << f << " = " << twice(f) << '\n';
    cout << "Twice " << d << " = " << twice(d) << '\n';

    enable_if<true, int> test1;
    enable_if<true, double> test2;
    enable_if<false, float> test3;

    return 0;
}
