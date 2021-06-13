from tkinter import *
import random
from playsound import playsound

response = open("Data/wordlist.txt", "r")
words = response.read().splitlines()
word = random.choice(words).lower()
while len(word) <= 1:
    word = random.choice(words).lower()

right = []
correct_count = 0
wrong = []
limit = len(word) + 2
display = ""
answer = ""
error = ""
for i in range(len(word)):
    display += " _ "


def submit(event):
    global answer, error, error_el, display, display_el, wrong, wrong_el, chances_el, submit_el, right, limit, correct_count, frame1, frame2, word, box
    answer = box.get().lower()
    if len(answer) != 1:
        error = "Guess only ONE letter"
        error_el.forget()
        error_el = Label(frame2, text=error, fg="orange")
        error_el.pack()
        box.delete(0, END)
        playsound("Data/wrong.wav", False)
        return
    if word.find(answer) < 0:
        error = "You guessed wrong"
        error_el.forget()
        error_el = Label(frame2, text=error, fg="red")
        error_el.pack()
        wrong.append(answer)
        wrong_el.forget()
        wrong_el = Label(root, text="  ".join(wrong), fg="red", font=("Arial", 15))
        wrong_el.pack(pady=50)
        box.delete(0, END)
        playsound("Data/wrong.wav", False)
    else:
        if len(right) == 0:
            error = "You guessed the right letter"
            error_el.forget()
            error_el = Label(frame2, text=error, fg="green")
            error_el.pack()
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
                error = "You have already guessed this letter"
                error_el.forget()
                error_el = Label(frame2, text=error, fg="orange")
                error_el.pack()
                box.delete(0, END)
                playsound("Data/wrong.wav", False)
                return
            else:
                error = "You guessed the right letter"
                error_el.forget()
                error_el = Label(frame2, text=error, fg="green")
                error_el.pack()
                right.append(answer)
                correct_count += word.count(answer)
                box.delete(0, END)
                playsound("Data/right.wav", False)

    display = ""
    for i in range(len(word)):
        display += f" {word[i]} "

    for letter in word:
        try:
            index = right.index(letter)
        except Exception:
            index = -1

        if index == -1:
            display = display.replace(letter, "_")

    display_el.forget()
    display_el = Label(frame1, text=display, font=("Arial", 25))
    display_el.pack()
    chances_el.forget()
    chances_el = Label(root, text=f"You have {limit - len(wrong)} chances left")
    chances_el.place(x=50, y=80)
    if limit - len(wrong) <= 0:
        error = "You lose!!!"
        display = word
        display_el.forget()
        display_el = Label(frame1, text=display, font=("Arial", 25))
        display_el.pack()
        error_el.forget()
        error_el = Label(frame2, text=error, fg="red", font=("Arial", 20))
        error_el.pack()
        box.forget()
        box = Entry(root, width=10, font=("Arial", 15), state=DISABLED)
        box.place(x=320, y=80)
        submit_el.forget()
        submit_el = Button(root, text="Guess!!!", state=DISABLED)
        submit_el.place(x=450, y=80)
        playsound("Data/lose.wav", False)
    if correct_count >= len(word):
        error = "You win!!! Congratulations!"
        display = word
        display_el.forget()
        display_el = Label(frame1, text=display, font=("Arial", 25))
        display_el.pack()
        error_el.forget()
        error_el = Label(frame2, text=error, fg="green", font=("Arial", 20))
        error_el.pack()
        box.forget()
        box = Entry(root, width=10, font=("Arial", 15), state=DISABLED)
        box.place(x=320, y=80)
        submit_el.forget()
        submit_el = Button(root, text="Guess!!!", state=DISABLED)
        submit_el.place(x=450, y=80)
        playsound("Data/win.wav", False)


root = Tk()
root.title("Hang man")
root.geometry("550x200")
root.resizable(0, 0)
root.iconbitmap("Data/app.ico")

frame1 = LabelFrame(root, borderwidth=0)
frame1.pack()

display_el = Label(frame1, text=display, font=("Arial", 25), justify="center")
display_el.pack()

frame2 = LabelFrame(root, borderwidth=0)
frame2.pack()
error_el = Label(frame2, text=error, fg="orange")
error_el.pack()

chances_el = Label(root, text=f"You have {limit - len(wrong)} chances left")
chances_el.place(x=50, y=80)

box = Entry(root, width=10, font=("Arial", 15))
box.bind('<Return>', submit)
box.place(x=320, y=80)

submit_el = Button(root, text="Guess!!!", command=submit)
submit_el.place(x=450, y=80)

wrong_el = Label(root, text="  ".join(wrong), fg="red", font=("Arial", 10))
wrong_el.pack(pady=50)


root.mainloop()
