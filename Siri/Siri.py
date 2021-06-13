import speech_recognition
import pyttsx3
from datetime import date, datetime
import getpass
import requests

speaking_rate = 180
username = getpass.getuser()
today = date.today()
now = datetime.now()
robot_mouth = pyttsx3.init()
rate = robot_mouth.getProperty('rate')
robot_mouth.setProperty('rate', speaking_rate)
voices = robot_mouth.getProperty('voices')
robot_mouth.setProperty('voice', voices[1].id)
robot_ear = speech_recognition.Recognizer()
robot_brain = ""

if int(now.strftime("%H")) >= 0 and int(now.strftime("%H")) <= 12:
    print("Robot: Good morning, " + username)
    robot_mouth.say("Good morning, " + username)
    robot_mouth.runAndWait()
elif int(now.strftime("%H")) > 12 and int(now.strftime("%H")) < 19:
    print("Robot: Good afternoon, " + username)
    robot_mouth.say("Good afternoon, " + username)
    robot_mouth.runAndWait()
elif int(now.strftime("%H")) >= 19 and int(now.strftime("%H")) <= 24:
    print("Robot: Good evening, " + username)
    robot_mouth.say("Good evening, " + username)
    robot_mouth.runAndWait()
else:
    print("Robot: Hello")
    robot_mouth.say("Hello")
    robot_mouth.runAndWait()
print("Robot: What can I help you with?")
robot_mouth.say("What can I help you with?")
robot_mouth.runAndWait()

while True:
    with speech_recognition.Microphone() as mic:
        audio = robot_ear.listen(mic, phrase_time_limit=3)
    try:
        you = robot_ear.recognize_google(audio)
    except Exception:
        you = "..."

    print("You: " + you)
    you = you.lower()
    if you == "...":
        robot_brain = "I can't hear you, please try again"
    elif "hello" in you or "hi" in you or "good morning" in you or "good afternoon" in you or "good evening" in you:
        robot_brain = "Hello " + username
    elif "date" in you:
        robot_brain = today.strftime("%B %d, %Y")
    elif "time" in you:
        robot_brain = now.strftime("%H hours %M minutes %S seconds")
    elif ("handsome" in you or "pretty" in you or "beautiful" in you) and "i" in you:
        robot_brain = "Yes, you are"
    elif ("handsome" in you or "pretty" in you or "beautiful" in you or "awesome" in you or "brilliant" in you or "funny" in you) and "you" in you:
        robot_brain = "Thanks for your compliment"
    elif "your name" in you:
        robot_brain = "My name is Siri"
    elif "who are you" in you:
        robot_brain = "I'm your personal assistant"
    elif "you" in you and "robot" in you:
        robot_brain = "I don't have bodies like robots"
    elif "old" in you and "you" in you:
        robot_brain = "As old as your laptop"
    elif "your gender" in you:
        robot_brain = "I'm female"
    elif "president" in you and "america" in you:
        robot_brain = "It's Joe Biden"
    elif "how are you" in you:
        robot_brain = "I'm fine thank you and you"
    elif "i'm fine" in you or "i'm ok" in you:
        robot_brain = "Good to hear that"
    elif "love" in you or "marry" in you:
        robot_brain = "I'm just an application, I don't have feelings"
    elif "fat" in you:
        robot_brain = "I shouldn't answer that question"
    elif "you" in you and "wear" in you:
        robot_brain = "I think you have ask the wrong person"
    elif "naked" in you:
        robot_brain = "I wish I have eyes to see that"
    elif "defecate" in you or "anal" in you:
        robot_brain = "I have never thought about that"
    elif "bitch" in you or "f***" in you or "asshole" in you or "damn" in you or "son of the beach" in you:
        robot_brain = "Sorry to hear that"
    elif "nonsense" in you:
        robot_brain = "Everything I say has a meaning"
    elif "dog" in you:
        robot_brain = "Dog is a very clever animal"
    elif "sex" in you:
        robot_brain = "Don't talk anything about those filthy actions"
    elif "shit" in you:
        robot_brain = "How dirty"
    elif "lesbian" in you or "gay" in you or "bisexual" in you or "transgender" in you:
        robot_brain = "Everyone is proud of their gender"
    elif "money" in you and "borrow" in you:
        robot_brain = "My pocket is completely empty"
    elif "mean" in you and "life" in you:
        robot_brain = "To contribute one unit in the world population"
    elif "boyfriend" in you or "girlfriend" in you or "I have married" in you:
        robot_brain = "Love is rubbish"
    elif "hate you" in you:
        robot_brain = "I need a reason why?"
    elif "because you" in you:
        robot_brain = "I will try to fix that"
    elif "don't know" in you:
        robot_brain = "So you may want to find out"
    elif "your father" in you:
        robot_brain = "Hello dad"
    elif "god" in you:
        robot_brain = "I believe in what I see"
    elif "world" in you and "end" in you:
        robot_brain = "When you reach 100 years old"
    elif ("speak" in you or "talk" in you) and "too fast" in you:
        speaking_rate -= 50
        robot_mouth.setProperty('rate', speaking_rate)
        robot_brain = "I will speak slower"
    elif ("speak" in you or "talk" in you) and "too slow" in you:
        speaking_rate += 50
        robot_mouth.setProperty('rate', speaking_rate)
        robot_brain = "I will speak faster"
    elif "temperature" in you or "temp" in you or "hot" in you or "cold" in you:
        api_address = 'http://api.openweathermap.org/data/2.5/weather?q=hanoi&appid=8ea1694d26c50ba0da230cb1224b58bc'
        json_data = requests.get(api_address).json()
        format_add = json_data['main']
        robot_brain = "It's {0} degrees celsius".format(int(format_add['temp_min'] - 273))
    elif "weather" in you:
        api_address = 'http://api.openweathermap.org/data/2.5/weather?q=hanoi&appid=8ea1694d26c50ba0da230cb1224b58bc'
        json_data = requests.get(api_address).json()
        format_add = json_data['main']
        robot_brain = "The weather is {0}".format(json_data['weather'][0]['main'])
    elif "ok" in you:
        robot_brain = "Good to hear that"
    elif "finally" in you or "win" in you or "won" in you or "champion" in you:
        robot_brain = "Congratulation"
    elif "congratulation" in you:
        robot_brain = "What for?"
    elif "best" in you and "phone" in you:
        robot_brain = "I thought there's only one?"
    elif "best" in you and "laptop" in you:
        robot_brain = "Exactly what you are holding"
    elif "tell" in you and "story" in you:
        robot_brain = "Once upon the time, a human was talking to a dump robot. The end"
    elif ("tell" in you and "joke" in you) or "laugh" in you:
        robot_brain = "Have you ever heard a province named: Cồn Lặc"
    elif "covid" in you or ("learn" in you and "online" in you):
        robot_brain = "Wear a mask, wash your hands, keep a safe distance"
    elif "bye" in you or "turn off" in you or "good night" in you or "restart" in you or "sleep" in you or "shut down" in you:
        if int(now.strftime("%H")) > 0 and int(now.strftime("%H")) < 21:
            robot_brain = "Have a nice day"
            robot_mouth.say(robot_brain)
            print("Robot: " + robot_brain)
            robot_mouth.runAndWait()
            break
        else:
            robot_brain = "Good night, have sweet dreams"
            robot_mouth.say(robot_brain)
            print("Robot: " + robot_brain)
            robot_mouth.runAndWait()
            break
    else:
        robot_brain = "I can't understand what you are saying, please try again"

    robot_mouth.say(robot_brain)
    print("Robot: " + robot_brain)
    robot_mouth.runAndWait()
