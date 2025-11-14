# Hands-on Snellius file systems

Open a terminal to access to Snellius via `ssh`.

```
$ ssh scur1448@snellius.surf.nl
Last login: Wed Nov 8 18:33:29 2023
[scur1448@int5 ~]$
```

On the login node, we will identify the different file systems:
1. `/home`
2. `/scratch-shared`
3. `/project`
4. `/archive`

## Home
The home file system, often denoted as `/home`, is the storage space dedicated to individual user accounts on Snellius. It serves as a personal workspace where users can store their important files, configuration files, scripts, and other data. **Each user on Snellius has their own dedicated home directory** within the `/home` file system, which is found at `/home/<username>`. The home directory is usually private and can only be accessed by the user who owns it. Other users typically don't have access to your home directory. Although you can change its access permissions, you should be very restrictive in using this capability.

Right after logging into Snellius via ssh, the prompt will be located at your home. You can check this via the path to the working directory command, `pwd`, as follows:

```
[scur1448@int5 ~]$ pwd
/home/scur1448
```

The home file system often has disk space quotas associated with it. Users are allocated a specific amount of storage space, and it's essential to be mindful of your usage to avoid exceeding your quota. The number of individual files, or inodes, is also limited. You can check your quota and current usage with the `myquota` command.

```
[scur1448@int5 ~]$ myquota
scur1448@home4|GiB:quota=200.00,limit=210.00,usage=0.0000%|Inodes:quota=1000000,limit=1200000,usage=0.0008%
```

The home directory is typically designed for **long-term storage of essential files** and data. It's not the ideal location for temporary or large files that you're actively working on. Files stored in the home directory are often **backed up regularly to prevent data loss** in case of hardware failures or accidental file deletion. SURF supplies a versioned **incremental backup service** for your home directory that is run overnight. Files that have been backed up are retained in the backup repository for **three weeks** after they have been deleted from the file system. We can restore files and/or directories when you accidentally remove them or overwrite them with the wrong contents.

While the home file system is suitable for long-term storage, it's not optimized for high-performance I/O or large data processing tasks. For such operations, other file systems like `/scratch` or `/project` may be more suitable.

## Scratch
The scratch file systems are intended as fast temporary storage that can be used while running a job and can be accessed by all users with a valid account on the system. A user's default scratch space capacity quota is 8 TiB, which is counted over all data usage of scratch-local and scratch-shared of the user. Again, you can check your quota and current usage with the `myquota` command.

```
[scur1448@int5 ~]$ myquota
scur1448@wstor_scratch1|TiB:quota=8.00,limit=10.00,usage=0.0038%|Inodes:quota=3000000,limit=4000000,usage=0.0014%
```

Snellius offers three distinct scratch file systems to meet various storage and performance requirements.
* Shared. 
* Local.
* Node.

### Scratch-shared
The scratch-shared file system, denoted as `/scratch-shared`, is a shared workspace accessible from all compute nodes on Snellius. It is designed for temporary and high-performance storage, making it suitable for parallel and distributed computing tasks.

You can create your own directory using your `<username>`, or any other filename.

```
[scur1448@int6 ~]$ mkdir /scratch-shared/scur1448
[scur1448@int6 ~]$ touch /scratch-shared/scur1448/testfile-scratch-shared.foo
[scur1448@int6 ~]$ ls /scratch-shared/scur1448/
testfile-scratch-shared.foo
```

### Scratch-local
The scratch-local file system is dedicated to individual compute nodes on Snellius. While it sits on the same GPFS infrastructure as the scratch-shared system, it is uniquely configured for each compute node upon the initiation of a job. You can access it via the environment variable `$TMPDIR`. For example, follow the steps below to create a test file on login node `int6` (if you did not land on `int6`, you can either switch or adapt the next steps to your specific login node).

