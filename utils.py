"""Here are the utility funcions"""

import os

def check_valid_path(path):
    return os.path.exists(path)

def make_raw_string(string):
    return string.replace("\\", "\\\\")