import os

from utils import dt_now_as_text
from ios import read_json, write_json


class Settings:
    def __init__(self, path: str):
        print(f"[{dt_now_as_text()}] loading settings...")

        self.path = path
        if not os.path.isfile(path):
            self.create_file()

        data = read_json(path)

        # input / output
        self.input = data["input"]
        self.output = data["output"]

        # image settings
        self.use_geo = data["use_geo"]
        self.use_time = data["use_time"]
        self.remove_thumbnail = data["remove_thumbnail"]

        # add folders
        if not os.path.isdir(self.input):
            os.makedirs(self.input)

        if not os.path.isdir(self.output):
            os.makedirs(self.output)

    def create_file(self):
        print(f"[{dt_now_as_text()}] No settings found, creating new ones...")
        data = {
            "input": "input",
            "output": "output",
            "use_geo": True,
            "use_time": True,
            "remove_thumbnail": True
        }

        write_json(self.path, data)

