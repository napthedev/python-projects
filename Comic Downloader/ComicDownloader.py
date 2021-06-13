from bs4 import *
import requests
import os
import threading


def main(download_url):
    global website
    download_res = requests.get(download_url)
    soup = BeautifulSoup(download_res.text, "html.parser")
    if website == "truyenqq.com":
        temp = soup.select(".works-chapter-list a")
    elif website == "nettruyentop.com":
        temp = soup.select(".list-chapter ul a")
    elif website == "blogtruyen.vn":
        temp = soup.select("#loadChapter a")

    links = []

    if website == "truyenqq.com":
        title = soup.find("title").getText()
        if title.count("|") > 0:
            name = title.split("|")[0].strip()
        elif title.count("-") > 0:
            name = title.split("-")[0].strip()
    elif website == "nettruyentop.com":
        name = soup.find("title").getText()
        if name.count("Đã Full") > 0:
            name = name.split("Đã Full")[0].strip()
        elif name.count("[Tới Chap") > 0:
            name = name.split("[Tới Chap")[0].strip()
    elif website == "blogtruyen.vn":
        name = soup.find("title").getText().replace("| BlogTruyen.Com", "").strip()

    os.system("cls")
    print(f"Đang tải truyện {name}")

    for i in range(len(temp) - 1, -1, -1):
        links.append(temp[i])

    if not os.path.exists(name):
        os.mkdir(name)

    for link in links:
        if website == "truyenqq.com":
            chap_name = link["href"].split("chap-")[-1].replace(".html", "").replace("-", ".")
            download(name, chap_name, link["href"])
        elif website == "nettruyentop.com":
            chap_name = link["href"].split("chap-")[-1].split("/")[0]
            download(name, chap_name, link["href"])
        elif website == "blogtruyen.vn":
            response = requests.get("https://blogtruyen.vn/" + link["href"])
            soup = BeautifulSoup(response.text, "html.parser")
            chap_name = soup.select("header > h1")[0].getText().replace(name, "").strip()
            download(name, chap_name, "https://blogtruyen.vn/" + link["href"])


def request_image(name, images, image, images_dir, i, j):
    global website
    if website == "truyenqq.com":
        image_link = image["src"]
        response = requests.get(image_link, headers={
            "referer": "http://truyenqq.com/"
        })
    elif website == "nettruyentop.com":
        image_link = "http:" + image["src"]
        response = requests.get(image_link, headers={
            "referer": "http://www.nettruyentop.com/"
        })
    elif website == "blogtruyen.vn":
        image_link = image["src"]
        response = requests.get(image_link, headers={
            "referer": "https://blogtruyen.vn/"
        })

    if response.ok:
        with open(os.path.join(images_dir, f"{j + 1}.jpg"), "wb") as file:
            file.write(response.content)
    else:
        print(f"Ảnh số {j + 1} trong chap {i} bị lỗi!!")


def download(name, i, url):
    global website
    try:
        images_dir = os.path.join(name, f"{name} chap {i}")
        if not os.path.exists(images_dir):
            os.mkdir(images_dir)

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        if website == "truyenqq.com":
            images = soup.select(".story-see-content img")
        elif website == "nettruyentop.com":
            images = soup.select(".box_doc img")
        elif website == "blogtruyen.vn":
            images = soup.select("#content img")

        for j, image in enumerate(images):
            th = threading.Thread(target=lambda: request_image(name, images, image, images_dir, i, j))
            th.start()

        print(f"Đã tải chap {i}")
    except Exception as bug:
        print(bug)
        print("Đang thử tải lại...", end="\r")
        download(name, i, url)


websites = [
    "truyenqq.com",
    "nettruyentop.com",
    "blogtruyen.vn"
]

print(" | ".join(websites))
website = input("Gõ tên Website mà bạn muốn tải: ")
while website not in websites:
    website = input(f"Chỉ có thể tải truyện từ {len(websites)} website trên: ")

download_url = input("Nhập URL truyện bạn muốn tải: ")
main(download_url)
