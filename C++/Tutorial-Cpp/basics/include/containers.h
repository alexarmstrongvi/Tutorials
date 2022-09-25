#pragma once
// STL
#include <sstream>
#include <string>
#include <deque>
#include <iterator> // next

// C libs
#include <cassert> // assert

template <class T>
void assert_arrays_equal(const T* arr1, const T* arr2, unsigned int n) {
    for (unsigned int ii = 0; ii < n; ii++) {
        assert(arr1[ii] == arr2[ii]);
    }
}

template <class T>
std::string to_string(const T* arr, unsigned int n, char sep = ',') {
    std::stringstream ss;
    ss << '{';
    for (unsigned int ii = 0; ii < n; ii++) {
        ss << arr[ii];
        if (ii+1 < n) {
            ss << sep << ' ';
        }
    }
    ss << '}';
    return ss.str();
}

template <class T>
std::string to_string(const T &sequence) {
    std::stringstream ss;
    ss << '{';
    for (unsigned int ii = 0; ii < sequence.size(); ii++) {
        ss << sequence[ii];
        if (ii+1 < sequence.size()) {
            ss << ", ";
        }
    }
    ss << '}';
    return ss.str();
}

template <class T>
std::string map_to_string(const T &associative) {
    std::stringstream ss;
    ss << '{';
    for (auto it = associative.begin(); it != associative.end(); it++) {
        ss << '{' << it->first << ',' << it->second << '}';
        if (std::next(it) != associative.end()) {
            ss << ", ";
        }
    }
    ss << '}';
    return ss.str();
}

template <typename T>
std::string pair_to_string(const T& p) {
    std::stringstream ss;
    ss << '{' << p.first << ", " << p.second << '}';
    return ss.str();
}


template <class T>
std::string set_to_string(const T &s) {
    std::stringstream ss;
    ss << '{';
    for (auto it = s.cbegin(); it != s.cend(); it++) {
        ss << *it;
        if (std::next(it) != s.cend()) {
            ss << ", ";
        }
    }
    ss << '}';
    return ss.str();
}

template <class T>
int n_deque_blocks(const std::deque<T>& deq) {
    if (deq.empty()) { 
        return 0;
    } else if (deq.size() == 1) {
        return 1;
    }

    int n_blocks = 1;
    const int* prev_ptr = &deq.front(); 
    for (auto it = deq.begin() + 1; it < deq.end(); it++) { 
        const int& val = *it;
        const int* ptr = &val;
        if (ptr - prev_ptr != 1) {
            n_blocks += 1;
        } else if (ptr == prev_ptr) {
            return -1;
        }
        prev_ptr = ptr;
    }
    return n_blocks;
}
