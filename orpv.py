#!/usr/bin/env python

import os
import subprocess
import random


def is_mounted(mount_point):
    """Check if a specific mount point is mounted."""
    return os.path.ismount(mount_point)

def mount_partition(device, mount_point):
    """Attempt to mount a partition."""
    response = input(f"The partition '{device}' is not mounted. Do you want to mount it? (yes/no): ").strip().lower()
    if response in ["yes", "y"]:
        try:
            # Mount the partition to the mount point
            subprocess.run(["sudo", "mount", device, mount_point], check=True)
            print(f"Mounted '{device}' to '{mount_point}' successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to mount '{device}': {e}")
            return False
    else:
        print(f"Skipping mount for '{device}'.")
        return False
    return True

def open_random_file(folder_path):
    """Open a random file from the folder or its subfolders."""
    import random

    files = []
    for root, _, filenames in os.walk(folder_path):
        for filename in filenames:
            files.append(os.path.join(root, filename))

    if not files:
        print(f"No files found in '{folder_path}'.")
        return

    random_file = random.choice(files)
    print(f"Opening: {random_file}")

    if os.name == "nt":  # Windows
        os.startfile(random_file)
    elif os.name == "posix":  # Linux/Mac
        subprocess.run(["xdg-open", random_file])
    else:
        print("Unsupported operating system.")

if __name__ == "__main__":
    partitions = {
        "/dev/sdb6": "/Storage2/"
    }

    directories = ["/Storage2/.crimozone/"]

    # Check and mount partitions
    for device, mount_point in partitions.items():
        if not is_mounted(mount_point):
            print(f"The partition '{device}' is not mounted.")
            if not mount_partition(device, mount_point):
                print(f"Skipping directories under '{mount_point}'.")
                continue

    # Process directories
    directory = random.choice(directories)
    if os.path.exists(directory):
        open_random_file(directory)
    else:
        print(f"The directory '{directory}' does not exist after mounting.")
