
#real time scanner/monitoring of directory



import os
import time

def scan_file(filename):
    # TODO: Replace with your virus scanning code
    # Return True if the file is infected, False otherwise
    return False

def monitor_directory(directory):
    # Get a list of all files in the directory
    files = {}
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        
        # Skip directories and hidden files
        if os.path.isdir(path) or filename.startswith('.'):
            continue
        
        # Store the last modified time for each file
        files[path] = os.path.getmtime(path)
    
    # Monitor the directory for changes every 5 seconds
    while True:
        time.sleep(5)
        
        for path in files:
            # Check if the file has been modified
            mtime = os.path.getmtime(path)
            if mtime != files[path]:
                files[path] = mtime
                
                # Scan the file for viruses
                if scan_file(path):
                    print(f"Virus detected in {path}!")
                else:
                    print(f"{path} is clean")

if __name__ == '__main__':
    import sys
    
    # Get the directory path from the command line argument
    directory = sys.argv[1]
    
    # Start monitoring the directory for changes
    monitor_directory(directory)







#the monitor_directory function takes a directory path as input, 
# and scans all files in the directory that have been modified since the last scan. 
# The function first reads the last modified time for each file in the directory, 
# and then enters an infinite loop that repeatedly checks for changes in the directory every 
# 5 seconds using the os.path.getmtime function. If a file has been modified since the last scan, 
# it is scanned for viruses using the scan_file function.






#The scan_file function is a placeholder that you will need to replace with your own virus scanning code. 
# This function should return True if the file is infected, and False otherwise.

#To run the program, simply pass the directory path as a command line argument:


# python my_scanner.py /path/to/directory
