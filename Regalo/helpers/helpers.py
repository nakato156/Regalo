import os

def get_size_file(file_path):
    return os.path.getsize(file_path)

def format_size(size):
    if size < 1024:
        return str(size) + "B"
    elif size < 1024 * 1024:
        return str(round(size / 1024, 2)) + "KB"
    else:
        return str(round(size / 1024 / 1024, 2)) + "MB"

def get_format_size(file_path):
    return format_size(get_size_file(file_path))
