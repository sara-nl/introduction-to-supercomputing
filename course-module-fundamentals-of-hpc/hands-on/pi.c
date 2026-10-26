#include <omp.h>
#include <stdio.h>

int main(void) {
    const long steps = 100000000;
    const double width = 1.0 / steps;
    double sum = 0.0;
    double start = omp_get_wtime();
#pragma omp parallel for reduction(+:sum)
    for (long i = 0; i < steps; ++i) {
        double x = (i + 0.5) * width;
        sum += 4.0 / (1.0 + x * x);
    }
    printf("pi = %.9f; threads = %d; elapsed = %.6f s\n",
           width * sum, omp_get_max_threads(), omp_get_wtime() - start);
    return 0;
}
