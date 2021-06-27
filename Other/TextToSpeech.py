import pyttsx3

speaker = pyttsx3.init()
rate = speaker.getProperty("rate")
speaker.setProperty("rate", 150)
voices = speaker.getProperty("voices")
speaker.setProperty("voice", voices[1].id)

with open("Example.txt", "r", encoding="utf8") as file:
    content = file.read()

speaker.say(content)
speaker.runAndWait()
