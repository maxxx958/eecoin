import subprocess, atexit, time

# List of commands to run
commands = ["python test1.py", "python test2.py", "python test3.py", "python test4.py", "python test5.py"]

# Create a list to hold the subprocess.Popen objects
processes = []

# Start each command in a subprocess and append it to the list
for command in commands:
    process = subprocess.Popen(command, shell=True)
    processes.append(process)
    time.sleep(0.1)

# Function to terminate all subprocesses
def terminate_subprocesses():
    for process in processes:
        process.terminate()

# Register the function to be called on program exit
atexit.register(terminate_subprocesses)

# Wait for all subprocesses to finish
for process in processes:
    process.wait()

print("All commands have finished.")
