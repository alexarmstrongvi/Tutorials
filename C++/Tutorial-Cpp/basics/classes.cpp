#include <cassert> // assert
/*
- acess specifiers: private, public, protected
- members
*/
class Point {
  // private by default
    int x_;
    int y_;

  public:
    // Constructors
    Point() {}
    Point(int x, int y) : x_(x), y_(y) {}
    // Point(int x, int y) : x_(x) {y_ = y;}
    // Point(int x, int y) {x_ = x; y_ = y;}
    
    // copy construtor
    Point(const Point& p) : x_(p.x_) {}

    // Non-modifying function members
    int x() const {return x_;}
    int y() const {return y_;}
    int y_plus_1() const {return y_+1;}

    // Modifying function members
    void set_x(int x) {x_ = x;}
};

int main() {
    Point p(1, 2);
    p.x() == 1;
    p.y_plus_1() == 2;
    assert(p.x() == 1 && p.y() == 2);
}