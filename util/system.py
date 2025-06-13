import os

def get_home_directory() -> str:
    return os.path.expanduser("~").__str__()