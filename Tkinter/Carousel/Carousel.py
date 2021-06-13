from tkinter import *
from PIL import ImageTk, Image
import os
import random

string = ""


root = Tk()
root.title("Carousel")
root.geometry("680x360")
root.resizable(0, 0)

img_name = os.listdir("images")
for i in range(len(img_name)):
    img_name[i] = "images/" + str(img_name[i])

random.shuffle(img_name)

img_list = []
for name in img_name:
    temp = Image.open(name)
    temp = temp.resize((600, 330), Image.ANTIALIAS)
    temp = ImageTk.PhotoImage(temp)
    img_list.append(temp)

current = 0


def back():
    global img_list, current, my_label, progress
    my_label.grid_forget()
    current -= 1
    if current < 0:
        current = len(img_list) - 1
    my_label = Label(image=img_list[current])
    my_label.grid(row=0, column=1)
    progress.grid_forget()
    progress = Label(root, text=f"Image {current + 1} of {len(img_list)}")
    progress.grid(row=1, column=1)


def forward():
    global img_list, current, my_label, progress
    my_label.grid_forget()
    current += 1
    if current >= len(img_list):
        current = 0
    my_label = Label(image=img_list[current])
    my_label.grid(row=0, column=1)
    progress.grid_forget()
    progress = Label(root, text=f"Image {current + 1} of {len(img_list)}")
    progress.grid(row=1, column=1)


my_label = Label(image=img_list[current])
my_label.grid(row=0, column=1)

btn_back = Button(root, text="<", fg="black", bg="#f0f0f0", padx=12, pady=150, borderwidth=0, command=back)
btn_forward = Button(root, text=">", fg="black", bg="#f0f0f0", padx=12, pady=150, borderwidth=0, command=forward)

btn_back.grid(row=0, column=0)
btn_forward.grid(row=0, column=2)

progress = Label(root, text=f"Image {current + 1} of {len(img_list)}")
progress.grid(row=1, column=1)

root.mainloop()
