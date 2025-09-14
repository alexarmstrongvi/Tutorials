#include <fmt/core.h>

#include <array>
#include <bitset>
#include <cstddef>
#include <format>
#include <print>
#include <sstream>
#include <type_traits>
#include <utility>

// Suppress switch-related warnings (Clang, GCC, MSVC)
#if defined(__clang__)
// Clang
#define DISABLE_SWITCH_DEFAULT_WARNINGS \
     _Pragma("clang diagnostic push") \
     _Pragma("clang diagnostic ignored \"-Wswitch-default\"")
#define RESTORE_SWITCH_DEFAULT_WARNINGS \
     _Pragma("clang diagnostic pop")

#elif defined(__GNUC__)
// GCC
#  define DISABLE_SWITCH_DEFAULT_WARNINGS \
     _Pragma("GCC diagnostic push") \
     _Pragma("GCC diagnostic ignored \"-Wswitch-default\"")
#  define RESTORE_SWITCH_DEFAULT_WARNINGS \
     _Pragma("GCC diagnostic pop")

#elif defined(_MSC_VER)
// MSVC
#  define DISABLE_SWITCH_DEFAULT_WARNINGS \
     __pragma(warning(push)) \
     __pragma(warning(disable:4061))
#  define RESTORE_SWITCH_DEFAULT_WARNINGS \
     __pragma(warning(pop))

#else
// Unknown compiler — no-op
#  define DISABLE_SWITCH_DEFAULT_WARNINGS
#  define RESTORE_SWITCH_DEFAULT_WARNINGS
#endif

////////////////////////////////////////////////////////////////////////////////
// Enum and Enum Flag library
////////////////////////////////////////////////////////////////////////////////

template <typename E> concept Enum = std::is_enum_v<E>;

template <Enum E> struct enum_traits {
    using enum_type = E;
    using underlying_type = std::underlying_type_t<E>;
    using array_type = std::array<E, 0>;

    static constexpr std::string type_name = "";
    static constexpr array_type values = {};
    static constexpr std::string_view to_string(E e);
    // static constexpr std::array<std::string_view, 0> names = {};
};


template <Enum E>
constexpr auto enum_values() noexcept { return enum_traits<E>::values; }

template <Enum E>
constexpr std::string_view to_string(E e) noexcept { return enum_traits<E>::to_string(e); }

template <Enum E> 
constexpr std::size_t enum_size_v = enum_traits<E>::values.size();

template<Enum E>
struct std::formatter<E> : std::formatter<std::string_view> {
    auto format(E c, auto& ctx) const {
        return std::formatter<std::string_view>::format(enum_traits<E>::to_string(c), ctx);
    }
};
template<Enum E>
struct fmt::formatter<E> : fmt::formatter<std::string_view> {
    auto format(E c, auto& ctx) const {
        return fmt::formatter<std::string_view>::format(enum_traits<E>::to_string(c), ctx);
    }
};

template <Enum E>
class EnumFlag : private std::bitset<enum_size_v<E>>
{
    using Base = std::bitset<enum_size_v<E>>;

public:
    constexpr EnumFlag() = default;
    constexpr EnumFlag(E e) { set(e); }
    constexpr EnumFlag(std::initializer_list<E> es) { for (auto e : es) set(e); }

    // Use bitset methods
    using Base::operator|=;
    using Base::operator&=;
    using Base::operator^=;
    using Base::reset;
    using Base::set;
    using Base::flip;
    using Base::any;
    using Base::none;
    using Base::all;
    using Base::count;
    using Base::size;
    using Base::operator==;
    using Base::operator~;
    using Base::to_ulong;
    using Base::to_ullong;
    friend EnumFlag<E> operator|(EnumFlag<E> lhs, EnumFlag<E> rhs) {
        lhs |= rhs;
        return lhs;
    }
    friend EnumFlag<E> operator&(EnumFlag<E> lhs, EnumFlag<E> rhs) {
        lhs &= rhs;
        return lhs;
    }
    friend EnumFlag<E> operator^(EnumFlag<E> lhs, EnumFlag<E> rhs) {
        lhs ^= rhs;
        return lhs;
    }

    // Implement methods that must convert enum to underlying type
    constexpr EnumFlag& set(E e, bool value = true) {
        Base::set(std::to_underlying(e), value);
        return *this;
    }

    constexpr bool test(E e) const {
        return Base::test(std::to_underlying(e));
    }

