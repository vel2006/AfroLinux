import subprocess
import argparse
import json
import os
import shutil
from pathlib import Path
from packaging.version import parse as parse_version

AFRO_REPO = "https://github.com/vel2006/AfroLinux"
AFRO_PATH = Path("/etc/AfroLinux")
FILES_LIST = AFRO_PATH / "files.json"

AFRO_PATH.mkdir(parents=True, exist_ok=True)
#Loads installed packages
def load_installed_packages():
    
    if FILES_LIST.exists():
        with open(FILES_LIST, "r") as f:
            return json.load(f)
    return {}


#saves installed packages
def save_installed_packages(packages):
    with open(FILES_LIST, "w") as f:
        json.dump(packages, f, indent=4)


#install package
def install_package(package_name):
    try:
        subprocess.check_call(["apt", "install", package_name])
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to install package '{package_name}': {e}")
        return False
    return True


#ches if packages exissts
def package_exists(package_name):
    try:
        subprocess.check_call(["apt", "show", package_name])
        return True
    except subprocess.CalledProcessError as e:
        return False
    

#gets version of package
def get_installed_version(package_name):
    try:
        output = subprocess.check_output(["apt", "show", package_name])
        version = output.decode("utf-8").splitlines()[1].split(":")[1].strip()
        return version
    except subprocess.CalledProcessError as e:
        return None
    

#removes package
def remove_package(package_name):
    if package_exists(package_name):
        try:
            subprocess.check_call(["apt", "remove", package_name])
            packages = load_installed_packages()
            del packages[package_name]
            save_installed_packages(packages)
            print(f"Package '{package_name}' removed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to remove package '{package_name}': {e}")
    else:
        print(f"ERROR: Package '{package_name}' is not installed.")


def main():

    parser = argparse.ArgumentParser(description="Afro Linux Package Manager")
    parser.add_argument("command", choices=["add", "remove", "update", "list", "find", "version"], help="Command to run")
    parser.add_argument("package", nargs="?", help="Package name (if required)")
    args = parser.parse_args()

    if args.command == "add" and args.package:
        if package_exists(args.package):
            if get_installed_version(args.package):
                print(f"ERROR: Package '{args.package}' is already installed.")
            else:
                install_package(args.package)
        else:
            print(f"ERROR: Package '{args.package}' not found.")
    elif args.command == "remove" and args.package:
        remove_package(args.package)
    elif args.command == "update" and args.package:
        subprocess.check_call(["apt", "update", args.package])
    elif args.command == "list":
        subprocess.check_call(["apt", "list", "--installed"])
    elif args.command == "version" and args.package:
        version = get_installed_version(args.package)
        if version:
            print(f"Package '{args.package}' version: {version}")
        else:
            print(f"ERROR: Package '{args.package}' is not installed.")
    elif args.command == "find" and args.package:
        if package_exists(args.package):
            print(f"Package '{args.package}' is available.")
        else:
            print(f"ERROR: Package '{args.package}' not found.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()