#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <errno.h>
#include <stdint.h>

void generate_random_values(double *array, long n){
    srand(time(NULL));

    for(long i=0; i<n; ++i){
        array[i] = (double)rand()/RAND_MAX; // Generate a random value between 0 and 1
    }
}

// Flush the data to the file system and return the number of bytes written
long close_file(FILE *output_file){
    int failed = ferror(output_file);
    if(fflush(output_file) != 0) failed = 1;
    if(fsync(fileno(output_file)) != 0) failed = 1;
    long bytes = ftell(output_file);
    if(bytes < 0) failed = 1;
    if(fclose(output_file) != 0) failed = 1;
    if(failed){
        fprintf(stderr, "Error writing or flushing output file\n");
        return -1;
    }
    return bytes;
}

long print_to_file_ascii(const char *filename, double *array, long n){
    FILE *output_file = fopen(filename, "w");
    if(output_file==NULL){
        printf("Error opening file for writing\n");
        return -1;
    }

    for(long i=0; i<n; i++){
        fprintf(output_file, "%.6lf\n", array[i]);
    }

    return close_file(output_file);
}

long print_to_file_binary(const char *filename, double *array, long n){
    FILE *output_file = fopen(filename, "wb");
    if(output_file==NULL){
        printf("Error opening file for writing\n");
        return -1;
    }

    fwrite(array, sizeof(double), n, output_file);

    return close_file(output_file);
}

int main(int argc, char** argv){
    if(argc!=4){
        printf("Usage: %s <n> <file> <format>\n", argv[0]);
        printf("  <n> must be a positive integer'\n");
        printf("  <file> must be a valid file name\n");
        printf("  <format> must be either 'ascii' or 'binary'\n");
        return 1;
    }

    char *number_end;
    errno = 0;
    long int n = strtol(argv[1], &number_end, 10);
    const char* filename = argv[2];
    const char* format = argv[3];

    if(errno || number_end == argv[1] || *number_end || n<=0 || (unsigned long)n > SIZE_MAX/sizeof(double)){
        printf("Parameter <n> must be a positive integer\n");
        return 1;
    }

    double* array = (double*)malloc(sizeof(double)*n);

    if(array==NULL){
        printf("Memory allocation failed\n");
        return 1;
    }

    generate_random_values(array, n);

    long bytes = -1;
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start); // Start the wall-clock timer

    if(strcmp(format, "ascii")==0){
        bytes = print_to_file_ascii(filename, array, n);
    }
    else if(strcmp(format, "binary")==0){
        bytes = print_to_file_binary(filename, array, n);
    }
    else{
        printf("Parameter <format> must be either 'ascii' or 'binary'\n");
    }

    clock_gettime(CLOCK_MONOTONIC, &end); // Stop the timer
    double elapsed_time = (double)(end.tv_sec - start.tv_sec) + (double)(end.tv_nsec - start.tv_nsec)/1.0e9;

    if(bytes<0){
        free(array);
        return 1;
    }

    // Calculate the size of the written file in MB and data transfer rate in MB/s
    double data_size = (double)bytes/(1.0e6); // Data size in MB
    double transfer_rate = data_size/elapsed_time; // Data transfer rate in MB/s

    printf("%ld random double-precision values written to %s in %s format\n", n, filename, format);
    printf(" Elapsed time [s]: %.6f\n", elapsed_time);
    printf(" File size [MB]: %.6f\n", data_size);
    printf(" Transfer rate [MB/s]: %.6f\n", transfer_rate);

    free(array);

    return 0;
}
