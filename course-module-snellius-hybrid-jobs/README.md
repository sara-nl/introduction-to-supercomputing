# Snellius hybrid jobs

## Introduction

### About the course module and hands-on session

> [!NOTE]
> The materials for this course module have been adapted from *Introducción a la Supercomputación* by **José Luis Bosque, Borja Pérez, Ramón Beivide,** and **Carmen Martínez** of the Universidad de Cantabria. This adaptation was carried out by the EuroCC NL team at SURF. For more information about the EuroCC2 project, please visit [EuroCC2](https://www.eurohpc-ju.europa.eu/research-innovation/our-projects/eurocc-2_en). The EuroCC NL team expresses gratitude to the original authors for their contributions to these materials.

In this session, we will dive deeper into the Slurm resource manager, focusing on understanding key parameters for efficient parallel job scheduling, including threads, cores, sockets, nodes, and processes. Our goal is to connect to the Snellius supercomputer and explore hybrid job execution, which leverages both shared-memory (OpenMP) and distributed-memory (MPI) parallelism.

We will explore three basic linear algebra kernels, each with a different parallel nature:

1. **Linear combination of vectors (axpy)**: The operation $$y \gets a * x + y$$, known as *axpy*, is a pointwise operation where each element of the vectors `x` and `y` can be updated independently. This makes it an embarrassingly parallel task, meaning all operations can be executed simultaneously without any inter-task communication.
2. **Dot product (scalar product)**: The dot product of two vectors, $$z \gets \sum_{i=1}^{n} x_i * y_i$$, involves multiplying corresponding elements of two vectors and summing the results. The parallel complexity arises from the need for a reduction operation to sum the products. This requires synchronization between threads or processes to accumulate the intermediate sums.
3. **Matrix multiplication**: The matrix product $$C \gets A * B$$ is more complex, as it involves computing the dot product of rows from matrix `A` with columns from matrix `B`. Efficient parallelization requires distributing the data across multiple nodes or threads, managing both computation and data transfer, which introduces a higher level of parallel complexity compared to vector operations.

The provided materials include these implementations:

- A **sequential** version of each kernel, to understand the basic functionality (`ex1` axpy, `ex3` dot product, `ex5` matrix multiplication).
- A **hybrid** version of axpy (`ex2`) and the dot product (`ex4`), combining shared-memory (OpenMP) and distributed-memory (MPI) parallelization. Matrix multiplication has no hybrid version; parallelizing `ex5/matmul.c` is left as an open exercise.

The main objective is to gain practical experience in running hybrid jobs on supercomputing systems, focusing on the challenges and strategies for parallelizing different computations.

You can find the materials and example codes in the linked repository. This document will guide you through the exercises step by step.

### Snellius supercomputer

We will work with a small subset of the Snellius supercomputer, a powerful system with a total computational performance of 37.9 petaFLOPS. Snellius consists of over 1,500 compute nodes interconnected via a high-speed InfiniBand network. The system is equipped with a variety of processors and GPUs, including AMD Genoa CPUs and NVIDIA H100 GPUs, optimized for tasks ranging from high-performance scientific computing to AI workloads.

Snellius features a range of node types:

- **Thin nodes**: 1,263 nodes with AMD Rome or Genoa CPUs, each containing either 128 or 192 CPU cores, for a total of over 208,000 cores.
- **Fat nodes**: 120 nodes, each with 1 TiB or 1.5 TiB of RAM, intended for memory-intensive jobs.
- **High-memory nodes**: 4 nodes with 4 TiB or 8 TiB of RAM, intended for extremely memory-intensive jobs.
- **GPU nodes**: 160 nodes equipped with 4 NVIDIA A100 or H100 GPUs per node, designed for massively parallel computations such as machine learning and molecular dynamics.

The front-end nodes of the cluster are accessed via `snellius.surf.nl`, and all job submissions and resource management are handled through Slurm. For additional details on the system, you can refer to the [SURF User Knowledge Base](https://servicedesk.surf.nl/wiki/spaces/WIKI/pages/30660184/Snellius) or explore the [Snellius virtual tour](https://visualization.surf.nl/snellius-virtual-tour/) for a more interactive overview.

### Connecting to Snellius

Since this module is part of the third section in the *Introduction to Supercomputing* course series, we assume that participants already have established connections to Snellius and are familiar with the system, including moving data and interacting with the filesystem. 

However, if needed, you can refer to the following guides for assistance:

- [Connecting to the system](https://servicedesk.surf.nl/wiki/spaces/WIKI/pages/30660216/Connecting+to+the+system).
- [Interacting with the filesystem](https://servicedesk.surf.nl/wiki/spaces/WIKI/pages/92668034/Interacting+with+the+filesystem).

### Snellius environment modules

In a high-performance computing (HPC) cluster, users require access to a variety of software tools, libraries, compilers, and applications. These resources can include various versions of the same software or distinct installations tailored for different hardware architectures. Consequently, managing these resources effectively becomes essential to ensure that users can select the appropriate version and avoid potential conflicts that might arise from incompatible installations.

The environment modules provide a robust solution for this purpose. It allows users to dynamically load and unload specific software modules into their environment, tailoring it to their particular computational needs. By doing so, users can seamlessly switch between different software versions or configurations without the risk of interference between them. 

The advantages of using the `module` command include:

- **Version management**: Users can easily switch between different versions of a software package, ensuring that they run their applications with the correct dependencies and optimizations suited for their particular task.
- **Hardware compatibility**: The cluster may contain software installations optimized for specific hardware, such as GPUs or multi-core CPUs. The `module` system allows users to load the necessary versions that take advantage of the available hardware.
- **Environment configuration**: The `module` command simplifies the setup process by providing an easy interface to manage software dependencies and configurations. This ensures that users can focus on their computations rather than dealing with environment management.

Basic options for the `module` command are listed in the table below.

| Command          | Description                                                                    |
|------------------|--------------------------------------------------------------------------------|
| `module help`    | Provides information about the command options                                 |
| `module avail`   | Displays all modules available in the system                                   |
| `module list`    | Shows the modules currently loaded in your environment                         |
| `module load`    | Loads a new module into your environment                                       |
| `module unload`  | Removes a module from your environment                                         |
| `module purge`   | Removes all modules from your environment                                      |

#### Exercise

In this exercise, you will load the necessary software modules in a Slurm job script and verify that the modules have been loaded correctly by outputting the version of the compiler.

First, **create a Slurm script** named `load_modules.sh` with the following content:

```bash
#!/bin/bash
#SBATCH -J load_modules         # Job name
#SBATCH -o load_modules.out     # Output file
#SBATCH --nodes 1               # Number of nodes
#SBATCH --ntasks 1              # Number of tasks
#SBATCH -t 01:00:00             # Time limit

# Load the necessary modules
module load 2023                # Load the general 2023 module
module load foss/2023a          # Load the foss compiler module

# Verify the loaded modules by checking the version of the compiler
echo "Loaded modules:"
module list                     # Display currently loaded modules

echo "Checking compiler version:"
mpicc -v                        # Output the version of the MPI C compiler
```

**Submit the Slurm job** to the cluster by executing the following command:

```bash
sbatch load_modules.sh
```

**Verify the output** by checking the contents of `load_modules.out` after the job completes. This file will contain:
- A list of the currently loaded modules
- The version information of the MPI C compiler
   
```bash
cat load_modules.out
```

By completing this exercise, you will have successfully loaded the required software modules in a Slurm job script and verified that they are functioning as expected.

### Slurm job scheduler

Slurm (Simple Linux Utility for Resource Management) is a workload manager designed to efficiently manage the execution of tasks across the nodes of a cluster. When a job is submitted, Slurm assesses its requirements, primarily focusing on the number of CPU cores needed. If sufficient resources are available, Slurm executes the job immediately. If not, the job is placed in a queue until the necessary resources are freed up for execution. 

The following table summarizes the basic commands used in Slurm.

| Command               | Description                                             |
|-----------------------|---------------------------------------------------------|
| [`sbatch`](https://slurm.schedmd.com/sbatch.html)     | Submits a script for execution                              |
| [`scancel`](https://slurm.schedmd.com/scancel.html)   | Cancels jobs that are currently running or pending          |
| [`sinfo`](https://slurm.schedmd.com/sinfo.html)       | Displays information about the state of compute nodes       |
| [`squeue`](https://slurm.schedmd.com/squeue.html)     | Provides information about jobs that are running or pending |

A Slurm job script consists of two main sections: the job description and the execution commands. The job description includes directives that specify the resources required for the job. The execution section typically contains the command to run the application, along with any necessary shell commands. Below is an example of a basic job script:

```bash
#!/bin/bash
#SBATCH -J hello               # Job name
#SBATCH -o hello.out           # Output file
#SBATCH --nodes 1              # Number of nodes
#SBATCH --ntasks 1             # Number of tasks
#SBATCH -t 01:00:00            # Time limit

srun ./hello                   # Command to execute
```

In the table below, we have listed some commonly used Slurm directives.

| Option                       | Description                                                              |
|------------------------------|--------------------------------------------------------------------------|
| `--job-name=name`            | Informative name for the job, aiding in identification.                  |
| `--nodes=#`                  | Specifies the number of nodes to utilize.                                |
| `--ntasks=#`                 | Specifies the number of tasks to execute (distributed parallelism).      |
| `--ntasks-per-node=#`        | Number of tasks assigned to each physical node.                          |
| `--cpus-per-task=#`          | Specifies the number of cores allocated per task (shared memory parallelism). |
| `--time=[[DD-]HH:]MM:SS`     | Maximum allowable runtime for the job.                                  |
| `--mem-per-cpu=#`            | RAM required per CPU (in MB).                                           |
| `--mem=#`                    | RAM required per node (in MB).                                          |
| `--output=name`              | File for standard output of the job.                                    |
| `--error=name`               | File for error output of the job.                                       |
| `--chdir=[dirname]`          | Working directory for the job.                                          |

For certain directives, such as the output file name, you can use the wildcard `%j` to include the Slurm job ID. For example, if you specify `--output=out-%j.log` and the job is assigned ID 600, the output will be redirected to `out-600.log` upon job execution.

#### Exercise

The `hostname` command in Linux displays the name of the node on which it is executed. We will write a Slurm script that outputs the names of the nodes where the tasks are executed. Start by executing one task on a single node. Check the output file to ensure it executed on only one node. Next, run the script with 4 and then 8 tasks on a single node. Then, execute the same sequence of jobs but distribute them across two compute nodes. Verify that Slurm indeed assigns two nodes to your job. Finally, modify your script to ensure that when running 8 tasks, they are evenly distributed across the nodes. Check the results.

Here is a sample solution for the exercise:

```bash
#!/bin/bash
#SBATCH -J name                # Job name
#SBATCH -o name.out            # Output file
#SBATCH --nodes 2              # Number of nodes
#SBATCH --ntasks 8             # Total number of tasks
#SBATCH --ntasks-per-node=4    # Tasks per node
#SBATCH -t 01:00:00            # Time limit

srun hostname                  # Execute the hostname command
```

## Hands-on Snellius hybrid jobs

In this section, we will delve into the execution of Slurm hybrid jobs by exploring three basic linear algebra kernels, each with a different parallel nature.

### Linear combination of vectors

The linear combination of vectors, also known as `axpy`, can be written as:

$$y \gets a * x + y$$.

The `axpy` kernel is a simple pointwise operation, which means each computation is independent of the others, making it an ideal starting point for understanding parallelization. Namely, the operation updates each element of vector `y` by scaling the corresponding element of vector `x` by a constant `a`, and adding it to the existing element of `y`. In more detail,
  - `n` is the number of elements in the vectors `x` and `y`,
  - `a` is the scalar value to multiply with vector `x`, 
  - `x`, `y` are the input vectors.

#### Exercise: sequential execution of linear combination of vectors

We will begin by executing a sequential version of `axpy` in C to understand the basic computation before moving to parallel implementations. The example code can be found in this repository: `hands-on/ex1`. The Slurm job script is prepared to take the size of the vector, `N`, as input parameter. Submit the script as follows.

```bash
sbatch submit-axpy.sh <N>
```

Example of output for `N` = 10000000. The kernel runs 100 times, so `y[0]` = 2 + 100 * 2 * 1 = 202. Your times will differ:

```bash
$ cat axpy-28085116.out
Length of the arrays: 10000000
y[0] = 202.000000
Time taken for axpy execution: 0.963870 seconds
```

> [!TIP]
> Try submitting multiple jobs with different `N` values. Compare the time to solution between different executions.

#### Exercise: parallel execution of linear combination of vectors

We will follow by executing a shared- and distributed-memory parallel version of `axpy` in C, OpenMP, and MPI to understand the basic Slurm job options in the Slurm script. The example code can be found in this repository: `hands-on/ex2`. The Slurm job script is prepared to take the (global) size of the vector, `N`, as input parameter. Submit the script as follows:

```bash
sbatch submit-axpy-hybrid.sh <N>
```
Example of output for `N` = 10000000 with the script's 128 tasks:

```bash
$ cat axpy-hybrid-28085117.out
Global length of the arrays: 10000000
Local length of the arrays: 78125
y[0] = 202.000000
Time taken for axpy execution: 0.009485 seconds
```

`Hyb-T-C` in the table below means `T` MPI tasks with `C` OpenMP threads each. Options on the `sbatch` command line override the `#SBATCH` lines, so `sbatch --ntasks=1 --cpus-per-task=16 submit-axpy-hybrid.sh <N>` runs `Hyb-1-16`.

> [!NOTE]
> With more than one OpenMP thread per task, pin the threads to cores so that the operating system does not move them during the run, which adds noise to the timings. Set these before `srun` in the job script, and bind the tasks as well:
> ```bash
> export OMP_PLACES=cores
> export OMP_PROC_BIND=close
> srun --cpu-bind=cores ./axpy-hybrid.out $N
> ```
> `OMP_PLACES=cores` gives each thread its own core, `OMP_PROC_BIND=close` keeps the threads of a task on neighbouring cores, and `--cpu-bind=cores` binds each task to the cores Slurm allocated to it.

After a job has finished, check how well it used the cores it asked for:

```bash
seff <jobid>
sacct -j <jobid> --format=JobID,AllocCPUS,Elapsed,TotalCPU,MaxRSS,State
```

`seff` reports the CPU efficiency: the CPU time used divided by the allocated cores times the elapsed time. The whole job counts, including compilation and initialization, so a short kernel gives a low figure even when it scales well. Compare the efficiency between configurations rather than reading one value on its own.

> [!TIP]
> Try submitting multiple jobs with different `ntasks` and `cpus-per-task`. Compare the time to solution between different executions. Complete the table by recording the time taken for the axpy operation across different vector sizes and parallel configurations.
> | Vector Size   | Sequential | Hyb-16-1 | Hyb-128-1 | Hyb-256-1 | Hyb-1-16 | Hyb-1-128 | Hyb-2-128 |
> |---------------|------------|----------|-----------|-----------|----------|-----------|-----------|
> | 1,000,000     |            |          |           |           |          |           |           |
> | 10,000,000    |            |          |           |           |          |           |           |
> | 100,000,000   |            |          |           |           |          |           |           |
> | 1,000,000,000 |            |          |           |           |          |           |           |
> | 10,000,000,000|            |          |           |           |          |           |           |
>
> The last row needs about 160 GB for `x` and `y`. Add `--exclusive` to the job script so that the job gets the memory of a full node.
>
> `Hyb-256-1` and `Hyb-2-128` need 256 cores, two `rome` nodes, while the script asks for one node. Add `--nodes=2` for those columns, for example `sbatch --nodes=2 --ntasks=256 --cpus-per-task=1 submit-axpy-hybrid.sh <N>` and `sbatch --nodes=2 --ntasks=2 --cpus-per-task=128 submit-axpy-hybrid.sh <N>`.

### Scalar product

The scalar product, or dot product, is a crucial operation in linear algebra and is widely used in applications like machine learning, graphics, and scientific simulations. It can be expressed as:

$$\text{result} = \sum_{i=0}^{n-1} x[i] \cdot y[i]$$,

where `x` and `y` are vectors of length `n`, and `result` is a scalar value that represents the sum of the products of corresponding elements of `x` and `y`.

The dot product kernel is a pointwise multiplication in which each element of vector `x` is multiplied by the corresponding element of vector `y`, *i.e.*, $$x[i] \cdot y[i]$$. This operation is **embarrassingly parallel** as each multiplication is independent of the others, making it highly suitable for parallelization. However, in contrast to axpy, after computing the individual products, the results must be summed together to produce the final scalar result. While this summation introduces dependencies between elements, it can still be performed in parallel using reduction techniques.

In shared-memory parallelism (*e.g.*, with OpenMP), each thread can compute a portion of the dot product and use a reduction clause to combine the partial results. In distributed-memory parallelism (*e.g.*, MPI), each process computes a local sum of its assigned portion of the vectors, followed by a global reduction to combine these local sums into the final result. Indeed, the reduction operation involves a global synchronization in which threads must reduce their local sums, and also distributed processes need to broadcast and gather their local solutions.

#### Exercise: sequential execution of dot product

We will start by executing a sequential version of the dot product in C to understand the basic operation before moving to parallel implementations. The example code can be found in the repository: `hands-on/ex3`. The Slurm job script is prepared to take the size of the vector, `N`, as an input parameter.

To submit the job, run the following command:

```bash
sbatch submit-dot.sh <N>
```

The vectors hold `sin(i)` and `0.5 * cos(i)`, and the result sums the dot product over 100 repetitions. Example of output for `N` = 10000000:

```bash
$ cat dot-28085119.out
Length of the arrays: 10000000
Dot product result: 12.3778
Time taken for dot product execution: 1.21664 seconds
```

> [!TIP]
> Try running the code with different values of `N` to see how the time to solution scales with the size of the vectors.

#### Exercise: parallel execution of dot product

After understanding the sequential version, we will proceed with executing parallel versions of the dot product using both OpenMP for shared-memory parallelism and MPI for distributed-memory parallelism. Each process or thread will compute a portion of the dot product independently, followed by a reduction step to sum the partial results.

The parallel implementations can be found in the repository: `hands-on/ex4`. The Slurm job script is prepared to accept the global size of the vector, `N`, as an input parameter.

To submit the parallel job, run the following command:

```bash
sbatch submit-dot-hybrid.sh <N>
```

Example of output for `N` = 10000000 with the script's 128 tasks. The result matches the sequential run to the printed digits; the order of the additions differs, so later digits can differ:

```bash
$ cat dot-hybrid-28085121.out
Global length of the arrays: 10000000
Local length of the arrays: 78125
Global dot product result: 12.3778
Time taken for dot product execution: 0.039711 seconds
```

> [!TIP]
> Experiment with different configurations of tasks and CPUs per task to understand how the execution time changes with varying levels of parallelism. Try submitting jobs with different `ntasks` and `cpus-per-task` values. Fill out the following table with the time taken for the dot product across different vector sizes and parallel configurations.
>| Vector Size   | Sequential | Hyb-16-1 | Hyb-128-1 | Hyb-256-1 | Hyb-1-16 | Hyb-1-128 | Hyb-2-128 |
>|---------------|------------|----------|-----------|-----------|----------|-----------|-----------|
>| 1,000,000     |            |          |           |           |          |           |           |
>| 10,000,000    |            |          |           |           |          |           |           |
>| 100,000,000   |            |          |           |           |          |           |           |
>| 1,000,000,000 |            |          |           |           |          |           |           |
>| 10,000,000,000|            |          |           |           |          |           |           |
>
> The last row needs about 160 GB for `x` and `y`. Add `--exclusive` to the job script so that the job gets the memory of a full node.
>
> `Hyb-256-1` and `Hyb-2-128` need 256 cores, two `rome` nodes, while the script asks for one node. Add `--nodes=2` for those columns, for example `sbatch --nodes=2 --ntasks=256 --cpus-per-task=1 submit-dot-hybrid.sh <N>` and `sbatch --nodes=2 --ntasks=2 --cpus-per-task=128 submit-dot-hybrid.sh <N>`.
