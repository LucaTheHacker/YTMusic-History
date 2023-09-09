import shutil
import os


def get_fs_stats():
    _, download_folder_size, _ = shutil.disk_usage("/downloads")
    download_folder_filecount = len([name for name in os.listdir('/downloads') if os.path.isfile(name)])
    database_size = os.path.getsize('/database/database.db')
    return download_folder_size, download_folder_filecount, database_size
