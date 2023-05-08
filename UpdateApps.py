#!/usr/bin/env python3
import os
import platform

import decorators


def update_apps_debian():
    """Update app installed through apt on Debian."""

    # Runs a series of commands as sudo to install updates.
    if os.system("which nala") == 0:
        # If nala is installed use that for faster downloads.
        os.system("sudo nala upgrade -y")
    else:
        # Default command for installing updates.
        os.system("sudo apt update -y")
        os.system("sudo apt upgrade -y")

    # Updates OS, but does not upgrade to new release.
    os.system("sudo apt dist-upgrade -y")
    # Removes unused dependencies.
    os.system("sudo apt autoremove -y")
    # Cleans the package lists.
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

    # Windows app store updates.
    os.system("winget upgrade -h –all --accept-package-agreements --accept-source-agreements")
    # Windows updates.
    os.system("wuauclt /detectnow /updatenow")


@decorators.run_time
def update_apps():
    """Determines the OS and chooses how to update applications."""
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


# Entrypoint for the running of the application
if __name__ == '__main__':
    update_apps()
