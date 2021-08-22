import os
from PIL import Image

root = input("Directory to check: ")

for path, subdirs, files in os.walk(root):
    for name in files:
        if name.endswith(".jpg"):
            filename = os.path.join(path, name)
            try:
                img = Image.open(filename)
                img.verify()
                img.close()
                img = Image.open(filename)
                img.transpose(Image.FLIP_LEFT_RIGHT)
                img.close()
            except Exception:
                print("Corrupted file:", filename)
