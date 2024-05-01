import os
from typing import List, Union

from data_models import File, Folder


def create_nested_file_structure(root_path: str) -> Folder:
    """
    Function which builds an object with Folders and Files.

    Parameters:
        root_path (str): Path of the root folder/directory.

    Returns:
        Folder: An object which contains nested Folders or Files.
    """  # noqa: E501

    root_name = os.path.basename(__check_path(root_path))
    nested_structure = {
        "name": root_name,
        "files": __create_file_structure(root_path),
    }

    return Folder(**nested_structure)


def __check_path(path: str) -> str:
    """
    Checks if path ends with a slash or backslash  to prevent os.path.basename
    from returning an empty string.

    Parameters:
        path (str): a path to a folder or file.

    Returns:
        path (str): a path without trailing slash or backslash.
    """  # noqa: E501

    if path[-1] == "/" or path[-1] == "\\":
        path = path[0:-1]

    return path


def __create_file_structure(path: str) -> List[Union[Folder, File]]:
    """
    Creates a list of nested Folder or Files.

    Parameters:
        path (str): a path to a folder or file.

    Returns:
        file_structure (List[Union[Folder, File]]): list of nested Folder or Files.
    """  # noqa: E501

    items = os.listdir(path)
    file_structure: List[Union[Folder, File]] = []

    for item in items:
        if item[0] == ".":
            continue
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            folder_item = {
                "name": item,
                "files": __create_file_structure(item_path),
            }
            file_structure.append(Folder(**folder_item))
        elif os.path.isfile(item_path):
            file_item = {"name": item, "path": item_path}
            file_structure.append(File(**file_item))

    return file_structure

def create_directory(path: str) -> None:
    """
    Create a directory if it does not exist.

    Parameters:
        path (str): The path of the directory to be created.
    """
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception as e:
            print(f"Error creating directory '{path}': {e}")