```
[scur1448@int6 ~]$ touch $TMPDIR/testfile-local-int6.foo
[scur1448@int6 ~]$ echo "a file in int6" > $TMPDIR/testfile-local-int6.foo
[scur1448@int6 ~]$ cd $TMPDIR
[scur1448@int6 scur1448]$ ll
total 1
-rw-r----- 1 scur1448 scur1448 15 Nov  8 23:33 testfile-local-int6.foo
[scur1448@int6 scur1448]$ cat testfile-local-int6.foo 
a file in int6
```

Now, let's switch to the login node `int5` by using `ssh int5`. First, verify whether the file in the scratch-shared system is still present.

```
[scur1448@int6 scur1448]$ ssh int5
[scur1448@int5 ~]$ ll /scratch-shared/scur1448/
total 0
-rw-r----- 1 scur1448 scur1448 0 Nov  8 23:13 testfile-scratch-shared.foo
```

Next, confirm that the file in the scratch-local system is absent.

```
[scur1448@int5 ~]$ ls $TMPDIR
[scur1448@int5 ~]$ 
```

Next, use the script below to launch a job that lists the contents of `$TMPDIR`, creates a file, and prints the path and real path to `$TMPDIR`.

```
#!/bin/bash
#SBATCH -J files
#SBATCH -t 5
#SBATCH -p thin_course

ls -l $TMPDIR
touch "$TMPDIR/testfile.foo"
hostname > "$TMPDIR/testfile.foo"
ls -l $TMPDIR
echo $TMPDIR
realpath $TMPDIR
```

We executed the job twice and provided the outputs below. Despite both jobs being allocated to the same node, it's shown that the scratch-local directory is not only node-specific but also job-specific.

```
[scur1448@int5 ~]$ cat slurm-4401218.out
tcn386.local.snellius.surf.nl
total 0
total 0
-rw-r----- 1 scur1448 scur1448 0 Nov  9 00:25 testfile-.foo
/scratch-local/scur1448.4401218
/gpfs/scratch1/nodespecific/tcn386/scur1448.4401218
```

```
[scur1448@int5 ~]$ cat slurm-4401219.out
tcn386.local.snellius.surf.nl
total 0
total 0
-rw-r----- 1 scur1448 scur1448 0 Nov  9 00:25 testfile-.foo
/scratch-local/scur1448.4401219
/gpfs/scratch1/nodespecific/tcn386/scur1448.4401219
```

In this configuration, you might occasionally lose track of files generated by your jobs in the scratch-node file system, potentially leading to the consumption of your allocated quota. To address this, you can use the following commands to locate all your files on the scratch file system:

```
[scur1448@int5 ~]$ ls -ld /gpfs/scratch1/nodespecific/*/scur1448.*
drwxr-xr-x 2 scur1448 scur1448 4096 Nov  9 00:19 /gpfs/scratch1/nodespecific/tcn386/scur1448.4401213
drwxr-xr-x 2 scur1448 scur1448 4096 Nov  9 00:25 /gpfs/scratch1/nodespecific/tcn386/scur1448.4401218
drwxr-xr-x 2 scur1448 scur1448 4096 Nov  9 00:25 /gpfs/scratch1/nodespecific/tcn386/scur1448.4401219
```

### Scratch-node
The scratch-node behavior is technically similar to scratch-local. For each assigned node, a user-specific partition is created and mounted under `/scratch-node`. The environment variable `$TMPDIR` points to the user-specific directory within `/scratch-node`, which should be used within your job. However, there are some differences that are worth noting:
1. Scratch-node operates on NVMe-based storage and is physically located on the node itself.
2. When a user's job is completed, their respective file system mounted under `/scratch-node` will be automatically removed. Therefore, it's essential to copy your data from `$TMPDIR` to a more permanent location at the end of your job script.
3. There are no quotas imposed on `/scratch-node`, and no backup policy is in place. Users should exercise caution in data management.

Please be aware that when requesting a shared node, you will only receive a portion of the local NVMe disk, such as 25%, 50%, or 75%, depending on the requested job resources.

Scratch-node is available on a subset of Snellius nodes. To secure a node with the scratch-node file system, you may use the `--constraint=scratch-node` flag in your job configuration.

