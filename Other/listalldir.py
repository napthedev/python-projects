import os
import json


def path_to_dict(path):
    obj = {"name": os.path.basename(path)}
    if os.path.isdir(path):
        obj["children"] = [path_to_dict(os.path.join(path, x)) for x in os.listdir(path)]
    return obj


data = json.dumps(path_to_dict(r"D:\Setup"), indent=2, sort_keys=True)

with open("allsetupfile.json", "w") as file:
    file.write(data)
