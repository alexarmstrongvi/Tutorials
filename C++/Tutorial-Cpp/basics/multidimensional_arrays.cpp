/*

Compile command:
clang++ 
-Wall -Wextra -Wpedantic -Wimplicit-int-conversion -Wno-unused-variable 
-g -O0 --std=c++26 
multidimensional_arrays.cpp 
&& ./a.out
*/

#include <array>
#include <cassert>
#include <mdspan>
#include <print>
#include <span>

constexpr int M = 2;
constexpr int N = 3;
using T = int;
constexpr size_t uz(int64_t x) {
    return static_cast<size_t>(x);
}

////////////////////////////////////////////////////////////////////////////////
void print(const T mat[][N], const int m);
void print(const T (* const mat[])[N], const int m);
void print(const T * const mat[], const int m, const std::span<const int> ns);
void print(const std::array<std::array<T, N>, M> mat);
void print(std::span<const T> arr);
void print(const std::array<std::span<T>, M> mat);
void print(std::mdspan<const T, std::extents<int, M, N>> mat);
void print(std::mdspan<const T, std::dextents<size_t, 2>> mat);

void passing_2darrays_args() {
    // Contiguous
    {
        T mat[][N] = {
            {-1, 0, 0},
            { 0, 2, 0},
        };
        static_assert(std::ssize(mat) == M);
        static_assert(std::ssize(mat[0]) == N);
        print(mat, M);
    }

    // Non-contiguous fixed-size rows (no real use case for this)
    {
        T row1[] = { 0, 2, 0};
        T row0[] = {-1, 0, 0};
        T (*mat[])[N] = {&row0, &row1};

        static_assert(std::ssize(mat) == M);
        static_assert(sizeof(*mat[0])/sizeof((*mat[0])[0]) == N);
        assert((*mat[0])[0] == -1);
        assert((*mat[1])[1] == 2);
        print(mat, M);
    }
    
    // Non-contiguous varying-size rows (a.k.a. jagged array)
    {
        T row1[] = { 0, 2, 0, 99, 99};
        T row0[] = {-1, 0, 0};
        T *mat[] = {row0, row1};
        T **pmat = mat;

        static_assert(std::ssize(mat) == M);
        // static_assert(sizeof(*mat[0])/sizeof((*mat[0])[0]) == N);
        assert(mat[1][1] == 2);
        assert(mat[1][3] == 99);
        print(mat, M, {3, 5});
        print(pmat, M, {3, 4});
    }


    // std::array
    {
        std::array<std::array<T, N>, M> mat = {{
            {-1, 0, 0},
            { 0, 2, 0}
        }};
        print(mat);

        // std::span<std::span<T>> is not a valid type so multidimensional arrays
        // can only be stored in 1D spans or array of spans
        std::span<T> flat(mat[0].begin(), N*M);
        print(flat);

        std::array<std::span<T>, M> rows;
        for (int i = 0; i < std::ssize(mat); ++i) {
            rows[i] = std::span(mat[i]);
        }
        print(rows);

    }

    {
        std::array<T, N*M> holder = {{
            -1, 0, 0,
             0, 2, 0
        }};

        std::mdspan<const T, std::extents<int, M, N>> mat {holder.data()};
        static_assert(mat.rank() == 2);
        static_assert(mat.static_extent(0) == M);
        static_assert(mat.static_extent(1) == N);
        static_assert(mat.size() == M*N);
        print(mat);

        auto mat_dyn = std::mdspan(holder.data(), M, N);
        static_assert(mat_dyn.rank() == 2);
        assert(mat_dyn.static_extent(0) == std::dynamic_extent);
        assert(mat_dyn.extent(0) == M);
        assert(mat_dyn.extent(1) == N);
        assert(mat_dyn.size() == M*N);
        print(mat_dyn);

    }

}

