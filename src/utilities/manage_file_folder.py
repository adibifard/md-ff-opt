import glob
import os
import shutil
import sys


class SourceCodeFileFinder:
    def __init__(self):
        self._main_path = os.path.abspath(sys.modules['__main__'].__file__)
        self._dirname = os.path.dirname(self._main_path)

    def find_file_in_subdirectories(self, filename):
        """
        Search for a file within all nested subdirectories of the given start path.
        :return: The path to the file if found, otherwise None.
        """

        pattern = os.path.join(self._dirname, '**', filename)
        for filepath in glob.glob(pattern, recursive=True):
            return filepath
        return None


def get_file_names_and_paths(directory):
    file_names = os.listdir(directory)
    file_paths = [os.path.join(directory, file) for file in file_names if
                  os.path.isfile(os.path.join(directory, file))]
    return file_names, file_paths


def find_file(file_name, search_paths):
    """
    Search for a file in a list of directories and return the first path found.

    :param file_name: The name of the file to search for.
    :param search_paths: A list of directories to search.
    :return: The path to the file if found, otherwise None.
    """
    for base_path in search_paths:
        potential_path = os.path.join(base_path, file_name)
        if os.path.exists(potential_path):
            return potential_path
    return None


def find_files_with_extension(directory_path, file_extension):
    """
    Find all files within a directory with a specific extension.
    :param directory_path: Path to the directory
    :param file_extension: Extension of the files to find
    :return: List of file paths with the specified extension
    """
    matching_files = []

    # Check if the directory exists
    if not os.path.isdir(directory_path):
        print("Directory does not exist.")
        return matching_files

    # Iterate through all files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(file_extension):
            # Append the full path of the file
            matching_files.append(os.path.join(directory_path, filename))

    return matching_files


def filter_files_by_word(file_names, file_paths, word):
    # Filter the files that contain the specific word in their names
    filtered_file_names = [name for name in file_names if word in name]
    filtered_file_paths = [path for path, name in zip(file_paths, file_names) if word in name]
    return filtered_file_names, filtered_file_paths


def get_sorted_folders(directory):
    # List all entries in the given directory
    entries = os.listdir(directory)

    # Filter out the entries that are directories
    folders = [entry for entry in entries if os.path.isdir(os.path.join(directory, entry))]

    # Sort the folders
    folders.sort()

    return folders


def get_and_sort_folders(directory):
    # Extract folders and their full paths
    folders = []
    folder_paths = []

    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)
        if os.path.isdir(full_path):
            folders.append(entry)
            folder_paths.append(full_path)

    # Sort the folders and their paths based on folder names
    sorted_folders = sorted(folders)
    sorted_folder_paths = [os.path.join(directory, folder) for folder in sorted_folders]

    return sorted_folders, sorted_folder_paths


def remove_folder_contents(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Remove all contents of the folder
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)  # Remove files and links
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Remove subdirectories
        return f"All contents of the folder '{folder_path}' have been removed."
    else:
        return f"The folder '{folder_path}' does not exist."
