import argparse
import logging
import os
import time
import hashlib
import shutil


def safe_copy(source, destination):
    """Copy a file with a permission error check."""
    try:
        shutil.copy2(source, destination)
    except PermissionError as e:
        logging.error(f"Permission error: {e}")


def safe_remove(file_path):
    """Remove a file with a permission error check."""
    try:
        os.remove(file_path)
    except PermissionError as e:
        logging.error(f"Permission error: {e}")


def remove_directory(directory):
    """Remove a directory and its contents recursively, chceking for permission errors"""
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        try:
            if os.path.isdir(item_path):
                remove_directory(item_path)
            else:
                os.remove(item_path)
        except Exception as e:
            # Log the permission error and continue with other items
            logging.error(f"Permission error while deleting {item_path}: {e}")

    try:
        os.rmdir(directory)
    except Exception as e:
        # Log the permission error when trying to remove the directory itself
        logging.error(
            f"Permission error while removing directory {directory}: {e}")


def sync(source, replica, interval, log_file):
    """Synchronize source folder to replica folder every interval seconds.

    Args:
        source (str): Source folder path.
        replica (str): Replica folder path.
        interval (int): Synchronization interval (in seconds).
        log_file (str): Log file path.
    """

    if not os.path.isdir(source):
        raise argparse.ArgumentTypeError(f"{source} is not a valid folder")

    if not os.path.isdir(replica):
        os.makedirs(replica)

    logging.info(
        f" Synchronization started with the following parameters:\n"
        f"Source: {source}\n"
        f"Replica: {replica}\n"
        f"Time interval: {interval}\n"
        f"Log file: {log_file}")

    while True:
        try:
            compare_folders(source, replica)
            time.sleep(interval)
        except KeyboardInterrupt:
            print("Synchronization stopped by KeyboardInterrupt")
            raise SystemExit


def compare_files_metadata(file1, file2):
    """Compare file sizes and modification times."""
    size1 = os.path.getsize(file1)
    size2 = os.path.getsize(file2)
    if size1 != size2:
        return False
    mtime1 = os.path.getmtime(file1)
    mtime2 = os.path.getmtime(file2)
    if mtime1 != mtime2:
        return False
    return True


def hash_file(filename):
    """Generate a hash for a file's content."""
    hasher = hashlib.md5()
    with open(filename, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def compare_files_content(file1, file2):
    """Compare the content of two files using hashes."""
    return hash_file(file1) == hash_file(file2)


def compare_files(file1, file2):
    """Compare two files by metadata and content."""
    if not compare_files_metadata(file1, file2):
        return False
    return compare_files_content(file1, file2)


def compare_folders(source_folder, replica_folder):
    """Compare source and replica folders and synchronize them."""
    source_files = os.listdir(source_folder)
    replica_files = os.listdir(replica_folder)

    # Synchronize source folder to replica folder
    for file in source_files:

        source_file = os.path.join(source_folder, file)
        replica_file = os.path.join(replica_folder, file)

        # File in source is a folder
        if os.path.isdir(source_file):

            # Folder in source does not exist in replica - create it
            if not os.path.isdir(replica_file):
                os.makedirs(replica_file)
                message = f" Creating folder {replica_file} - copy of {source_file}"
                logging.info(message)
                print(message)

            compare_folders(source_file, replica_file)

        # File in source is not a folder
        else:

            # If source file does not exist in replica, copy it
            if file not in replica_files:
                message = f" Creating file {replica_file} - copy of {source_file}"
                safe_copy(source_file, replica_file)
                logging.info(message)
                print(message)

            # If source file exists in replica but is different, copy update it
            elif not compare_files(source_file, replica_file):
                message = f" Updating file {replica_file} to match {source_file}"
                safe_copy(source_file, replica_file)
                logging.info(message)
                print(message)

            # If source file exists in replica and is same, do nothing

    # Remove files from replica folder that are not in source folder
    for file in replica_files:

        replica_file = os.path.join(replica_folder, file)

        # File in replica is a folder
        if os.path.isdir(replica_file):

            # Folder in replica does not exist in source - remove it
            if file not in source_files:
                remove_directory(replica_file)
                message = f" Removing folder {replica_file}"
                logging.info(message)
                print(message)

        else:

            # File in replica does not exist in source - remove it
            if file not in source_files:
                safe_remove(replica_file)
                message = f" Removing file {replica_file}"
                logging.info(message)
                print(message)


if __name__ == "__main__":

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="One-way folder synchronization")
    parser.add_argument("-s", "--source", type=str,
                        default="source", help="Source folder path")
    parser.add_argument("-r", "--replica", type=str,
                        default="replica", help="Replica folder path")
    parser.add_argument("-i", "--interval", type=int, default=60,
                        help="Synchronization interval (in seconds)")
    parser.add_argument("-l", "--log-file", type=str,
                        default="log.txt", help="Log file path")

    args = parser.parse_args()

    # Configurate file logging
    logging.basicConfig(filename=args.log_file, level=logging.INFO)

    # Call sync function
    sync(args.source, args.replica, args.interval, args.log_file)
