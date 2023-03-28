import json


def read_json(path: str):
    with open(path, "r") as f:
        data = json.load(f)
    return data


def write_json(path: str, data: dict):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
