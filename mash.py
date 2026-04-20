import os
import sys
import signal

def signal_handler(sig, frame):
    """Intercepts Ctrl+C so the shell doesn't crash."""
    print("\nCaught SIGINT. Type 'exit' to gracefully leave mash.")
    # Green prompt
    sys.stdout.write("\033[1;32mmash>\033[0m ")
    sys.stdout.flush()

def execute_command(args):
    """Handles execution and output redirection for the Child process."""
    # Check if user wants to redirect output (e.g., echo hello > file.txt)
    if ">" in args:
        try:
            redirect_index = args.index(">")
            command_args = args[:redirect_index]
            file_name = args[redirect_index + 1]

            # Open file, redirect standard output (stdout) to this file
            fd = os.open(file_name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
            os.dup2(fd, sys.stdout.fileno()) 
            os.close(fd)
            
            args = command_args # Strip the redirection part before execution
        except Exception as e:
            # Red error message
            print(f"\033[1;31mmash: parsing error - {e}\033[0m")
            sys.exit(1)

    # Overwrite the child process memory with the command
    try:
        os.execvp(args[0], args)
    except FileNotFoundError:
        # Red error message
        print(f"\033[1;31mmash: command not found: {args[0]}\033[0m")
        sys.exit(1) # Kill child if command is invalid

def main():
    # 1. Bind the signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # 2. The REPL Loop
    while True:
        try:
            # Green prompt
            user_input = input("\033[1;32mmash>\033[0m ")
        except EOFError:
            print("\nExiting mash...")
            break
        
        if not user_input.strip():
            continue

        args = user_input.split()

        # 3. Built-in Commands (Executed by Parent)
        if args[0] == "exit":
            break
            
        if args[0] == "cd":
            try:
                target_dir = args[1] if len(args) > 1 else os.path.expanduser("~")
                os.chdir(target_dir)
            except FileNotFoundError:
                # Red error message
                print(f"\033[1;31mmash: cd: {args[1]}: No such file or directory\033[0m")
            continue

        # 4. KERNEL INTERACTION: Fork and Exec
        pid = os.fork()

        if pid < 0:
            # Red error message
            print("\033[1;31mmash: Critical OS Error - Fork failed.\033[0m")
        elif pid == 0:
            # Child Process
            execute_command(args)
        else:
            # Parent Process
            os.wait()

if __name__ == "__main__":
    main()