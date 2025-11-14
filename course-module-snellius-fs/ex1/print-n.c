#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

void generate_random_values(double *array, int n){
    srand(time(NULL));

    for(int i=0; i<n; ++i){
        array[i] = (double)rand()/RAND_MAX; // Generate a random value between 0 and 1
    }
}

void print_to_file_ascii(const char *filename, double *array, int n){
    FILE *output_file = fopen(filename, "w");
    if(output_file==NULL){
        printf("Error opening file for writing\n");
        return;
    }

    for(int i=0; i<n; i++){
        fprintf(output_file, "%.6lf\n", array[i]);
    }

    fclose(output_file);
}

void print_to_file_binary(const char *filename, double *array, int n){
    FILE *output_file = fopen(filename, "wb");
    if(output_file==NULL){
        printf("Error opening file for writing\n");
        return;
    }

    fwrite(array, sizeof(double), n, output_file);

    fclose(output_file);
}

int main(int argc, char** argv){
    if(argc!=4){
        printf("Usage: %s <file> <n> <format>\n", argv[0]);
        printf("  <n> must be a positive integer'\n");
        printf("  <file> must be a valid file name\n");
        printf("  <format> must be either 'ascii' or 'binary'\n");
        return 1;
    }

    long int n = atoi(argv[1]);
    const char* filename = argv[2];
    const char* format = argv[3];

    if(n<=0){
        printf("Parameter <n> must be a positive integer\n");
        return 1;
    }

    double* array = (double*)malloc(sizeof(double)*n);

    if(array==NULL){
        printf("Memory allocation failed\n");
        return 1;
    }

    generate_random_values(array, n);

    clock_t start = clock(); // Start the timer

    if(strcmp(format, "ascii")==0){
        print_to_file_ascii(filename, array, n);
    }
    else if(strcmp(format, "binary")==0){
        print_to_file_binary(filename, array, n);
    }
    else{
        printf("Parameter <format> must be either 'ascii' or 'binary'\n");
    }

    clock_t end = clock(); // Stop the timer
    double elapsed_time = (double)(end - start)/CLOCKS_PER_SEC;

    // Calculate data size in MB and data transfer rate in MB/s
    double data_size = (double)(sizeof(double)*n)/(1.0e6); // Data size in MB
    double transfer_rate = data_size/elapsed_time; // Data transfer rate in MB/s

    printf("%ld random double-precision values written to %s in %s format\n", n, filename, format);
    printf(" Elapsed time [s]: %.6f\n", elapsed_time);
    printf(" Buffer size [MB]: %ld\n", sizeof(double)*n);
    printf(" Transfer rate [MB/s]: %.6f\n", transfer_rate);

    free(array);

    return 0;
}
