# mash (Micro-Architecture Shell)

`mash` is a custom, POSIX-compliant command-line shell built to demonstrate direct kernel interaction and core Operating System process management. 

Unlike basic scripts that rely on high-level wrappers like `os.system()` or `subprocess`, `mash` manually manages the Process Control Block (PCB) and system file descriptors using raw kernel system calls.

## Core OS Concepts Implemented

1. **Process Creation & Cloning (`os.fork`)**
   The shell clones itself using `fork()`, creating a distinct Child process with an identical memory space to safely execute commands without risking the Parent shell's stability.

2. **Memory Replacement (`os.execvp`)**
   The Child process utilizes the `exec` family of system calls to overwrite its own memory space and execute the compiled binaries of user commands (e.g., `ls`, `pwd`, `cat`).

3. **Process Synchronization & Zombie Prevention (`os.wait`)**
   To prevent resource leaks and the creation of "zombie" processes, the Parent shell utilizes `wait()` to suspend its execution until the Child process formally terminates and returns its exit status to the kernel.

4. **File Descriptor Manipulation (I/O Redirection)**
   `mash` supports output redirection (`>`). It intercepts the command, opens a target file, and uses `os.dup2()` to reroute the standard output (stdout) file descriptor of the executing process directly into the file.

5. **Asynchronous Interrupt Handling (`signal`)**
   The shell overrides default OS interrupt behavior using the `signal` module. It catches `SIGINT` (Ctrl+C), ensuring that a runaway child process can be killed without terminating the parent shell itself.

## Usage
Built and tested in a Linux container environment.
