#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <omp.h>

#define REP 100

void axpy(size_t local_n, double a, double *x, double *y) {
    #pragma omp parallel for
    for (size_t i = 0; i < local_n; i++) {
        y[i] = a * x[i] + y[i];
    }
}

int main(int argc, char **argv) {
    int rank, world;
    size_t n, local_n, remainder;
    double a = 2.0;
    double *x, *y;
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
    n = atoi(argv[1]);

    // Calculate local sizes based on the rank
    remainder = n % world;
    if (rank < remainder) {
        local_n = n / world + 1;
    } else {
        local_n = n / world;
    }

    if (rank == 0) {
        printf("Global length of the arrays: %ld\n", n);
        printf("Local length of the arrays: %ld\n", local_n);
    }

    // Allocate memory for the local vectors
    x = (double *)malloc(local_n * sizeof(double));
    y = (double *)malloc(local_n * sizeof(double));

    // Initialize local vectors
    for (size_t i = 0; i < local_n; i++) {
        x[i] = 1.0f;  // Each rank initializes its local x with 1.0
        y[i] = 2.0f;  // Each rank initializes its local y with 2.0
    }

    // Start the timer
    MPI_Barrier(MPI_COMM_WORLD);  // Synchronize before timing
    start_time = MPI_Wtime();

    // Perform the local axpy computation using OpenMP
    for(size_t i = 0; i < REP; i++) {
        axpy(local_n, a, x, y);
    }

    // Stop the timer
    MPI_Barrier(MPI_COMM_WORLD);  // Synchronize after computation
    end_time = MPI_Wtime();

    // Print the result and time on rank 0
    if (rank == 0) {
        printf("y[0] = %f\n", y[0]);
        printf("Time taken for axpy execution: %f seconds\n", end_time - start_time);
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
