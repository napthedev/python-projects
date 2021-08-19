from tkinter import *
from tkinter import ttk
import random
from playsound import playsound

response = open("Data/wordlist.txt", "r")
words = response.read().splitlines()
word = random.choice(words).lower()
while len(word) <= 1:
    word = random.choice(words).lower()


root = Tk()
root.title("Hang man")
root.geometry("550x180")
root.resizable(0, 0)
root.iconbitmap("Data/app.ico")

right = []
correct_count = 0
wrong = []
wront_output = StringVar()
limit = len(word) + 2
display = StringVar()
answer = ""
chances = StringVar()
chances.set(f"You have {limit - len(wrong)} chances left")
for i in range(len(word)):
    display.set(display.get() + " _ ")


def submit(event):
    global answer, display, wrong, chances, submit_el, right, limit, correct_count, word, box
    answer = box.get().lower()
    if len(answer) != 1:
        box.delete(0, END)
        playsound("Data/wrong.wav", False)
        return
    if word.find(answer) < 0:
        if wrong.count(answer) == 0:
            wrong.append(answer)
        wront_output.set("  ".join(wrong))
        box.delete(0, END)
        playsound("Data/wrong.wav", False)
    else:
        if len(right) == 0:
            right.append(answer)
            correct_count += word.count(answer)
            box.delete(0, END)
            playsound("Data/right.wav", False)
        else:
            try:
                index = right.index(answer)
            except Exception:
                index = -1
            if index != -1:
                box.delete(0, END)
                playsound("Data/wrong.wav", False)
                return
            else:
                right.append(answer)
                correct_count += word.count(answer)
                box.delete(0, END)
                playsound("Data/right.wav", False)

    display.set("")
    for i in range(len(word)):
        display.set(display.get() + f" {word[i]} ")

    for letter in word:
        try:
            index = right.index(letter)
        except Exception:
            index = -1

        if index == -1:
            display.set(display.get().replace(letter, "_"))

    chances.set(f"You have {limit - len(wrong)} chances left")
    if limit - len(wrong) <= 0:
        display.set(word)
        box["state"] = DISABLED
        playsound("Data/lose.wav", False)
        display_el["foreground"] = "#FF0000"

        submit_el["state"] = DISABLED
    if correct_count >= len(word):
        display.set(word)
        box["state"] = DISABLED
        playsound("Data/win.wav", False)

        display_el["foreground"] = "#00FF00"
        submit_el["state"] = DISABLED


display_el = ttk.Label(root, textvariable=display, font=("Arial", 25), justify="center")
display_el.pack(pady=15)


chances_el = ttk.Label(root, textvariable=chances)
chances_el.place(x=50, y=80)

box = ttk.Entry(root, width=10, font=("Arial", 15))
box.bind('<Return>', submit)
box.place(x=320, y=80)

submit_el = ttk.Button(root, text="Guess!", command=submit)
submit_el.place(x=450, y=80)

wrong_el = ttk.Label(root, textvariable=wront_output, foreground="red", font=("Arial", 20))
wrong_el.pack(pady=(50, 0))


root.mainloop()