#### Exercise
Modify the script above to launch a job that creates a file on scratch-node and displays the file's real path.

```
#!/bin/bash
#SBATCH -J scratch-node-test
#SBATCH -t 5
#SBATCH -p thin_course
#SBATCH --constraint=scratch-node

touch "$TMPDIR/testfile-scratch-node.foo"
echo "This is a file on scratch-node" > "$TMPDIR/testfile-scratch-node.foo"
realpath "$TMPDIR/testfile-scratch-node.foo"
```

#### Advanced exercise: Creating large file sets and evaluating transfers

##### Objective
- Learn how to generate large numbers of files with random data.
- Compare the efficiency of transferring these files as individual files versus transferring them as an archive between different file systems (e.g., home and scratch).

##### Set-up guide

1. **Create a directory for the test**:
   - Create a directory to store the random files: 
     ```bash
     mkdir ~/file_transfer_test
     cd ~/file_transfer_test
     ```

2. **Generate random files**:
   - Use a `for` loop to create 1000 files, each with random data.
   - You can use the `dd` command or `head` with `/dev/urandom` to generate files with random data. Here's an example of creating 1000 files with 1 MB of random data each:
     ```bash
     for i in {1..1000}; do
         head -c 1M </dev/urandom > file_$i.bin
     done
     ```
   - **Explain**: This loop generates 1000 binary files (`file_1.bin`, `file_2.bin`, ..., `file_1000.bin`), each with 1 MB of random data.

3. **Check the size of the directory**:
   - After creating the files, check the total size of the directory:
     ```bash
     du -sh ~/file_transfer_test
     ```
   This gives you an idea of how much data will be transferred.

##### Moving the files between file systems

Now, we'll move these files between different file systems (e.g., from **home** to **scratch** or **project**) in two different ways: 
1. Moving the individual files.
2. Moving a compressed archive of the files.

1. **Transfer as individual files**:
   - First, move the files individually:
     ```bash
     cp -r ~/file_transfer_test /path/to/scratch/
     ```
   - Use `time` to measure how long the transfer takes:
     ```bash
     time cp -r ~/file_transfer_test /path/to/scratch/
     ```

2. **Transfer as an archive**:
   - Archive and compress the directory using `tar` and `gzip`:
     ```bash
     tar -czf file_transfer_test.tar.gz ~/file_transfer_test
     ```
   - Measure the size of the compressed archive:
     ```bash
     du -sh file_transfer_test.tar.gz
     ```
   - Now, transfer the archive to the **scratch** directory:
     ```bash
     time cp file_transfer_test.tar.gz /path/to/scratch/
     ```

3. **Extract the archive in the scratch directory**:
   - Once the transfer is complete, extract the archive in the scratch directory to restore the files:
     ```bash
     cd /path/to/scratch/
     tar -xzf file_transfer_test.tar.gz
     ```

##### Evaluate the performance

1. **Compare transfer times**:
   - Review the `time` command outputs from both transfers (individual files vs. archive).
   - Discuss how much time it took to transfer the files as individual files versus as a compressed archive.

2. **Compare data size**:
   - Check the total size of the original directory and the compressed archive. Highlight the difference in storage requirements and transfer speeds based on compression.

3. **Discuss trade-offs**:
   - **When to use individual file transfers**: If you're working with a small number of files or if they will be used directly without further processing.
   - **When to use archived file transfers**: Compressing many small files reduces both disk space usage and transfer time due to fewer I/O operations.

4. **Advanced considerations**:
   - Discuss how these operations scale using larger directories or more complex file systems.
   - Introduce the concept of **I/O bottlenecks** in HPC and why proper file management is crucial when working with large data sets.

##### Clean-up

- After the hands-on session, guide the participants to clean up the directories and files to free up space on the system:
  ```bash
  rm -r ~/file_transfer_test
  rm ~/file_transfer_test.tar.gz
  rm -r /path/to/scratch/file_transfer_test
  rm /path/to/scratch/file_transfer_test.tar.gz
