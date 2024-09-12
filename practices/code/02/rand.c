#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(void)
{
    srand(time(NULL));
    while (1) {
        uint32_t value = rand();
        fwrite((void*) &value, sizeof(value), 1, stdout);
    }
    return 0;
}