void c_array_and_pointer_syntax() {
    // Legend
    // c = const
    // p = pointer
    // a = array
    // d = decayed array pointer
    // u = pointer (only when pointing to array with unknown size)

    // Combinations
    // pacx = pointer to array of constant values

    // Notes
    // cc       - duplicate const allowed but is the same as one const
    // ca vs cd - arrays are not assignable/copyable and so are functionally
    //            constant always where for a decayed array pointer it is
    //            meaningful whether it is const or not.
    // d vs pa  - a decayed array pointer has different semantics then a pointer
    //            to an array
    // pa       - pointers to an array may or may not store the size of the
    //            array they point to depending on how they are declared. In
    //            `(*pax)[3]` vs `(*pax)[]`, only the former can be used with
    //            sizeof to recover 3.
    constexpr auto ptr_size = sizeof(void*);
    static_assert(sizeof(int*) == ptr_size);
    static_assert(sizeof(size_t*) == ptr_size);
 
    ////////////////////////////////////////
    // Layer 0
    int x = 8, y = 9;

    // Access
    assert( x == 8 &&  y == 9);

    // Const
    int const cx = x, cy = y;

    // Const behavior
    // cx = 1; // ❌

    ////////////////////////////////////////
    // Layer 1
    int *px   = &x,        *py   = &y;
    int  ax[] = {x, x, x},  ay[] = {y, y, y};
    int *dx   = ax;

    // Access
    assert(*px    == x && *py == y);
    assert( ax[0] == x && *ay == y);
    assert( dx[0] == x);

    // Compile-time info
    constexpr int n = std::ssize(ax); 
    static_assert(n == 3);
    static_assert(n == sizeof(ax)/sizeof(ax[0])); // older C-style
    static_assert(sizeof(dx) == ptr_size);

    // Arrays are not assignable or copyable
    //   ax = {1, 2, 3, 4}; // ❌ Compile error
    //   ax = ay            // ❌ Compile error
    // but decayed array pointers and array items are assignable
    //   dx = ay;       // ✅
    //   ax[0] = ay[0]; // ✅
    // Copying C-arrays should be done with std::copy, memcpy, or for-loop
    //   std::copy(std::begin(ay), std::end(ay), ax);
    //   memcpy(ax, ay, std::ssize(ay));
    //   for (int i; i < std::ssize(ay); ++i) ax[i] = ay[i];

    // Const
    int   const *        pcx   = &cx;
    int         * const  cpx   = px; // = pcx; ❌
    int   const * const cpcx   = pcx;
    int   const          acx[] = {x, x, x};
    int         * const  cdx   = ax; // = acx; ❌
    int   const * const cdcx   = acx;
 
    // Const behavior
    //  cpx    = py; // ❌
    // *cpx    = 1;  // ✅
    //  acx[0] = 1;  // ❌     
    //  cdx[0] = 1;  // ✅
    //  acx    = ay; // ❌
    //  cdx    = ay; // ❌
    // *pcx    = 2;  // ❌
    //  pcx    = py; // ✅

    ////////////////////////////////////////
    // Layer 2
    int **ppx      = &px;
    int (*pax)[n]  = &ax;
    int (*uax)[]   = pax; // like pax but size not part of type. sizeof(*uax) ❌
    int  *apx[]    = {px, px, px};
    int **dpx      = apx;
    int   aax[][n] = {{x, x, x}, {x, x, x}, {x, x, x}};
    int (*dax)[n]  = aax;

    // Access
    assert(**ppx       == x);
    assert((*pax)[1]   == x && **pax == (*pax)[0]);
    assert( *apx[0]    == x);
    assert( *apx[0]    == x);
    assert(  aax[1][1] == x && **aax == aax[0][0]);

    // Compile-time info
    static_assert(std::ssize(apx) == n);
    static_assert(std::ssize(aax) == n);
    static_assert(std::ssize(aax[0]) == n);
    static_assert(sizeof(*pax)/sizeof((*pax)[0]) == n); // std::size doesn't work

    // Const
    int       *       * const   cppx = ppx;
    int       * const *         pcpx = &cpx;
    int       * const * const  cpcpx = pcpx;
    int const *       *         ppcx = &pcx;
    int const *       * const  cppcx = ppcx;
    int const * const *        pcpcx = &cpcx;
    int const * const * const cpcpcx = pcpcx;

    int const aacx[][n] = {{x, x, x}, {x, x, x}, {x, x, x}}; // caax == acax == aacx

    int       (* const  cpax)[n]  = pax;
    int const (*        pacx)[n] = &acx;
    int const (* const cpacx)[n] = pacx;
    
    int const *        apcx[] = {pcx, pcx, pcx};
    int       * const  acpx[] = {cpx, cpx, cpx};
    int const * const acpcx[] = {cpcx, cpcx, cpcx};

    // Const behavior
    // cppx    = ppx; // ❌
    // *cppx   = px;  // ✅
    // *pcpx   = px;  // ❌
    // pcpx    = ppx; // ✅
    // **pcpx  = y;   // ✅
    // ...etc

    ////////////////////////////////////////
    // Layer 3
    int ***pppx       = &ppx;
    int (**ppax)[n]   = &pax;
    int *(*papx)[]    = &apx;
    int  (*paax)[][n] = &aax;
    int  **appx[]     = {ppx, ppx, ppx};
    int  (*apax[n])[] = {pax, pax, pax};
    int   *aapx[][n]  = {{px, px, px}, {px, px, px}, {px, px, px}};
    int  aaax[][n][n] = {
        {{x,x,x}, {x,x,x}, {x,x,x}},
        {{x,x,x}, {x,x,x}, {x,x,x}},
        {{x,x,x}, {x,x,x}, {x,x,x}}
    };

    int  *adax[] = {ax, ax, ax};

    // Usage
    assert( ***pppx         == x);
    assert( (**ppax)[1]     == x);
    assert( *(*papx)[1]     == x);
    assert(  (*paax)[1][1]  == x);
    assert(  **appx[1]      == x);
    assert(  (*apax[1])[1]  == x);
    assert(   *aapx[1][1]   == x);
    assert(   aaax[1][1][1] == x);

    // Compile-time info

    // Const
    T const (* const acpacx[n])[n] = {cpacx, cpacx, cpacx};
}

