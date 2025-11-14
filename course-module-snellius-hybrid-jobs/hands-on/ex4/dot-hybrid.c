#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <mpi.h>
#include <omp.h>

#define REP 100

double dot(size_t local_n, double *x, double *y) {
    double local_sum = 0.0f;

    #pragma omp parallel for reduction(+:local_sum)
    for (size_t i = 0; i < local_n; i++) {
        local_sum += x[i] * y[i];
    }

    return local_sum;
}

/*
double dot(size_t local_n, double *x, double *y) {
    double local_sum = 0.0f;
    const int threads = omp_get_num_threads();

    #pragma omp parallel default(shared) reduction(+:local_sum)
    {
        const int tid = omp_get_thread_num();
        const int remainder = local_n % threads;
        size_t thread_n, offset;

        if (tid < remainder) {
            thread_n = local_n / threads + 1;
            offset = thread_n * tid;
        } else {
            thread_n = local_n / threads;
            offset = thread_n * tid + remainder;
        }

        printf("Thread %d from %ld to %ld\n", tid, offset, offset + thread_n);
        for (size_t i = offset; i < offset + thread_n; i++) {
            local_sum += x[i] * y[i];
        }
    }

    return local_sum;
}
*/

int main(int argc, char **argv) {
    int rank, world;
    size_t local_n, remainder, offset;
    double *x, *y, result = 0.0;
    double start_time, end_time;

    // Initialize MPI
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);  // Get rank of the process
    MPI_Comm_size(MPI_COMM_WORLD, &world);  // Get number of processes

    // Read the global size N from the command line argument
    if (argc != 2) {
        if (rank == 0) {
            printf("Usage: %s <vector_size>\n", argv[0]);
        }
        MPI_Finalize();
        return -1;
    }
    const size_t n = (size_t)atoi(argv[1]);

    // Calculate local sizes based on the rank
    remainder = n % world;
    if (rank < remainder) {
        local_n = n / world + 1;
        offset = local_n * rank;
    } else {
        local_n = n / world;
        offset = local_n * rank + remainder; 
    }

    if (rank == 0) {
        printf("Global length of the arrays: %ld\n", n);
        printf("Local length of the arrays: %ld\n", local_n);
    }

    // Allocate memory for the local vectors
    x = (double *)malloc(local_n * sizeof(double));
    y = (double *)malloc(local_n * sizeof(double));

    // Check for successful memory allocation
    if (x == NULL || y == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }

    // Initialize local vectors
    for (size_t i = 0; i < local_n; i++) {
        x[i] = 1.0 * sin((double)(i + offset));  // Each rank initializes its local x with trigonometric functions
        y[i] = 0.5 * cos((double)(i + offset));  // Each rank initializes its local y with trigonometric functions
    }

    // Start the timer
    MPI_Barrier(MPI_COMM_WORLD);  // Synchronize before timing
    start_time = MPI_Wtime();

    // Perform the local dot product computation using OpenMP
    for(size_t i = 0; i < REP; i++) {
        result += dot(local_n, x, y);

        // Reduce the local dot products to a global sum
        MPI_Allreduce(MPI_IN_PLACE, &result, 1, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
    }


    // Stop the timer
    MPI_Barrier(MPI_COMM_WORLD);  // Synchronize after computation
    end_time = MPI_Wtime();

    // Print the result and time on rank 0
    if (rank == 0) {
        printf("Global dot product result: %g\n", result);
        printf("Time taken for dot product execution: %g seconds\n", end_time - start_time);
    }

    // Free the allocated memory
    free(x);
    x = NULL;
    free(y);
    y = NULL;

    // Finalize MPI
    MPI_Finalize();

    return 0;
}
