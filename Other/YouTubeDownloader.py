try:
    from pytube import YouTube
    link = input("Enter video URL: ")
    video = YouTube(link)
    print("Downloading...")
    video.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first().download()
    print("Download finished")
    input()
except Exception as bug:
    print(bug)
    print("Failed to download!")
    input()