void cpp_array_syntax() {
    int x = 8, y = 9;
    int const cx = x, cy = y;
    
    ////////////////////////////////////////
    // std::array
    std::array<T, N> ax = {x, x, x};

    // Const
    std::array<const T, N>  acx = {x, x, x};
    const std::array<T, N>  cax = {x, x, x};
    const std::array<T, N> cacx = {cx, cx, cx};

    // Const behavior
    //   ax[0] = 9; // ✅
    //  cax[0] = 9; // ❌
    //  acx[0] = 9; // ❌
    // cacx[0] = 9; // ❌
    //   ax = {9, 9, 9}; // ✅
    //  cax = {9, 9, 9}; // ❌
    //  acx = {9, 9, 9}; // ❌
    // cacx = {9, 9, 9}; // ❌
    // NOTE: const propogates so cax, acx, cacx are behaviorly the same. Use cax.

    ////////////////////////////////////////
    // std::span
    std::span<T> sx = ax; // = acx ❌

    // Const
          std::span<const T>  scx = cax; // = acx, = cacx ✅
    const std::span<      T>  csx =  ax; // = acx, = cax ❌
    const std::span<const T> cscx = cax;

    // Const behavior
    //   sx[0] = 9; // ✅
    //  scx[0] = 9; // ❌
    //  csx[0] = 9; // ✅
    // cscx[0] = 9; // ✅
    //   sx = sx.subspan(1);  // ✅
    //  scx = sx.subspan(1);  // ✅
    //  csx = csx.subspan(1); // ❌
    // cscx = csx.subspan(1); // ❌
 
    ////////////////////////////////////////
    // std::mdspan
    using ext = std::extents<int, 1, N>;

    std::mdspan<T, ext> mx {ax.data()};

    const std::mdspan<      T, ext>  cmx { ax.data()};
          std::mdspan<const T, ext>  mcx {cax.data()};
    const std::mdspan<const T, ext> cmcx {cax.data()};

    std::array<T, N> ax2 = {9, 9, 9};
    //   mx[0,0] = 9; // ✅
    //  mcx[0,0] = 9; // ❌
    //  cmx[0,0] = 9; // ✅
    // cmcx[0,0] = 9; // ❌
    //   mx = std::mdspan<T, ext> {ax2.data()}; // ✅
    //  mcx = std::mdspan<T, ext> {ax2.data()}; // ✅
    //  cmx = std::mdspan<T, ext> {ax2.data()}; // ❌
    // cmcx = std::mdspan<T, ext> {ax2.data()}; // ❌


}

