"""Misc helper functions."""


def convert_path_objects_to_path_strings(t_paths):
    """Convert a tuple of WindowsPath objects to a simple list of paths."""
    return [str(path) for path in t_paths]
