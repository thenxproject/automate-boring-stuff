# automate-boring-stuff
Python tools to automate boring stuff. This is the start of a collection of tools to automate boring tasks

## Tools available
### UpdateProjects
#### Description 
This command is intended to update Idea IntelliJ and PyCharm git repositories. It expects the projects to be in the PyCharmProjects and IdeaProjects directories withing the users home directory because that is the default. It uses parallel processing to update multiple repositories at the same time.
#### Example usage
`python3 UpdateProjects.py`

### UpdateApps
#### Description
This command will update installed apps through various package managers. OS is detected and updates run now special steps needed.
Current support is for the following:
- Homebrew - MacOS X
- Apt - Debian & Ubuntu
- Snap - Ubuntu
- DNF - Fedora
- APX - Vanilla OS
#### Example usage
`python3 UpdateApps.py`

### CloneFolder
#### Description
This command will clone a folder and all its files. This is useful when creating a backup of a large number of files.

If the destination folder exists only modified files will be copied.

If the destination folder has a file that is not in source directory it will be deleted.
#### Example usages
`python3 CloneFolder.py ~/Documents ~/Documents_backup`
`python3 CloneFolder.py ~/Documents "~/Documents Backup"`
`python3 CloneFolder.py`
