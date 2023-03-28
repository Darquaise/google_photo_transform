import os
from PIL import Image
import piexif
from datetime import datetime

from settings import Settings
from utils import verbose_print, letlon2dms
from ios import read_json


def transform_gps_json2exif(gd: dict):
    return {
        1: b'N' if gd['latitude'] > 0 else b'S',
        2: letlon2dms(gd['latitude']),
        3: b'E' if gd['longitude'] > 0 else b'W',
        4: letlon2dms(gd['longitude'] if gd['longitude'] > 0 else gd['longitude'] * -1),
        5: 0,
        6: (int(gd['altitude']), 1)
    }


def locate_json(path: str):
    if os.path.isfile(path + ".json"):
        return path + ".json"

    *file_path, name = path.split("/")
    return "/".join(file_path) + "/" + name[:46] + ".json"


def transform_jpg(path: str, verbose: bool = False):
    # get data
    jpg_data = piexif.load(path)
    json_data = read_json(locate_json(path))

    photo_taken = datetime.fromtimestamp(int(json_data['photoTakenTime']['timestamp'])).strftime("%Y:%m:%d %H:%M:%S")
    geodata = json_data['geoData']

    # overwrite data
    jpg_data['0th'][piexif.ImageIFD.DateTime] = photo_taken
    jpg_data['Exif'][piexif.ExifIFD.DateTimeOriginal] = photo_taken
    jpg_data['Exif'][piexif.ExifIFD.DateTimeDigitized] = photo_taken

    # remove thumbnail
    jpg_data['thumbnail'] = None

    # * overwrite if location data exists in json data
    if float(geodata['latitude']) != 0.0:
        jpg_data["GPS"] = transform_gps_json2exif(geodata)

    # store new data
    piexif.remove(path)
    piexif.insert(piexif.dump(jpg_data), path)


def transform_png(png_path: str, verbose: bool = False):
    # transform png to jpg
    path = png_path[:-3] + "jpg"
    Image.open(png_path).convert('RGB').save(path, quality=95)
    os.remove(png_path)

    # insert exif data into jpg
    json_path = locate_json(png_path)
    json_data = read_json(json_path)
    photo_taken = datetime.fromtimestamp(int(json_data['photoTakenTime']['timestamp'])).strftime("%Y:%m:%d %H:%M:%S")

    exif_data = {
        "0th": {piexif.ImageIFD.DateTime: photo_taken},
        "Exif": {piexif.ExifIFD.DateTimeOriginal: photo_taken, piexif.ExifIFD.DateTimeDigitized: photo_taken},
        "GPS": transform_gps_json2exif(json_data['geoData']),
        "Interop": {},
        "1st": {},
        "thumbnail": None
    }

    piexif.insert(piexif.dump(exif_data), path)

    # change json file name
    os.rename(json_path, path + ".json")


def scan_photos(settings: Settings, verbose: bool = False):
    total = 0
    jpg = 0
    png = 0
    changed = 0
    deleted = 0
    too_long = 0

    for folder in os.listdir(settings.input):
        verbose_print(f"Start scanning folder '{folder}'", verbose)
        for file in os.listdir(f"{settings.input}/{folder}"):
            if file.endswith(".json"):
                continue

            total += 1
            path = f"{settings.input}/{folder}/{file}"
            verbose_print(f"{folder}/{file}", verbose)

            if "bearbeitet" in file or "(1)" in file:
                deleted += 1
                os.remove(path)
                continue
            elif len(file) == 51:
                too_long += 1
                continue

            if file.lower().endswith(".jpg") or file.lower().endswith(".jpeg"):
                jpg += 1
                changed += 1
                transform_jpg(path, verbose)

            elif file.lower().endswith(".png"):
                png += 1
                changed += 1

                transform_png(path, verbose)

    verbose_print("", verbose)
    verbose_print("", verbose)
    verbose_print(
        f"{total} total images and videos\n"
        f"{changed} images changed\n"
        f"* {jpg} JPEGs\n"
        f"* {png} PNGs\n"
        f"{deleted} deleted, {too_long} were too long",
        verbose
    )
