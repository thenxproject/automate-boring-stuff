import os


def update_apps_debian():
    """Update app installed through apt on Debian."""
    os.system("sudo apt update")
    os.system("sudo apt upgrade")
    os.system("sudo apt dist-upgrade")
    os.system("sudo apt autoremove")
    os.system("sudo apt autoclean")


def update_apps_ubuntu():
    """Updates apps installed through snap and apt on Ubuntu."""
    update_apps_debian()
    os.system("sudo snap refresh")


def update_apps_mac_os_x():
    """Updates aps installed through Homebrew."""
    os.system("brew update")
    os.system("brew upgrade")


if __name__ == '__main__':
    if os.uname().sysname == "Linux":
        if "Ubuntu" in os.uname().version:
            update_apps_ubuntu()
        elif "Debian" in os.uname().version:
            update_apps_debian()
    elif os.uname().sysname == "Darwin":
        update_apps_mac_os_x()
