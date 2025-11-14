#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define REP 100

void axpy(size_t n, double a, double *x, double *y) {
    for (size_t i = 0; i < n; i++) {
        y[i] = a * x[i] + y[i];
    }
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <N>\n", argv[0]);
        return 1;
    }

    const size_t n = (size_t)atoi(argv[1]);  // Size of the vectors from command line input
    const double a = 2.0f;                    // Scalar multiplier

    printf("Lenght of the arrays: %ld\n", n);

    // Allocate memory for the vectors
    double *x = (double*) malloc(n * sizeof(double));
    double *y = (double*) malloc(n * sizeof(double));

    // Check for successful memory allocation
    if (x == NULL || y == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }

    // Initialize the vectors
    for (size_t i = 0; i < n; i++) {
        x[i] = 1.0f;
        y[i] = 2.0f;
    }

    // Start the timer
    clock_t start = clock();

    // Perform the AXPY operation
    for(size_t i = 0; i < REP; i++) {
        axpy(n, a, x, y);
    }

    // Stop the timer
    clock_t end = clock();

    // Calculate the elapsed time in seconds
    double elapsed_time = (double)(end - start) / CLOCKS_PER_SEC;

    // Print the result and elapsed time
    printf("y[0] = %f\n", y[0]);
    printf("Time taken for axpy execution: %f seconds\n", elapsed_time);

    // Free the allocated memory
    free(x);
    x = NULL;
    free(y);
    y = NULL;

    return 0;
}
