#!/usr/bin/env python3
import shutil
import subprocess
import platform
from decorators import run_time


def use_sudo() -> str:
    """Checks if sudo is installed and returns the sudo command if it is."""
    if shutil.which("sudo") is not None:
        return "sudo"

    return ""


def update_apps_apt():
    """Update app installed through apt."""

    # Runs a series of commands as sudo to install updates.
    if shutil.which("nala") is not None:
        # If nala is installed, use that for faster downloads.
        subprocess.run(f"{use_sudo()} nala upgrade -y", shell=True)
        # Removes unused dependencies.
        subprocess.run(f"{use_sudo()} nala autoremove -y", shell=True)
        subprocess.run(f"{use_sudo()} nala autopurge -y", shell=True)
    elif shutil.which("apt") is not None:
        # Default command for installing updates.
        subprocess.run(f"{use_sudo()} apt update -y", shell=True)
        subprocess.run(f"{use_sudo()} apt upgrade -y", shell=True)

        # Updates OS but does not upgrade to a new release
        subprocess.run(f"{use_sudo()} apt dist-upgrade -y", shell=True)
        # Removes unused dependencies.
        subprocess.run(f"{use_sudo()} apt autoremove -y", shell=True)
        # Cleans the package lists.
        subprocess.run(f"{use_sudo()} apt autoclean -y", shell=True)


def update_apps_vso():
    """Updates Vanilla OS using VSO"""

    # If VSO command exists, rus commands to update apps
    if shutil.which("vso") is not None:
        # Updates system
        subprocess.run(f"{use_sudo()} vso update-check", shell=True)
        subprocess.run(f"{use_sudo()} vso trigger-update --now", shell=True)


def update_apps_rpm_ostree():
    """Updates Fedora Silverblue using rpm-ostree"""

    # If rpm-ostree command exists rus commands to update apps
    if shutil.which("rpm-ostree") is not None:
        # Updates system
        subprocess.run("rpm-ostree upgrade", shell=True)


def update_apps_apx():
    """Updates apps on Vanilla OS that are not installed using Flatpak"""

    # If APX command exists, rus commands to update apps
    if shutil.which("apx") is not None:
        # APT, AUR, DNF apps
        subprocess.run("apx update --all -y", shell=True)
        subprocess.run("apx upgrade --all -y", shell=True)
        subprocess.run("apx autoremove --all", shell=True)


def update_apps_snap():
    """Updates apps installed through snap."""

    # Installs snap updates.
    if shutil.which("snap") is not None:
        subprocess.run(f"{use_sudo()} snap refresh", shell=True)


def update_apps_flatpak():
    """Updates Linux apps installed using Flatpak"""

    # Runs update for Flatpak command
    if shutil.which("flatpak") is not None:
        subprocess.run("flatpak update -y", shell=True)


def update_apps_apk():
    """Updates Linux apps installed using Alpine's APK package manager"""

    # Runs update for APK command
    if shutil.which("apk") is not None:
        subprocess.run("apk update", shell=True)
        subprocess.run("apk upgrade", shell=True)


def update_apps_dnf():
    """Updates Linux apps installed using dnf"""

    # Runs update for DNF command
    if shutil.which("dnf") is not None:
        subprocess.run(f"{use_sudo()} dnf --refresh -y upgrade", shell=True)


def update_apps_pacman():
    """Updates Linux apps installed using pacman"""

    # Runs update for PACMAN command
    if shutil.which("pacman") is not None:
        subprocess.run(f"{use_sudo()} pacman -Syuq", shell=True)


def update_apps_pacman_aur():
    """Updates Linux apps installed using pacman-aur"""
    if shutil.which("yay") is not None:
        subprocess.run("yay -Syuq", shell=True)
    elif shutil.which("paru") is not None:
        subprocess.run("paru -Syuq", shell=True)


def update_apps_homebrew():
    """Updates apps installed through Homebrew"""

    # Runs Homebrew apt updates.
    if shutil.which("brew") is not None:
        subprocess.run("brew update", shell=True)
        subprocess.run("brew upgrade", shell=True)


def update_apps_mac_os_x():
    """Updates aps installed through Homebrew, and system updates."""
    # Updates system software
    subprocess.run(f"{use_sudo()} softwareupdate -l -i -a -R", shell=True)


def update_apps_windows():
    """Updates apps installed through the Windows app store."""

    # Windows app store updates.
    subprocess.run("winget upgrade -h –all -u --force --disable-interactivity", shell=True)
    # Windows updates.
    subprocess.run("wuauclt /DetectNow /UpdateNow", shell=True)


@run_time
def update_apps():
    """Determines the OS and chooses how to update applications."""

    # Detects OS and runs updates for matches.
    if platform.system() == "Linux":
        update_apps_apx()
        update_apps_vso()
        update_apps_rpm_ostree()
        update_apps_apt()
        update_apps_dnf()
        update_apps_snap()
        update_apps_flatpak()
        update_apps_apk()
        update_apps_pacman()
        update_apps_pacman_aur()
        update_apps_homebrew()
    elif platform.system() == "Darwin":
        update_apps_mac_os_x()
        update_apps_homebrew()
    elif platform.system() == "Windows":
        update_apps_windows()


# Entrypoint for the running of the application
if __name__ == '__main__':
    update_apps()
