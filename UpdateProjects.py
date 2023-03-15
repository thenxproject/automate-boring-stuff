import os
from UserPaths import *
from multiprocessing import Process


def update_project_code(project_directory):
    os.system(f"git -C {project_directory} pull -q")


if __name__ == '__main__':
    projects = get_projects()
    for project in projects:
        process = Process(update_project_code(project))
        process.start()
        process.join()

