# Hands-on fundamentals of high-performance computing

This hands-on session introduces **basic usage of the Snellius supercomputer at SURF**. You will learn how to:
* connect to Snellius,
* understand the Linux environment,
* navigate the file system,
* compile a simple parallel program,
* submit and monitor jobs using the SLURM workload manager.

---

## 1. Accessing Snellius and exploring the Linux environment

**Objective:** Connect to Snellius and retrieve basic system and user information. Verify your access and become familiar with the Linux environment. Record this information in a text file called `<username>.dat` located in your home directory.
 
| #  | Question                                      | Command                               | Environment variable |
|----|-----------------------------------------------|---------------------------------------|----------------------|
| 1  | What is your username?                        | `whoami`                              | `echo $USER`         |
| 2  | What is your current working directory?       | `pwd`                                 | `echo $PWD`          |
| 3  | What is your home directory?                  | _none_                                | `echo $HOME`         |
| 4  | Which login node are you on?                  | `hostname`                            | `echo $HOSTNAME`     |
| 5  | When did you last log in to Snellius?         | `last -n 1 $USER`                     | _none_               |
| 6  | How much storage quota do you have?           | `myquota`                             | _none_               |
| 7  | What is your compute budget and usage?        | `accinfo`                             | _none_               |

### 1.1. Connecting to Snellius

To access Snellius, connect via SSH ([troubleshooting guide](https://servicedesk.surf.nl/wiki/spaces/WIKI/pages/30660265/Snellius+FAQ#SnelliusFAQ-TroublewithconnectingtoSnellius)):

```
$ ssh <username>@snellius.surf.nl
```

When you log in, you are placed on a login node (for example int4 or int6), and **interact with the system through a shell**. The shell interprets your **commands**, executes **programs**, and provides access to your **environment** variables: named values that configure your session.

### 1.2. Creating your first file

> 🖥️ **Editing files in the Shell**
>
> There are multiple ways to edit files in a Shell. Two common options are:
> * Shell editors like [`vim`](https://www.vim.org) or [`nano`](https://www.nano-editor.org), for manual editing.
> * Output [redirection](https://www.gnu.org/software/bash/manual/html_node/Redirections.html) using `>` for overwriting or `>>` for appending.

After connecting to Snellius, your Shell will be located at your home directory: `/home/<username>`. Let’s create a new text file where you will store all your answers for this section.

```
[<username>@int6 ~]$ touch <username>.dat
[<username>@int6 ~]$ ls
<username>.dat
```

Now every time you obtain a piece of information, append it to your file using, for instance, the >> redirection operator:

```
[<username>@int6 ~]$ echo "Username: $USER" >> <username>.dat
[<username>@int6 ~]$ cat <username>.dat
Username: <username>
```

### 1.3. Understanding the Linux environment

> 📦 **Why do environment variables exist?**
> 
> You’re working on a shared system (Snellius), with thousands of users and hundreds of programs. Every time you run a program, it needs to know who you are, where your files are, what software you use, what language or region settings you prefer.
> 
> Typing these details every single time would be painful and error-prone. That’s where environment variables come in: they act as a set of predefined, user-specific values that make the shell context-aware and help programs behave correctly without manual input every time.
> 
> Let’s say John Doe wants to create a folder for logs and save a file there. John could hardcode:
> ```
> [<username>@int6 ~]$ mkdir /home/johnd/logs
> [<username>@int6 ~]$ echo "My log entry" > /home/johnd/logs/run.log
> ```
> 
> But this will fail for everyone else, because `/home/johnd/` only works for John. Instead, John could use the environment variable `$HOME`, which automatically expands to the correct home directory for any user:
> ```
> [<username>@int6 ~]$ mkdir -p $HOME/logs
> [<username>@int6 ~]$ echo "My log entry" > $HOME/logs/run.log
> ```
> 
> ✅ Now the script works for everyone, not just John. This is essential in shared environments, job scripts, and automation.

#### 1.3.1. Exploring the Linux environment

**Environment variables determine how the shell behaves**. They tell programs where to look for files, which compiler to use, what language to display messages in, and more. You can inspect the environment defined in your session using the env command:
```
[<username>@int6 ~]$ env
SHELL=/bin/bash
USER=<username>
HOME=/home/<username>
PATH=/home/<username>/.local/bin:/usr/local/bin:/usr/bin:/bin
...
```

The method above is very verbose. Instead, let’s record a few key ones in the file: 
```
[<username>@int6 ~]$ echo "Current directory: $PWD" >> <username>.dat
[<username>@int6 ~]$ echo "Home directory: $HOME" >> <username>.dat
[<username>@int6 ~]$ echo "Login node: $HOSTNAME" >> <username>.dat
[<username>@int6 ~]$ cat <username>.dat
Username: <username>.dat
Current directory: /home/<username>/
Home directory: /home/<username>/
Login node: int6.local.snellius.surf.nl
```

#### 1.3.2. Modifying the Linux environment

**Environment variables only exist within your current shell session**. When you log out or launch a separate process, a new environment is created and does not automatically inherit the variables you changed manually—unless you explicitly export or pass them. Let’s explore this through two small experiments.

Create a variable in your current session and print its value. Then exit the session, log in again, and print the value again.
```
[<username>@int6 ~]$ NEWVAR="Hello_123"
[<username>@int6 ~]$ echo $NEWVAR
Hello_123
[<username>@int6 ~]$ exit
logout
$ ssh <username>@snellius.surf.nl
[<username>@int6 ~]$ echo $NEWVAR
```

The output is empty. **The variable `NEWVAR` is gone because the environment was destroyed when the session ended**. If you want a variable to appear automatically in every new login, you must define it in one of your shell startup files (for example `~/.bash_profile` or `~/.bashrc`).

#### 1.4. Retrieving system and accounting information
While the environment provides user-specific information or shell configuration, other types of information are obtained from **extensive system logs and accounting databases**. These logs are maintained by the operating system or by Snellius-specific services. System logs may include data such as your last login time or active sessions, while accounting logs store resource usage, storage quotas, or compute budgets.

On Snellius, accounting information is collected and exposed through dedicated commands implemented by the system administrators. These tools retrieve data directly from the system’s internal accounting infrastructure and present it in a user-friendly format.

Finally, use the following commands to collect details about your quota and compute budgets, and include them to your log file:

```
[<username>@int6 ~]$ last -n -R 1 $USER
<username>  pts/5        Tue Oct 28 20:12   still logged in
[<username>@int6 ~]$ myquota
<username>@home6
  Quota                Limit                Usage               
  200.00 GiB           210.00 GiB           65.7232%        GiB        [===================           ]
  1000000 Inodes       1200000 Inodes       70.8850%        Inodes     [=====================         ]

[<username>@int6 ~]$ accinfo
```

Now you have a single file summarising your system and user environment on Snellius — a simple but practical way to document what’s running under the hood.
