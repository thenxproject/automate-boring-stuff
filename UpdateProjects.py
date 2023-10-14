#!/usr/bin/env python3
from UserPaths import *
from multiprocessing import Process


def update_project_code(project_directory):
    """Runs the git command to silently pull the git repository in the specified directory."""
    os.system(f"git -C {project_directory} pull -q")


if __name__ == '__main__':
    projects = get_git_projects()
    process_list = []
    for project in projects:
        process = Process(target=update_project_code, args=(project,))
        process_list.append(process)
        process.start()

    for process in process_list:
        process.join()
