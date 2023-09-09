import os


def get_dir_size(path='.'):
    total = 0
    count = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
                count += 1
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total, count


def get_fs_stats():
    download_folder_size, download_folder_filecount = get_dir_size('/downloads')
    database_size = os.path.getsize('/database/database.db')
    return download_folder_size, download_folder_filecount, database_size
