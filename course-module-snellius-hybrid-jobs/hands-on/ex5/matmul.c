#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#define REP 100

// Matrix multiplication function: C = A * B
void matmul(size_t n, double **A, double **B, double **C) {
    for (size_t i = 0; i < n; i++) {
        for (size_t j = 0; j < n; j++) {
            C[i][j] = 0.0;
            for (size_t k = 0; k < n; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

int main(int argc, char **argv) {
    double start, end, elapsed_time;

    if (argc != 2) {
        fprintf(stderr, "Usage: %s <N>\n", argv[0]);
        return 1;
    }

    const size_t n = (size_t)atoi(argv[1]);  // Matrix size from command line input

    printf("Matrix size: %ld x %ld\n", n, n);

    // Allocate memory for the matrices
    double **A = (double**) malloc(n * sizeof(double*));
    double **B = (double**) malloc(n * sizeof(double*));
    double **C = (double**) malloc(n * sizeof(double*));

    for (size_t i = 0; i < n; i++) {
        A[i] = (double*) malloc(n * sizeof(double));
        B[i] = (double*) malloc(n * sizeof(double));
        C[i] = (double*) malloc(n * sizeof(double));
    }

    // Check for successful memory allocation
    if (A == NULL || B == NULL || C == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }

    // Initialize the matrices
    for (size_t i = 0; i < n; i++) {
        for (size_t j = 0; j < n; j++) {
            A[i][j] = 1.0;  // Initialize matrix A with trigonometric function
            B[i][j] = 2.0;  // Initialize matrix B with trigonometric function
        }
    }

    // Start the timer
    start = clock();

    // Perform matrix multiplication REP times
    for (size_t i = 0; i < REP; i++) {
        matmul(n, A, B, C);
    }

    // Stop the timer
    end = clock();

    // Calculate the elapsed time in seconds
    elapsed_time = (double)(end - start) / CLOCKS_PER_SEC;

    // Print the elapsed time
    printf("Time taken for matrix multiplication: %g seconds\n", elapsed_time);

    // Free the allocated memory
    for (size_t i = 0; i < n; i++) {
        free(A[i]);
        free(B[i]);
        free(C[i]);
    }
    free(A);
    free(B);
    free(C);

    return 0;
}
