import os


def get_user_home() -> str:
    """Gets the absolute path for the users home directory."""
    return os.path.expanduser("~")


def get_idea_projects_dir() -> str:
    """Gets the absolute path to the default IdeaProjects folder for IntelliJ projects."""
    return f"{get_user_home()}/IdeaProjects"


def get_pycharm_projects_dir() -> str:
    """Gets the absolute path to the default PycharmProjects folder for PyCharm projects."""
    return f"{get_user_home()}/PycharmProjects"


def is_folder_git_repo(folder: str) -> bool:
    """Determines if the specified folder is a git repository."""
    if os.path.exists(f"{folder}/.git"):
        return True
    else:
        return False


def get_git_repo_projects_in_folder(folder: str) -> list:
    """Returns a list of absolute paths to folders in specified folder that are not hidden and are git repositories."""

    # If path does not exist return empty list.\
    if os.path.exists(folder):
        """
        Uses list comprehension to create a list that contains the absolute paths for directories that are not hidden
        and that are git repositories.
        """
        return [f"{folder}/{item}"
                for item in os.listdir(folder)
                if not item.startswith(".") and is_folder_git_repo(f"{folder}/{item}")]
    else:
        return []


def get_git_projects() -> list:
    """Returns a list of absolute paths for all IntelliJ and PyCharm projects that are git repositories."""
    all_projects = []
    # Adds all IntelliJ projects to the final list of projects that are git repositories
    all_projects.extend(get_git_repo_projects_in_folder(get_idea_projects_dir()))
    # Adds all PyCharm projects to the final list of projects that are git repositories
    all_projects.extend(get_git_repo_projects_in_folder(get_pycharm_projects_dir()))

    return all_projects
