import os
import sys
import signal
import time
import random

def boot_sequence():
    """Theatrical boot sequence to impress non-technical viewers."""
    os.system('clear') # Clear the terminal for a clean start
    print("\033[1;36mMASH (Micro-Architecture Shell) v1.0.0\033[0m")
    print("\033[90mBooting POSIX-compliant kernel interface...\033[0m\n")
    
    for _ in range(15):
        addr = f"0x{random.randint(0x10000, 0xFFFFF):05X}"
        module = random.choice(["mem_alloc", "proc_sched", "io_ctrl", "vfs_mount", "ipc_pipe"])
        print(f"\033[90m[INIT] Loading kernel module {module} at {addr}... \033[1;32mOK\033[0m")
        time.sleep(0.04) # Artificial delay for visual effect
        
    print("\n\033[1;32m[OK] KERNEL BOOT SUCCESSFUL. HANDING CONTROL TO USER SPACE.\033[0m\n")
    time.sleep(0.5)

def display_sysinfo():
    """Reads live hardware data directly from the Linux virtual filesystem."""
    print("\n\033[1;36m=== MASH SYSTEM HARDWARE DASHBOARD ===\033[0m")
    try:
        # Reading raw Linux kernel files
        with open('/proc/cpuinfo', 'r') as f:
            cpu = [line.split(':')[1].strip() for line in f if 'model name' in line][0]
        with open('/proc/meminfo', 'r') as f:
            mem_lines = f.readlines()
            total_mem = mem_lines[0].split(':')[1].strip()
            free_mem = mem_lines[1].split(':')[1].strip()
        
        print(f"\033[1;33m[+] CPU Architecture:\033[0m {cpu}")
        print(f"\033[1;33m[+] Total Memory:\033[0m     {total_mem}")
        print(f"\033[1;33m[+] Free Memory:\033[0m      {free_mem}")
        print(f"\033[1;33m[+] OS Kernel:\033[0m        POSIX Cloud Container")
    except Exception as e:
        print(f"\033[1;31m[ERROR] Kernel access denied: {e}\033[0m")
    print("\033[1;36m======================================\033[0m\n")

def signal_handler(sig, frame):
    """Intercepts Ctrl+C."""
    print("\n\033[1;33m[KERNEL WARNING] Caught SIGINT. Main shell protected. Type 'exit' to terminate.\033[0m")
    sys.stdout.write("\033[1;32mmash>\033[0m ")
    sys.stdout.flush()

def execute_command(args):
    """Handles execution and output redirection."""
    if ">" in args:
        try:
            redirect_index = args.index(">")
            command_args = args[:redirect_index]
            file_name = args[redirect_index + 1]

            print(f"\033[36m[KERNEL] Intercepting data stream...\033[0m")
            time.sleep(0.3)
            print(f"\033[36m[KERNEL] Requesting File Descriptor for '{file_name}'...\033[0m")
            
            fd = os.open(file_name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
            os.dup2(fd, sys.stdout.fileno()) 
            os.close(fd)
            
            args = command_args 
        except Exception as e:
            print(f"\033[1;31mmash: parsing error - {e}\033[0m")
            sys.exit(1)

    print(f"\033[36m[KERNEL] Overwriting process memory with execvp()...\033[0m")
    time.sleep(0.2)
    try:
        os.execvp(args[0], args)
    except FileNotFoundError:
        print(f"\033[1;31mmash: command not found: {args[0]}\033[0m")
        sys.exit(1) 

def main():
    signal.signal(signal.SIGINT, signal_handler)
    boot_sequence()

    while True:
        try:
            user_input = input("\033[1;32mmash>\033[0m ")
        except EOFError:
            print("\n\033[1;31m[KERNEL] Terminating processes. Exiting mash...\033[0m")
            break
        
        if not user_input.strip():
            continue

        args = user_input.split()

        if args[0] == "exit":
            print("\033[1;31m[KERNEL] Terminating processes. Exiting mash...\033[0m")
            break
            
        if args[0] == "sysinfo":
            display_sysinfo()
            continue
            
        if args[0] == "cd":
            try:
                target_dir = args[1] if len(args) > 1 else os.path.expanduser("~")
                os.chdir(target_dir)
            except FileNotFoundError:
                print(f"\033[1;31mmash: cd: {args[1]}: No such file or directory\033[0m")
            continue

        print("\033[36m[KERNEL] Allocating PCB. Forking process...\033[0m")
        time.sleep(0.2)
        pid = os.fork()

        if pid < 0:
            print("\033[1;31mmash: Critical OS Error - Fork failed.\033[0m")
        elif pid == 0:
            execute_command(args)
        else:
            os.wait()

if __name__ == "__main__":
    main()