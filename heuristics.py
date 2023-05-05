
#basic analysis of file headers



import os
import time

def analyze_file(filepath):
    """Analyze the title header of a file."""
    try:
        with open(filepath, 'rb') as f:
            header = f.read(200).decode(errors='ignore')
            if 'MZ' in header:
                return 'Executable'
            elif '%PDF' in header:
                return 'PDF'
            else:
                return 'Document'
    except:
        return 'Error'

def scan_directory(directory_path, extensions):
    """Scan a directory for files with given extensions and analyze their title headers."""
    for filename in os.listdir(directory_path):
        filepath = os.path.join(directory_path, filename)
        if os.path.isfile(filepath) and os.path.splitext(filename)[1].lower() in extensions:
            print(f'{filename}: {analyze_file(filepath)}')

# Example usage
directory_path = '/path/to/directory'
extensions = ['.doc', '.docx', '.pdf', '.dll', '.exe']
scan_directory(directory_path, extensions)

#To use this script, you need to specify the directory path and the extensions you want to scan for. 
#The script will then print the name of each file with a matching extension and the type of file based on the header analysis.






















#basic analysis of behavior upon startup
#It loops through all the entries in the key 
#and checks if the file path is included in any of the startup entries

import winreg

def check_startup_entry(file_path):
    startup_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
    startup_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, startup_path, 0, winreg.KEY_READ)
    try:
        i = 0
        while True:
            name, value, _ = winreg.EnumValue(startup_key, i)
            if file_path.lower() in value.lower():
                return True
            i += 1
    except WindowsError:
        pass
    return False

#To use this script, you need to call the check_startup_entry() function and pass in the file path you want to check. 
#The function will return True if the file path is present in the Windows registry startup entries, and False otherwise.























#checks if a file is a copy of another, indicating a potential virus

import os
import hashlib

def is_duplicate(file_path, directory_path):
    """
    Check if a file is a duplicate of any file in a directory.
    
    :param file_path: The path of the file to check.
    :param directory_path: The path of the directory to check for duplicates.
    :return: True if the file is a duplicate, False otherwise.
    """
    with open(file_path, 'rb') as f:
        file_hash = hashlib.md5(f.read()).hexdigest()

    for dirpath, dirnames, filenames in os.walk(directory_path):
        for filename in filenames:
            if filename.lower().endswith(('.dll', '.exe', '.pdf')):
                current_path = os.path.join(dirpath, filename)
                with open(current_path, 'rb') as f:
                    current_hash = hashlib.md5(f.read()).hexdigest()
                if current_hash == file_hash:
                    return True
    return False

#To use this script, you need to call the is_duplicate() function and pass in the file path you want to check and the directory path you want to check for duplicates in. 
#The function will return True if the file is a duplicate of any file in the directory, and False otherwise.






















#basic heuristic analysis

import os

# Define a function to check if a file is suspicious based on its name
def is_suspicious_name(filename):
    if "malware" in filename.lower():
        return True
    elif "virus" in filename.lower():
        return True
    else:
        return False

# Define a function to check if a file is suspicious based on its size
def is_suspicious_size(filepath):
    if os.path.getsize(filepath) > 1000000: # 1MB
        return True
    else:
        return False

# Define a function to check if a file is suspicious based on its content
def is_suspicious_content(filepath):
    with open(filepath, 'rb') as f:
        content = f.read()
    if b'powershell' in content or b'cmd.exe' in content:
        return True
    else:
        return False

# Define a function to check if a file is suspicious based on its modification time
def is_suspicious_time(filepath):
    modification_time = os.path.getmtime(filepath)
    current_time = time.time()
    if current_time - modification_time < 86400: # 1 day
        return True
    else:
        return False

#To use this script, you can call the four functions with the file path you want to check as input, 
#and get a True or False value as output depending on whether the file is suspicious or not.

























import os
import hashlib

def heuristic_scan(path):
    suspicious_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Hash the file using MD5
                md5 = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
                
                # Check if the file has suspicious characteristics
                if len(file) > 20 and file.endswith(('.exe', '.dll', '.sys', '.bat', '.vbs')) \
                        and not file.startswith(('ms', 'spoolsv', 'lsass', 'services', 'svchost')):
                    suspicious_files.append((file_path, md5, "Suspicious filename"))
                
                # Check if the file has been modified recently
                stat = os.stat(file_path)
                if (time.time() - stat.st_mtime) < 86400:
                    suspicious_files.append((file_path, md5, "Recent modification"))
                
                # Check if the file has been compressed or encrypted
                with open(file_path, 'rb') as f:
                    data = f.read(1024)
                    if b'PK' in data or b'<?xml' in data:
                        suspicious_files.append((file_path, md5, "Compressed/encrypted data"))
                        
            except (PermissionError, IsADirectoryError):
                # Skip directories and files we can't read
                pass
            
    return suspicious_files






















#heuristic system

import os
import hashlib
import configparser
import logging
import threading

def load_config(config_file):
    """Load configuration settings from a file.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        configparser.ConfigParser: An object containing the configuration settings.
    """
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def is_suspicious(file, config):
    """Determine if a file is suspicious based on its filename and extension.

    Args:
        file (str): Name of the file.
        config (configparser.ConfigParser): Configuration settings.

    Returns:
        bool: True if the file is suspicious, False otherwise.
    """
    if len(file) > int(config['general']['max_filename_length']):
        return True
    if any(file.endswith(ext) for ext in config['extensions']):
        return True
    if any(file.startswith(prefix) for prefix in config['prefixes']):
        return True
    return False

def scan_file(file_path, config, logger):
    """Scan a file for suspicious characteristics.

    Args:
        file_path (str): Path to the file.
        config (configparser.ConfigParser): Configuration settings.
        logger (logging.Logger): Logger object for logging scan results.
    """
    try:
        with open(file_path, 'rb') as f:
            data = f.read(1024)
            if b'PK' in data or b'<?xml' in data:
                md5 = hashlib.md5(data).hexdigest()
                if md5 in config['hashes']:
                    logger.info(f'{file_path} has been seen before')
                else:
                    logger.warning(f'{file_path} is compressed/encrypted')
                    config['hashes'][md5] = file_path
    except (PermissionError, IsADirectoryError):
        logger.warning(f'Cannot read {file_path}')

def scan_directory(path, config):
    """Recursively scan a directory for suspicious files.

    Args:
        path (str): Path to the directory to scan.
        config (configparser.ConfigParser): Configuration settings.
    """
    logger = logging.getLogger()
    logger.info(f'Starting scan of {path}')
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if is_suspicious(file, config):
                logger.warning(f'{file_path} is suspicious')
            else:
                t = threading.Thread(target=scan_file, args=(file_path, config, logger))
                t.start()

def heuristic_scan(path, config_file, log_file):
    """Scan a directory for suspicious files using a heuristic approach.

    Args:
        path (str): Path to the directory to scan.
        config_file (str): Path to the configuration file.
        log_file (str): Path to the log file.
    """
    config = load_config(config_file)
    logging.basicConfig(filename=log_file, level=logging.INFO)
    scan_directory(path, config)
    config.write(open(config_file, 'w'))

if __name__ == '__main__':
    heuristic_scan('/path/to/scan', 'config.ini', 'scan.log')


#current updated version
#uses a configuration file to store the patterns to check for, and a database (in the form of a dictionary) to store the hashes of all files scanned. 
#It also uses a logger to log all actions taken by the script, and multi-threading to scan files concurrently. 
#Finally, it uses try-except blocks to handle any errors that may occur during the scanning process.
