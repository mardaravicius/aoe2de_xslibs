#include <iostream>
#include <random>
#include <cstdint>
#include <string>

int main(const int argc, const char * const * const argv) {
    if (argc < 3) {
        return -1;
    }
    try {
        const int32_t seed = static_cast<int32_t>(std::stol(argv[1]));
        const int32_t iterations = static_cast<int32_t>(std::stol(argv[2]));
        std::mt19937 mt(seed);
        for (int32_t i = 0; i < iterations; i++) {
            const int32_t i32 = static_cast<int32_t>(mt());
            std::cout << i32 << "\n";
        }
        return 0;
    } catch (const std::exception& e) {
        return -2;
    }
}