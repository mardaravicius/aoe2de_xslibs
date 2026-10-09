#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static inline uint32_t rotl(const uint32_t x, int k) {
	return (x << k) | (x >> (32 - k));
}


static uint32_t s[4];

uint32_t next(void) {
	const uint32_t result = rotl(s[1] * 5, 7) * 9;

	const uint32_t t = s[1] << 9;

	s[2] ^= s[0];
	s[3] ^= s[1];
	s[1] ^= s[2];
	s[0] ^= s[3];

	s[2] ^= t;

	s[3] = rotl(s[3], 11);

	return result;
}

static uint32_t state;

uint32_t splitmix32(void) {
    uint32_t z = (state += 0x9e3779b9);
    z ^= z >> 16; z *= 0x21f0aaad;
    z ^= z >> 15; z *= 0x735a2d97;
    z ^= z >> 15;
    return z;
}

void seed_from_int32(int32_t seed) {
    state = (uint32_t) seed;
    s[0] = splitmix32();
    s[1] = splitmix32();
    s[2] = splitmix32();
    s[3] = splitmix32();
    if (s[0] == 0 && s[1] == 0 && s[2] == 0 && s[3] == 0) {
        s[0] = 1;
    }
}

int main(int argc, char **argv) {
    if (argc < 3) {
        return -1;
    }

    char *end;
    int32_t seed = (int32_t) strtol(argv[1], &end, 10);
    if (end == argv[1]) {
        return -2;
    }
    int32_t iterations = (int32_t) strtol(argv[2], &end, 10);
    if (end == argv[2]) {
        return -2;
    }

    seed_from_int32(seed);
    for (int32_t i = 0; i < iterations; i++) {
        printf("%d\n", (int32_t) next());
    }
    return 0;
}