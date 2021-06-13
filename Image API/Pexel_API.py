import requests
import os
import getpass
import ctypes
from Set_Registry import set_reg
import random

USER = getpass.getuser()
WALLPAPER_DIR = r'C:\Users\{}\AppData\Roaming\Microsoft\Windows\Themes'.format(USER)
IMG_PATH = os.path.join(WALLPAPER_DIR, "pexel_api.jpg")

page = random.randint(1, 100)
API = f"https://api.pexels.com/v1/search?query=nature&per_page=1000&orientation=landscape&page={page}"


def set_pexel_wallpaper():
    global IMG_PATH, WALLPAPER_DIR, API
    try:
        print("Requesting wallpaper from Pexel API")
        res = requests.get(API, headers={
            "Authorization": "563492ad6f91700001000001e2c7a407d092472da11bd6f1d23228d5"
        })

        images = res.json()["photos"]

        urls = []

        for image in images:
            urls.append(image["src"]["landscape"])

        image_url = random.choice(urls)

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


set_pexel_wallpaper()
