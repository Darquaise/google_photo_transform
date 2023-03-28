import os

from settings import Settings
from utils import verbose_print


def reorder_photos(settings: Settings, verbose: bool = False):
    total = 0
    json = 0
    moved = 0

    for folder in os.listdir(settings.input):
        verbose_print(f"Start scanning folder '{folder}'", verbose)
        current = 0
        folder_count = 1
        for file in os.listdir(f"{settings.input}/{folder}"):
            total += 1
            if file.endswith(".json"):
                json += 1
                continue

            moved += 1
            current += 1
            if current > 100:
                folder_count += 1
                current = 0

            old_file_path = f"{settings.input}/{folder}/{file}"
            new_path = f"{settings.output}/{folder}_{folder_count}"
            new_file_path = f"{new_path}/{file}"

            verbose_print(new_file_path, verbose)

            if not os.path.exists(new_path):
                os.makedirs(new_path)
            os.rename(old_file_path, new_file_path)

    verbose_print("", verbose)
    verbose_print("", verbose)
    verbose_print(f"{total} files ({json} json files)\n{moved} moved", verbose)
