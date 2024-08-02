import os

def delete_sync_conflict_files(folder_path):
    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        # Check if "sync-conflict" is in the filename
        if "sync-conflict" in filename:
            file_path = os.path.join(folder_path, filename)
            # Check if it is a file (not a directory)
            if os.path.isfile(file_path):
                try:
                    # Delete the file
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

# Specify the folder path
folder_path = '/home/adam178/amm-obsidian-vault/Language Learning/Korean/Eps textbook notes'

# Call the function
delete_sync_conflict_files(folder_path)

