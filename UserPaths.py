import os


def get_user_home():
    return os.path.expanduser("~")


def get_idea_projects_dir():
    return f"{get_user_home()}/IdeaProjects"


def get_pycharm_projects_dir():
    return f"{get_user_home()}/PycharmProjects"


def is_folder_git_repo(folder):
    if os.path.exists(f"{folder}/.git"):
        return True
    else:
        return False


def get_projects_in_folder(folder):
    project_dirs = []
    for item in os.listdir(folder):
        path = f"{folder}/{item}"
        if not item.startswith(".") and is_folder_git_repo(path):
            project_dirs.append(path)

    return project_dirs


def get_projects():
    all_projects = []
    all_projects.extend(get_projects_in_folder(get_idea_projects_dir()))
    all_projects.extend(get_projects_in_folder(get_pycharm_projects_dir()))

    return all_projects

