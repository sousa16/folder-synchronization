

# folder-synchronization

This Python script offers robust folder synchronization capabilities with a focus on maintaining an exact replica in one direction. It incorporates several essential features to ensure reliable synchronization.

## Table of Contents

 - Key Features
 - Functionalities
 - Prerequisites
 - Usage
 - Example

## Key Features

-   **Exact Folder Replication:** Ensures that the replica folder mirrors the source folder's structure and content precisely.
    
-   **File Modification Tracking:** Utilizes file metadata such as modification times to determine if files need to be updated or copied.
    
-   **Checksum Verification:** Compares file content using MD5 hashing to ensure that files with identical content are not unnecessarily copied.
    
-   **Periodic Synchronization:** Allows users to specify a time interval for automatic synchronization between the source and replica folders.
    
-   **Error Handling:** Handles permission errors gracefully when copying, removing files, or deleting directories.

## Functionalities

-   **Safe Copy and Removal:** Uses `shutil.copy2` for secure file copying and includes error handling for `PermissionError` during file operations.
    
-   **Recursive Directory Removal:** Ensures complete removal of directories and their contents, handling permission errors encountered during directory removal.
    
-   **Logging:** Logs synchronization activities and errors to a specified log file (`log.txt` by default) for monitoring and troubleshooting.
    
-   **Command-Line Interface:** Provides a command-line interface using `argparse` for easy configuration of source folder, replica folder, synchronization interval, and log file path.

## Prerequisites

 - Python 3.x
 - Standard libraries: os, time, argparse, logging, hashlib, shutil

## Usage

`python sync.py -s SOURCE_FOLDER -r REPLICA_FOLDER -i TIME_INTERVAL -l LOG_FILE`

`-s, --source`: Source folder path

`-r, --replica`: Replica folder path

`-i, --interval`: Synchronization interval (in seconds)

`-l, --log-file`: Log file path

## Example

`python sync.py -s /path/to/source -r /path/to/replica -i 120 -l /path/to/log` 
