import os
import platform


def update_apps_debian():
    """Update app installed through apt on Debian."""

    # Runs a series of commands as sudo to install updates.
    os.system("sudo apt update -y")
    os.system("sudo apt upgrade -y")
    os.system("sudo apt dist-upgrade -y")
    os.system("sudo apt autoremove -y")
    os.system("sudo apt autoclean -y")


def update_apps_ubuntu():
    """Updates apps installed through snap and apt on Ubuntu."""

    # Installs apt package updates.
    update_apps_debian()
    # Installs snap updates.
    os.system("sudo snap refresh")


def update_apps_flatpak():
    """Updates Linux apps installed using Flatpak"""
    # Runs update for Flatpak command
    os.system("sudo flatpak update -y")


def update_apps_mac_os_x():
    """Updates aps installed through Homebrew, and system updates."""

    # Runs Homebrew apt updates.
    os.system("brew update")
    os.system("brew upgrade")
    # Updates system software
    os.system("softwareupdate -l -i -a")


def update_apps_windows():
    """Updates apps installed through Windows app store."""

    os.system("winget upgrade -h –all --accept-package-agreements --accept-source-agreements")
    os.system("wuauclt /detectnow /updatenow")


if __name__ == '__main__':
    # Detects OS and runs updates for matches.
    if platform.system() == "Linux":
        if "Ubuntu" in os.uname().version:
            update_apps_ubuntu()
        elif "Debian" in os.uname().version:
            update_apps_debian()

        # If flatpak is installed update flatpak apps
        if os.system("which flatpak") == 0:
            update_apps_flatpak()
    elif platform.system() == "Darwin":
        update_apps_mac_os_x()
    elif platform.system() == "Windows":
        update_apps_windows()
