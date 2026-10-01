#include <cstdint>
#include <iostream>
#include <limits>
int main() {
    static_assert(__cplusplus >= 201703L, "C++17 required");
    static_assert(std::numeric_limits<std::int64_t>::digits >= 63, "wide delay accumulator required");
    std::cout << "C++17 ready; int64 bits=" << std::numeric_limits<std::int64_t>::digits + 1 << '\n';
}
