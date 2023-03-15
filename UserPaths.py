import os


def get_user_home():
    """Gets the absolute path for the users home directory."""
    return os.path.expanduser("~")


def get_idea_projects_dir():
    """Gets the absolute path to the default IdeaProjects folder for IntelliJ projects."""
    return f"{get_user_home()}/IdeaProjects"


def get_pycharm_projects_dir():
    """Gets the absolute path to the default PycharmProjects folder for PyCharm projects."""
    return f"{get_user_home()}/PycharmProjects"


def is_folder_git_repo(folder):
    """Determines if the specified folder is a git repository."""
    if os.path.exists(f"{folder}/.git"):
        return True
    else:
        return False


def get_git_repo_projects_in_folder(folder):
    """Returns a list of absolute paths to folders in specified folder that are not hidden and are git repositories."""
    project_dirs = []
    # Loops through the items in the specified folder.
    for item in os.listdir(folder):
        # Assembles the path to each item in the folder.
        path = f"{folder}/{item}"
        """
        Determines if it is supposed to be a hidden folder "." on a Mac or Linux machine and if it is a git repository.
        If it meets both criteria it adds the absolute path to a list of paths for a project. If not it gets excluded.
        """
        if not item.startswith(".") and is_folder_git_repo(path):
            # Adds absolute path to the list
            project_dirs.append(path)

    return project_dirs


def get_git_projects():
    """Returns a list of absolute paths for all IntelliJ and PyCharm projects that are git repositories."""
    all_projects = []
    # Adds all IntelliJ projects to the final list of projects that are git repositories
    all_projects.extend(get_git_repo_projects_in_folder(get_idea_projects_dir()))
    # Adds all PyCharm projects to the final list of projects that are git repositories
    all_projects.extend(get_git_repo_projects_in_folder(get_pycharm_projects_dir()))

    return all_projects

