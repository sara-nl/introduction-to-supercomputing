# Introduction to Supercomputing

### Welcome

Welcome to the **Introduction to Supercomputing** course.

This training provides a practical overview of how modern supercomputers operate, how to run applications efficiently, and how to use the Snellius system at SURF. The aim is to give you the essential concepts and hands-on experience needed to work productively on HPC systems for your research.

The course is typically divided into three four-hour sessions, each focusing on a different aspect of supercomputing. Throughout the course you will work with hands-on exercises designed to reinforce the concepts and help you build confidence using HPC systems in practice.

We hope you find the training useful, and we welcome any feedback to help us improve future editions.

## Agenda

### **Part I — Fundamentals of HPC**
**Modules:**
- Fundamentals of HPC

### **Part II — Working with the Snellius environment**
**Modules:**  
- Snellius file systems
- QCG PilotJob

### **Part III — Performance and hybrid jobs**
**Modules:**  
- Performance analysis
- Slurm hybrid jobs

> [!NOTE]
> The course uses Snellius, but the hands-on sessions also run on a small Slurm cluster built from SURF Research Cloud (SRC) workspaces with the European Environment for Scientific Software Installations (EESSI) 2025.06. Notes like this one in each module list the differences. The cluster accepts the Snellius job scripts as they are: `module load 2025` loads EESSI 2025.06, the partition `rome` exists, `$TMPDIR` points at node-local scratch, and `sacct` and `seff` work. The performance analysis slides use `--constraint=hwperf`, the Energy Aware Runtime and AMD uProf, which exist only on Snellius; on the SRC cluster, PAPI and `perf` read the hardware counters instead. Your trainer gives you the cluster's address and an enrolment link that sets your password and SSH key.
