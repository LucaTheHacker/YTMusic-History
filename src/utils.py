import shutil
import os


def get_dir_size(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total


def get_fs_stats():
    download_folder_size = get_dir_size('/downloads')
    download_folder_filecount = len([name for name in os.listdir('/downloads') if os.path.isfile(name)])
    database_size = os.path.getsize('/database/database.db')
    return download_folder_size, download_folder_filecount, database_size
