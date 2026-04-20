import os
import sys
import signal

def signal_handler(sig, frame):
    """Intercepts Ctrl+C so the shell doesn't crash."""
    print("\nCaught SIGINT. Type 'exit' to gracefully leave mash.")
    sys.stdout.write("mash> ")
    sys.stdout.flush()

def execute_command(args):
    """Handles execution and output redirection for the Child process."""
    
    if ">" in args:
        try:
            redirect_index = args.index(">")
            command_args = args[:redirect_index]
            file_name = args[redirect_index + 1]

            
            fd = os.open(file_name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
            os.dup2(fd, sys.stdout.fileno()) 
            os.close(fd)
            
            args = command_args
        except Exception as e:
            print(f"mash: parsing error - {e}")
            sys.exit(1)

    try:
        os.execvp(args[0], args)
    except FileNotFoundError:
        print(f"mash: command not found: {args[0]}")
        sys.exit(1) 
def main():
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        try:
            user_input = input("mash> ")
        except EOFError:
            print("\nExiting mash...")
            break
        
        if not user_input.strip():
            continue

        args = user_input.split()

        if args[0] == "exit":
            break
            
        if args[0] == "cd":
            try:
                target_dir = args[1] if len(args) > 1 else os.path.expanduser("~")
                os.chdir(target_dir)
            except FileNotFoundError:
                print(f"mash: cd: {args[1]}: No such file or directory")
            continue

        pid = os.fork()

        if pid < 0:
            print("mash: Critical OS Error - Fork failed.")
        elif pid == 0:
            execute_command(args)
        else:
            os.wait()

if __name__ == "__main__":
    main()