    // Getters
    constexpr const Base& bits() const noexcept { return *this; }
};


template <Enum E>
constexpr EnumFlag<E> operator|(E lhs, E rhs) {
    return EnumFlag<E>({lhs, rhs});
}

template <Enum E, typename CharT>
auto format_impl(const EnumFlag<E>& flags, auto& ctx) {
    std::basic_ostringstream<CharT> oss;
    oss << "<" << enum_traits<E>::type_name;
    if (flags.any()) {
        oss << ".";
        bool first = true;
        for (auto e : enum_values<E>()) {
            if (flags.test(e)) {
                if (!first) oss << '|';
                oss << std::format("{}", e);
                first = false;
            }
        }
    }
    oss << ": " << flags.to_ullong() << '>';

    return std::ranges::copy(oss.str(), ctx.out()).out;
}


template <Enum E, typename CharT>
struct std::formatter<EnumFlag<E>, CharT> {
    constexpr auto parse(auto& ctx) { return ctx.begin(); }

    auto format(const EnumFlag<E>& flags, auto& ctx) const {
        return format_impl<E, CharT>(flags, ctx);
    }
};

template <Enum E, typename CharT>
struct fmt::formatter<EnumFlag<E>, CharT> {
    constexpr auto parse(auto& ctx) { return ctx.begin(); }

    auto format(const EnumFlag<E>& flags, auto& ctx) const {
        return format_impl<E, CharT>(flags, ctx);
    }
};

////////////////////////////////////////////////////////////////////////////////
enum class Color : uint8_t
{
    Red,
    Green,
    Blue,
};
template <>
struct enum_traits<Color> {
    using enum Color;

    static constexpr std::string type_name = "Color";

    static constexpr std::string_view to_string(Color c) noexcept {
        DISABLE_SWITCH_DEFAULT_WARNINGS
        switch (c) {
            case Red:   return "Red";
            case Green: return "Green";
            case Blue:  return "Blue";
        }
        RESTORE_SWITCH_DEFAULT_WARNINGS
    }

    static constexpr std::array values{
        Red,
        Green,
        Blue,
    };

};

////////////////////////////////////////////////////////////////////////////////
struct Person {
    std::string name;
    int         age;
    double      height;
    Color       color;
};

auto format_impl(const Person& p, auto& ctx) {
    return std::format_to(
        ctx.out(),
        "Person{{name={}, age={}, height={}, color={}}}",
        p.name, p.age, p.height, p.color
    );
}
template<>
struct std::formatter<Person> {
    constexpr auto parse(auto& ctx) { return ctx.begin(); }
    auto format(const Person& p, auto& ctx) const { return format_impl(p, ctx); }
};
template<>
struct fmt::formatter<Person> {
    constexpr auto parse(auto& ctx) { return ctx.begin(); }
    auto format(const Person& p, auto& ctx) const { return format_impl(p, ctx); }
};

////////////////////////////////////////////////////////////////////////////////
int main(int32_t, char**) {


    std::println("Formatting an Enum: {} values", enum_size_v<Color>);
    std::println("enum : {}", Color::Red);
    fmt::println("enum : {}", Color::Blue);
    std::print("All {} enum values: ", enum_size_v<Color>);
    for (auto& c : enum_values<Color>()) {
        std::print(" {}", c);
    }
    std::print("\n\n");

    std::println("Formatting an EnumFlag");
    EnumFlag<Color> colors1; 
    EnumFlag<Color> colors2(Color::Red); 
    EnumFlag<Color> colors3({Color::Red, Color::Blue}); 
    EnumFlag<Color> colors4(Color::Red | Color::Blue); 
    std::println("EnumFlag : {}", colors1);
    std::println("EnumFlag : {}", colors2);
    std::println("EnumFlag : {}", colors3);
    std::println("EnumFlag : {}", colors4);
    fmt::println("EnumFlag : {} [fmt]", colors4);

    EnumFlag<Color> colors; 
    colors = Color::Red | Color::Blue;
    std::println("EnumFlag : {}", colors);
    colors.set(Color::Green);
    std::println("EnumFlag : {}", colors);
    std::println("EnumFlag : has Green? {}", colors.test(Color::Green));
    std::println();

    std::println("Formatting a struct");
    Person person{.name = "John", .age = 23, .height = 6.2, .color = Color::Red};
    std::println("struct : {}", person);
    fmt::println("struct : {}", person);
    std::println();
}
