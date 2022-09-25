#pragma once
// STL
#include <iostream>
#include <limits>
#include <iomanip>

template <class T>
void type_summary(const char* name) {
    T default_val = T();
    T t_min = std::numeric_limits<T>::min();
    T t_max = std::numeric_limits<T>::max();
    int n_digit_bits = std::numeric_limits<T>::digits;
    int t_exp_max = std::numeric_limits<T>::max_exponent;
    T eps = std::numeric_limits<T>::epsilon();
    T err = std::numeric_limits<T>::round_error();
    bool sign_bit = std::numeric_limits<T>::is_signed;
   
    std::cout << std::setw(11) << name << ": ";
    std::cout << "Default " << default_val << "; ";
    if (t_exp_max == 0 ) {
        std::cout << "Bits [Sign, Digits] = [" << sign_bit << "," << std::setw(2) << n_digit_bits << "]; "; 
    } else {
        unsigned n_exp_bits = static_cast<unsigned>(log2(t_exp_max)) + 1;
        std::cout << "Bits [Sign, Digits, Exp] = [" << sign_bit << "," << n_digit_bits << "," << n_exp_bits << "]; ";
        std::cout << "eps @ 1 = " << eps << "; max err = " << err << "; ";
    }
    std::cout << "range ["  << +t_min << ", " << +t_max << "]; " ;
    std::cout << "\n";
}
