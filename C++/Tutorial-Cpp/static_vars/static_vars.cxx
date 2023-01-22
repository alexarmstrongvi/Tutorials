#include <iostream>
using std::cout;
using std::endl;

void use_static_vars() {
    static int X;
    X=2;
    cout << "static int X = " << X << endl;
    X++;
}

int main() {
    cout << "Hello World" << endl;
    static int X = 5;
    use_static_vars();
    use_static_vars();
    use_static_vars();
    use_static_vars();
    use_static_vars();
    use_static_vars();
    use_static_vars();
    return 0;
}
