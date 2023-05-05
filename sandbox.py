import subprocess
import logging
import time

# Path to the suspicious file
file_path = "C:/path/to/suspicious_file.exe"

# Define the command to execute the file in a sandbox using Firejail with process isolation and a timeout of 10 seconds
sandbox_command = ["firejail", "--private", "--net=none", "--timeout=10", "--", file_path]

# Execute the command in a subprocess
p = subprocess.Popen(sandbox_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Wait for the process to complete or timeout
timeout = 10  # Timeout in seconds
start_time = time.monotonic()
while p.poll() is None and time.monotonic() - start_time < timeout:
    time.sleep(1)

# Check if the process timed out
if p.poll() is None:
    logging.warning("Sandboxed process timed out")

# Check if the process exited with an error code
if p.returncode != 0:
    logging.warning(f"Sandboxed process exited with error code {p.returncode}")

# Print the results
stdout, stderr = p.communicate()
print(f"stdout: {stdout.decode()}")
print(f"stderr: {stderr.decode()}")

# Log the results
logging.info(f"Sandboxed process stdout: {stdout.decode()}")
logging.info(f"Sandboxed process stderr: {stderr.decode()}")








#This code assumes that you have Firejail installed on your system and that it is in your system's PATH











#you can use the execute_in_sandbox function by passing the path of the suspicious file as an argument. heres an example usage:

# Example usage
suspicious_file_path = "C:/path/to/suspicious_file.exe"
sandbox_tool = "Sandboxie"

# Execute the file in a sandbox
stdout, stderr = execute_in_sandbox(suspicious_file_path, sandbox_tool)

# Print the results
print(f"stdout: {stdout}")
print(f"stderr: {stderr}")
