#include "03_simple_project_structure/adder.h"

// C/C++ std library
#include <iostream>
using std::cout;
using std::endl;

int main(int argc, char* argv[]) {
    int x = 1;
    int y = 2;
    cout << "INFO :: " << x << " + " << y << " = " << add(x,y) << endl;
}
