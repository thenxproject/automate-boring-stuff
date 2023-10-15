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


def delete_files(delete_list: list, dst_dir: str) -> None:
    """Deletes files in destination that no longer exist in the source folder."""
    for file in delete_list:
        file_path = os.path.expanduser(f"""{dst_dir}{os.path.sep}{file}""")
        if os.path.exists(file_path):
            os.remove(file_path)


def copy_files(copy_list: list, src_dir: str, dst_dir: str) -> None:
    """Copies files that do not exist in the destination folder."""
    for file in copy_list:
        src_path = os.path.expanduser(f"""{src_dir}{os.path.sep}{file}""")
        dst_path = os.path.expanduser(f"""{dst_dir}{os.path.sep}{file}""")

        # Creates folder if it does not exist
        dst_folder = os.path.dirname(dst_path)
        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)

        # Copies file from source to destination folder.
        shutil.copy(src_path, dst_path)


def get_file_lists(src_dir: str, dst_dir: str) -> (dict, dict):
    """Gets a list of files in both the source and destination folders."""
    manager = Manager()
    src = manager.dict({})
    dst = manager.dict({})

    process_list = []

    process = Process(target=add_files_to_list, args=(src_dir, src))
    process_list.append(process)
    process.start()
    process = Process(target=add_files_to_list, args=(dst_dir, dst))
    process_list.append(process)
    process.start()

    for process in process_list:
        process.join()
        process.close()

    return src, dst


def get_list_to_delete(src_dict: dict, dst_dict: dict) -> list:
    """Filters the destination dictionary to a list of files that don't exist in the source list."""
    return [key for key in dst_dict if key not in src_dict.keys()]


def get_list_to_copy(src_dict: dict, dst_dict: dict) -> list:
    """Filters the source list to files that do not exist in the destination folder or files that were changed."""
    return [file for file in src_dict if file not in dst_dict.keys() or dst_dict[file] != src_dict[file]]


def copy_directory(src_dir: str, dst_dir: str) -> None:
    """
    Gets list of files for both the source and destination folders and makes the destination match the source folder.

    Hidden files on Linux or Mac are ignored.
    """
    src, dst = get_file_lists(src_dir, dst_dir)

    # Filters file lists to delete and copy lists.
    delete = get_list_to_delete(src, dst)
    copy = get_list_to_copy(src, dst)

    delete_files(delete, dst_dir)
    copy_files(copy, src_dir, dst_dir)


# Entrypoint for the running of the application
if __name__ == '__main__':
    if len(sys.argv) == 3:
        copy_directory(sys.argv[1], sys.argv[2])
    else:
        src_path = ""
        dst_path = ""

        while src_path == "" or dst_path == "":
            print("Both source and destination paths are required.")
            if src_path == "":
                src_path = input("What folder do you want to copy?\n")
            if dst_path == "":
                dst_path = input("Where do you want copy the files to?\n")

        copy_directory(src_path, dst_path)
