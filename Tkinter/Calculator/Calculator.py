from tkinter import *

root = Tk()
root.title("Calculator")
root.resizable(0, 0)
root.iconbitmap("app.ico")

display = Entry(root, width=12, font=('Arial', 15), bg="#f0f0f0", borderwidth=0, justify="right")
display.grid(row=0, column=0, columnspan=3, padx=10)
display.insert(END, 0)

real_display = "0"
num1 = 0
num2 = 0
current_operator = ""
operator_choosed = False


def number_clicked(number):
    global real_display
    if not(display.get().isnumeric()):
        display.delete(0, END)
        display.insert(END, real_display)
    else:
        real_display = display.get()
    if len(display.get()) < 10:
        if display.get() == "0" or not(display.get().isnumeric()):
            display.delete(0, END)
            real_display = ""
        display.insert(END, number)
        real_display += str(number)


def operator_clicked(operator):
    global num1, num2, real_display, current_operator, operator_choosed
    operator_choosed = True
    current_operator = operator
    if not(display.get().isnumeric()):
        display.delete(0, END)
        display.insert(END, real_display)
    else:
        real_display = display.get()
    if display.get() != "0" and display.get().isnumeric():
        num1 = float(display.get())
    display.delete(0, END)
    display.insert(0, 0)
    real_display = "0"


def clear():
    global num1, num2, real_display, current_operator, operator_choosed
    operator_choosed = False
    display.delete(0, END)
    display.insert(END, 0)
    num1 = 0
    num2 = 0
    current_operator = ""
    real_display = "0"


def backspace():
    global real_display
    if not(display.get().isnumeric()):
        display.delete(0, END)
        display.insert(END, real_display)
    else:
        real_display = display.get()
    temp = display.get()
    temp = temp[:len(temp) - 1]
    if temp == "":
        temp = "0"
    display.delete(0, END)
    display.insert(0, temp)
    real_display = temp


def equal():
    global num1, num2, real_display, current_operator, operator_choosed
    if not(display.get().isnumeric()):
        display.delete(0, END)
        display.insert(END, real_display)
    else:
        real_display = display.get()
        if operator_choosed:
            num2 = float(display.get())

    try:
        if current_operator == "+":
            num1 = num1 + num2
        elif current_operator == "-":
            num1 = num1 - num2
        elif current_operator == "*":
            num1 = num1 * num2
        elif current_operator == "/":
            num1 = num1 / num2

        if num1 % 1 == 0:
            num1 = int(num1)
        else:
            tmp = int("1" + (10 - len(str(round(num1)))) * "0")
            num1 = round(num1 * tmp) / tmp
        if len(str(num1)) > 11:
            print(1 / 0)
        real_display = num1
    except Exception:
        num1 = 0
        real_display = "MATH ERROR"
    display.delete(0, END)
    display.insert(END, real_display)
    operator_choosed = False


btn_divide = Button(root, text="÷", padx=20, pady=15, command=lambda: operator_clicked("/"))


btn1 = Button(root, text="1", padx=20, pady=15, command=lambda: number_clicked(1))
btn2 = Button(root, text="2", padx=20, pady=15, command=lambda: number_clicked(2))
btn3 = Button(root, text="3", padx=20, pady=15, command=lambda: number_clicked(3))
btn_multiple = Button(root, text="×", padx=20, pady=15, command=lambda: operator_clicked("*"))


btn4 = Button(root, text="4", padx=20, pady=15, command=lambda: number_clicked(4))
btn5 = Button(root, text="5", padx=20, pady=15, command=lambda: number_clicked(5))
btn6 = Button(root, text="6", padx=20, pady=15, command=lambda: number_clicked(6))
btn_minus = Button(root, text="-", padx=21, pady=15, command=lambda: operator_clicked("-"))


btn7 = Button(root, text="7", padx=20, pady=15, command=lambda: number_clicked(7))
btn8 = Button(root, text="8", padx=20, pady=15, command=lambda: number_clicked(8))
btn9 = Button(root, text="9", padx=20, pady=15, command=lambda: number_clicked(9))
btn_plus = Button(root, text="+", padx=20, pady=15, command=lambda: operator_clicked("+"))


btn0 = Button(root, text="0", padx=20, pady=15, command=lambda: number_clicked(0))
btn_clear = Button(root, text="CE", padx=16, pady=15, command=clear)
btn_backspace = Button(root, text="←", padx=18, pady=15, command=backspace)
btn_equal = Button(root, text="=", padx=20, pady=15, command=equal)

btn_divide.grid(row=0, column=3)

btn7.grid(row=1, column=0)
btn8.grid(row=1, column=1)
btn9.grid(row=1, column=2)
btn_multiple.grid(row=1, column=3)

btn4.grid(row=2, column=0)
btn5.grid(row=2, column=1)
btn6.grid(row=2, column=2)
btn_minus.grid(row=2, column=3)


btn1.grid(row=3, column=0)
btn2.grid(row=3, column=1)
btn3.grid(row=3, column=2)
btn_plus.grid(row=3, column=3)

btn0.grid(row=4, column=0)
btn_clear.grid(row=4, column=1)
btn_backspace.grid(row=4, column=2)
btn_equal.grid(row=4, column=3)


root.mainloop()