void print(const T mat[][N], const int m) {
    // Pointer decay will always result in the first dimension's size
    // information being dropped by the compiler. So `mat[M][N]` would be 
    // misleading as this function declaration will accept a[X][N] for all X 
    // and could result in UB if X < M. Therefore, `a[][N]` is the preferred 
    // syntax.

    std::print("Contiguous array = [");
    constexpr int n = sizeof(mat[0]) / sizeof(mat[0][0]);
    static_assert(n == N);

    for (int i = 0; i < m; ++i) {
        std::print("[");
        for (int j = 0; j < n; ++j) {
            std::print("{} ", mat[i][j]);
        }
        std::print("]");
    }
    std::println("]");
}

void print(const T (* const mat[])[N], const int m) {
    std::print("Non-contiguous array = [");
    constexpr int n = sizeof(*mat[0]) / sizeof((*mat[0])[0]);
    static_assert(n == N);

    for (int i = 0; i < m; ++i) {
        std::print("[");
        for (int j = 0; j < n; ++j) {
            std::print("{} ", (*mat[i])[j]);
        }
        std::print("]");
    }
    std::println("]");
}

void print(const T * const mat[], const int m, const std::span<const int> ns) {
    std::print("Jagged array = [");
    for (int i = 0; i < m; ++i) {
        const int n = ns[i];
        std::print("[");
        for (int j = 0; j < n; ++j) {
            std::print("{} ", mat[i][j]);
        }
        std::print("]");
    }
    std::println("]");
}

void print(const std::array<std::array<T, N>, M> mat) {
    std::print("std::array 2D = [");
    constexpr int m = std::ssize(mat);
    constexpr int n = std::ssize(mat[0]);
    for (int i = 0; i < m; ++i) {
        std::print("[");
        for (int j = 0; j < n; ++j) {
            std::print("{} ", mat[i][j]);
        }
        std::print("]");
    }
    std::println("]");
}

void print(const std::span<const T> arr) {
    std::print("Flat span view = [");
    assert(std::ssize(arr) == N*M);
    for (const auto& x : arr) {
        std::print("{} ", x);
    }
    std::println("]");
}

void print(const std::array<std::span<T>, M> mat) {
    std::print("Array of spans = [");
    for (const auto& row : mat) {
        std::print("[");
        for (const auto& x : row) {
            std::print("{} ", x);
        }
        std::print("]");
    }
    std::println("]");
}


void print(std::mdspan<const T, std::dextents<size_t, 2>> mat) {
    static_assert(mat.rank() == 2);

    const int m = static_cast<int>(mat.extent(0));
    const int n = static_cast<int>(mat.extent(1));
        
    std::print("mdspan = [");
    for (T i = 0; i < m; ++i) {
        std::print("[");
        for (T j = 0; j < n; ++j) {
            std::print("{} ", mat[i, j]);
        }
        std::print("]");
    }
    std::println("]");
}

void print(std::mdspan<const T, std::extents<int, M, N>> mat) {
    static_assert(mat.rank() == 2);
    static_assert(mat.static_extent(0) == M);
    static_assert(mat.static_extent(1) == N);
    std::print("static ");
    print(std::mdspan(mat.data_handle(), M, N));
}

int main() {

    c_array_and_pointer_syntax();
    cpp_array_syntax();
    passing_2darrays_args();
}
