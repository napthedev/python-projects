import requests
import os
import getpass
import ctypes
from Set_Registry import set_reg
import json
import random

USER = getpass.getuser()
WALLPAPER_DIR = r'C:\Users\{}\AppData\Roaming\Microsoft\Windows\Themes'.format(USER)
IMG_PATH = os.path.join(WALLPAPER_DIR, "windows_spotlight.jpg")
API = "https://arc.msn.com/v3/Delivery/Placement?pid=209567&fmt=json&rafb=0&ua=WindowsShellClient%2F0&cdm=1&disphorzres=9999&dispvertres=9999&lo=80217&pl=en-US&lc=en-US&ctry=us&time=2017-12-31T23:59:59Z"


def set_spotlight_wallpaper():
    global IMG_PATH, WALLPAPER_DIR, API
    try:
        print("Requesting wallpaper from Windows Spotlight")
        res = requests.get(API)
        parsed = res.json()["batchrsp"]["items"]

        images = []
        for i in parsed:
            images.append(json.loads(i["item"])["ad"]["image_fullscreen_001_landscape"]["u"])

        image_url = random.choice(images)

        image = requests.get(image_url)

        if os.path.exists(IMG_PATH):
            os.remove(IMG_PATH)

        with open(IMG_PATH, "wb") as file:
            file.write(image.content)
            file.close()

        ctypes.windll.user32.SystemParametersInfoW(20, 0, IMG_PATH, 0)

        set_reg("WallPaper", IMG_PATH)

        print("Wallpaper changed")

    except Exception as bug:
        print(bug)
        print("Changing wallpaper failed!")


set_spotlight_wallpaper()
