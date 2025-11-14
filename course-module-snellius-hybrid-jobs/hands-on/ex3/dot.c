#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define REP 100

// Dot product function: result = sum(x[i] * y[i])
double dot(size_t n, double *x, double *y) {
    double result = 0.0f;
    for (size_t i = 0; i < n; i++) {
        result += x[i] * y[i];
    }
    return result;
}

int main(int argc, char **argv) {
    double result;
    double start, end, elapsed_time;

    if (argc != 2) {
        fprintf(stderr, "Usage: %s <N>\n", argv[0]);
        return 1;
    }

    const size_t n = (size_t)atoi(argv[1]);  // Size of the vectors from command line input

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
        x[i] = 1.0 * sin((double)i);  // Each rank initializes its local x with trigonometric functions
        y[i] = 0.5 * cos((double)i);  // Each rank initializes its local y with trigonometric functions
    }

    // Start the timer
    start = clock();

    // Perform the dot product
    for(size_t i = 0; i < REP; i++) {
        result += dot(n, x, y);
    }

    // Stop the timer
    end = clock();

    // Calculate the elapsed time in seconds
    elapsed_time = (double)(end - start) / CLOCKS_PER_SEC;

    // Print the result and elapsed time
    printf("Dot product result: %g\n", result);
    printf("Time taken for dot product execution: %g seconds\n", elapsed_time);

    // Free the allocated memory
    free(x);
    x = NULL;
    free(y);
    y = NULL;

    return 0;
}
