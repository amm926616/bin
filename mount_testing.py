import os
import subprocess

def mount_partition(partition: str, mount_point: str) -> None:
    """
    Mounts a partition to a specified mount point.
    
    :param partition: The partition to be mounted (e.g., /dev/sda1).
    :param mount_point: The directory where the partition will be mounted.
    """
    # Ensure the mount point exists
    if not os.path.exists(mount_point):
        os.makedirs(mount_point)
        print(f"Created mount point at {mount_point}")

    # Mount the partition
    try:
        subprocess.run(['sudo', 'mount', partition, mount_point], check=True)
        print(f"Mounted {partition} to {mount_point}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to mount {partition}: {e}")
    except PermissionError:
        print("You need to run this script with root privileges.")

# Example usage
partition = "/dev/sda5"  # Replace with your partition
mount_point = "/mnt"  # Replace with your desired mount point
mount_partition(partition, mount_point)

