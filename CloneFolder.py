#!/usr/bin/env python3
import os
import hashlib
import shutil
import sys
from multiprocessing import Process, Manager


def sha256(absolute_path: str) -> str:
    """Calculates the sha256 hash of a file."""

    with open(absolute_path, "rb") as file:
        checksum = hashlib.sha256(file.read(), usedforsecurity=False).hexdigest()
    return checksum


def add_files_to_list(root_dir: str, file_list: dict) -> None:
    """Adds files and hashes to a list for copy."""

    for root, dirs, files in os.walk(os.path.expanduser(root_dir)):
        dirs[:] = [folder for folder in dirs if not folder.startswith(".")]
        files[:] = [file for file in files if not file.startswith(".")]
        for file in files:
            absolute_path = os.path.expanduser(f"{root}{os.path.sep}{file}")
            relative_path = absolute_path.replace(f"{os.path.expanduser(root_dir)}{os.sep}", "", 1)
            file_list[relative_path] = sha256(absolute_path)


# Entrypoint for the running of the application
if __name__ == '__main__':
    if len(sys.argv) == 3:
        manager = Manager()
        src = manager.dict({})
        dst = manager.dict({})

        process_list = []

        process = Process(target=add_files_to_list, args=(sys.argv[1], src))
        process_list.append(process)
        process.start()
        process = Process(target=add_files_to_list, args=(sys.argv[2], dst))
        process_list.append(process)
        process.start()

        for process in process_list:
            process.join()
            process.close()

        # Filters file lists to delete and copy lists.
        delete = [key for key in dst if key not in src.keys()]
        copy = [file for file in src if file not in dst.keys() or dst[file] != src[file]]

        # Deletes files in destination that no longer exist in the source folder.
        for file in delete:
            file_path = os.path.expanduser(f"""{sys.argv[2]}{os.path.sep}{file}""")
            if os.path.exists(file_path):
                os.remove(file_path)

        # Copies files that do not exist in the destination folder.
        for file in copy:
            src_path = os.path.expanduser(f"""{sys.argv[1]}{os.path.sep}{file}""")
            dst_path = os.path.expanduser(f"""{sys.argv[2]}{os.path.sep}{file}""")

            # Creates folder if it does not exist
            dst_folder = os.path.dirname(dst_path)
            if not os.path.exists(dst_folder):
                os.makedirs(dst_folder)

            # Copies file from source to destination folder.
            shutil.copy(src_path, dst_path)
    else:
        print("Both source and destination paths are required.")
