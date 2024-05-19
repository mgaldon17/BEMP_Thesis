import os


def ensureDirectoryExists(directory_name):
    """Ensure that a directory exists. If it doesn't, create it."""
    try:
        os.makedirs(directory_name, exist_ok=True)
    except PermissionError:
        print(f"Permission denied: Could not create directory '{directory_name}'.")
    except Exception as e:
        print(f"An error occurred while trying to create directory '{directory_name}': {e}")
