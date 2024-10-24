#include <stdio.h>
#include <stdint.h>
#include <time.h>
#include <math.h>

void bench(uint64_t lim)
{
    clock_t start_time = clock();
    for (uint64_t i = 0; i < lim; ++i);
    float end_time = (float)(clock() - start_time) / CLOCKS_PER_SEC;
    printf("Reaching %010llx took: %f\n", lim, end_time);
}

int main(void)
{
    uint64_t u31 = 0x7fffffff;
    uint64_t u32 = 0xffffffff;
    uint64_t u33 = 0x01ffffffff;

    bench(u31);
    bench(u32);
    bench(u33);

    // Adding one bit doubles the computation time of the full space.
    // If iterating over the full 32-bit space takes 5s,
    // then iterating over the full 64-bit space will take
    // 5 * 2^32 = 21 474 836 480s which is > 680 years.

    return 0;
}
