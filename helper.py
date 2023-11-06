import os

IMAGE_RES = 150

def get_subdirectory(sub_directory: str) -> str:
    """
    `input`: A sub-directory string

    `returns`: A filepath
    """
    current_directory = os.getcwd()
    print("Current Directory:", current_directory)

    return os.path.join(current_directory, sub_directory)


def build_directory_lookup(training_path: str):
    directory_lookup = {}
    directory_reverse_lookup = {}
    count = 0

    for filename in os.listdir(training_path):
        if not filename.startswith("."):
            directory_lookup[filename] = count
            directory_reverse_lookup[count] = filename
            count += 1

    return directory_lookup, directory_reverse_lookup
