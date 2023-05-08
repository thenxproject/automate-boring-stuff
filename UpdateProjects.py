#!/usr/bin/env python3
from UserPaths import *
from multiprocessing import Process


def update_project_code(project_directory):
    """Runs the git command to silently pull the git repository in the specified directory."""
    os.system(f"git -C {project_directory} pull -q")


if __name__ == '__main__':
    projects = get_git_projects()
    for project in projects:
        process = Process(update_project_code(project))
        process.start()
        process.join()

