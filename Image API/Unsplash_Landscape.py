import requests
import os
import getpass
import ctypes
from Set_Registry import set_reg

USER = getpass.getuser()
WALLPAPER_DIR = r'C:\Users\{}\AppData\Roaming\Microsoft\Windows\Themes'.format(USER)
IMG_PATH = os.path.join(WALLPAPER_DIR, "unsplash_api.jpg")
url = "https://source.unsplash.com/1920x1080/?landscape"


def set_unsplash_wallpaper():
    global IMG_PATH, WALLPAPER_DIR, url
    try:
        print("Requesting wallpaper from Unsplash")
        image = requests.get(url)

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


set_unsplash_wallpaper()
