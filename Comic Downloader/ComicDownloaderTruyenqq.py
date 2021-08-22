from bs4 import BeautifulSoup
import requests
import os
import threading


def main(download_url, name, links):
    if not os.path.exists(name):
        os.mkdir(name)

    for link in links:
        download(name, link["text"], link["href"])


def request_image(name, images, image, images_dir, i, j):
    image_link = image["src"]
    response = requests.get(image_link, headers={
        "referer": "http://truyenqq.net/"
    })

    if response.ok:
        with open(os.path.join(images_dir, f"{j + 1}.jpg"), "wb") as file:
            file.write(response.content)
    else:
        print(f"Image number {j + 1} in {i} is corrupted")


def download(name, i, url):
    try:
        images_dir = os.path.join(name, f"{name} {i}")
        if not os.path.exists(images_dir):
            os.mkdir(images_dir)

        response = requests.get(url, headers={
            "referer": "http://truyenqq.net/"
        })
        soup = BeautifulSoup(response.text, "html.parser")

        images = soup.select(".story-see-content img")

        for j, image in enumerate(images):
            th = threading.Thread(target=lambda: request_image(name, images, image, images_dir, i, j))
            th.start()

        print(f"Downloading {i}")
    except Exception as bug:
        print(bug)
        print("Trying to redownload...", end="\r")
        download(name, i, url)


def validate(download_url):
    try:
        res = requests.get(download_url, headers={
            "referer": "http://truyenqq.net/"
        })
        soup = BeautifulSoup(res.text, "html.parser")

        links = soup.select(".works-chapter-list a")

        invalid_chars = ["/", "\\", ":", "*", "?", "\"", "<", ">", "|"]

        temp = []
        for i in links:
            text = i.getText()
            for j in invalid_chars:
                text = text.replace(j, "")
            temp.append({
                "href": i["href"],
                "text": text
            })

        links = temp.copy()
        links.reverse()

        if links:
            return links

        return None
    except Exception as bug:
        print(bug)
        return None


print(f"Software to download comics from http://truyenqq.net/")

download_url = input("Enter the comic URL you want to download: ")

validate_result = validate(download_url)

if validate_result:
    name = input("Enter the name you want to save: ")
    main(download_url, name, validate_result)
else:
    print("\nThe URL is invalid or there an unknown error")
    input()
