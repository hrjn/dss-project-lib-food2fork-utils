import requests
import time
import os
import sys

def safe_str(val):
    if sys.version_info > (3, 0):
        return str(val)
    else:
        if isinstance(val, unicode):
            return val.encode("utf-8")
        else:
            return str(val)


def get_file_path(folder_path, file_name):
    # Be careful to enforce that folder_path and file_name are actually strings
    return os.path.join(safe_str(folder_path), safe_str(file_name))

def download_files_to_managed_folder(folder_path, files_info, chunk_size=8192):
    total_size = 0
    bytes_so_far = 0
    for file_info in files_info:
        response = requests.get(file_info["url"], stream=True)
        total_size += int(response.headers.get('content-length'))
        file_info["response"] = response
    update_time = time.time()
    for file_info in files_info:
        with open(get_file_path(folder_path, file_info["filename"]), "wb") as f:
            for content in file_info["response"].iter_content(chunk_size=chunk_size):
                f.write(content)

