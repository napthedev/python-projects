from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import requests
import os
import ctypes
from Set_Registry import set_reg
from apscheduler.schedulers.blocking import BlockingScheduler

TEXT_COLOR = (2, 176, 250)
FONT_FAMILY = "Eksell Display Medium.otf"
url = "https://api.openweathermap.org/data/2.5/weather?id=1581130&appid=8ea1694d26c50ba0da230cb1224b58bc"
font_big = ImageFont.truetype(FONT_FAMILY, 250)
font_medium = ImageFont.truetype(FONT_FAMILY, 130)
font_sm = ImageFont.truetype(FONT_FAMILY, 70)


def format_time(time):
    if len(time) < 2:
        time = "0" + time
    return time


def update_weather():
    global url, icon, description, temp
    try:
        print("Updating weather data")
        res = requests.get(url)

        icon_url = f"https://openweathermap.org/img/wn/{res.json()['weather'][0]['icon']}@2x.png"
        description = res.json()['weather'][0]['description']
        temp = res.json()['main']['temp'] - 273.15

        temp = round(temp, 1)

        res = requests.get(icon_url)
        icon = res.content

        with open("icon.jpg", "wb") as file:
            file.write(icon)

        icon = Image.open("icon.jpg")
        icon = icon.resize((icon.width * 2, icon.height * 2), Image.ANTIALIAS)
    except Exception as bug:
        print(bug)


def main():
    global TEXT_COLOR, font_big, font_medium, font_sm, hour
    try:
        print("Refreshing data every 1 minute")

        now = datetime.now()
        hour = now.strftime("%H")
        if now.strftime("%H") != "12":
            hour = format_time(str(int(now.strftime("%H")) % 12))
        minutes = format_time(now.strftime("%M"))
        am_pm = "pm" if int(now.strftime("%H")) >= 12 else "am"

        img = Image.open("wallpaper.png")

        img = img.convert("RGBA")

        draw = ImageDraw.Draw(img)

        w, h = draw.textsize(hour, font=font_big)
        draw.text(((img.width - w) / 2, 50), hour, font=font_big, fill=TEXT_COLOR)

        draw.text(((img.width + w) / 2 + 20, 100), am_pm, font=font_sm, fill=TEXT_COLOR)

        w, h = draw.textsize(minutes, font=font_big)
        draw.text(((img.width - w) / 2, 300), minutes, font=font_big, fill=TEXT_COLOR)

        w, h = draw.textsize(now.strftime("%A"), font=font_medium)
        draw.text((500 - w / 2, 180), now.strftime("%A"), font=font_medium, fill=TEXT_COLOR)
        w, h = draw.textsize(now.strftime("%B %d, %Y"), font=font_sm)
        draw.text((500 - w / 2, 370), now.strftime("%B %d, %Y"), font=font_sm, fill=TEXT_COLOR)

        img.paste(icon, (1830, 160), icon)

        w, h = draw.textsize(f"{temp}°C", font=font_medium)
        draw.text((2040, 180), f"{temp}°C", font=font_medium, fill=TEXT_COLOR)

        average = (1830 + 2200 + w / 2) / 2 + 35

        w, h = draw.textsize(description, font=font_sm)
        draw.text((average - w / 2, 370), description, font=font_sm, fill=TEXT_COLOR)

        img.save("output.png")

        IMG_PATH = os.path.join(os.getcwd(), "output.png")

        ctypes.windll.user32.SystemParametersInfoW(20, 0, IMG_PATH, 0)

        set_reg("WallPaper", os.path.join(os.getcwd(), "wallpaper.png"))

        print("Wallpaper changed")
    except Exception as bug:
        print(bug)


update_weather()
main()

scheduler = BlockingScheduler()
scheduler.add_job(main, "interval", minutes=1)
scheduler.start()

scheduler_2 = BlockingScheduler()
scheduler_2.add_job(update_weather, "interval", minutes=15)
scheduler_2.start()
