import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image
import os


def jpg_to_pdf(img_list, output_pdf):
    first_img = Image.open(img_list[0]).convert("RGB")
    rest = img_list[1:]
    converted = []
    for i in rest:
        converted.append(Image.open(i).convert("RGB"))
    first_img.save(output_pdf, save_all=True, append_images=converted)


def select_files():
    global images_name, images_error

    images_name = filedialog.askopenfilenames(title='Open images', filetypes=(
        ("Image file", ("*.jpg", "*.png", "*.jpeg", "*.jfif")),
        ("All file", "*.*")
    ))

    images_name = list(filter(lambda x: x.endswith(".jpg") or x.endswith(".png") or x.endswith(".jpeg") or x.endswith(".jfif"), images_name))

    if images_name:
        images_entry.delete(0, tk.END)
        images_entry.insert(0, f"{len(images_name)} images opened")
        images_error.config(text="")


def ask_save_file():
    global pdf_name, pdf_error
    pdf_name = filedialog.asksaveasfilename(filetypes=(("PDF file", "*.pdf"), ("All file", "*.*")), defaultextension=".pdf")

    if not pdf_name.endswith(".pdf"):
        return

    if pdf_name:
        pdf_entry.delete(0, tk.END)
        pdf_entry.insert(0, pdf_name)
        pdf_error.config(text="")


def main():
    global images_name, pdf_name, images_error, pdf_error, open_file_label
    if not images_name:
        images_error.config(text="Image files not selected")
        return
    else:
        images_error.config(text="")

    if not pdf_name:
        pdf_error.config(text="Destination PDF file not selected")
        return
    else:
        pdf_error.config(text="")

    try:
        jpg_to_pdf(images_name, pdf_name)
        fisnished_label.config(text="Images successfully converted to PDF")
        open_file_label.grid(row=4, column=0, columnspan=2)
        open_file_label.bind("<Enter>", enter)
        open_file_label.bind("<Leave>", leave)
        open_file_label.bind("<Button-1>", open_destination_file)
        convert_btn.config(state=tk.DISABLED)

    except Exception as bug:
        print(bug)


def open_destination_file(e):
    global pdf_name
    path = os.path.realpath(pdf_name)
    os.startfile(path)


def enter(e):
    global open_file_label
    open_file_label.config(foreground="#0B5ED7")


def leave(e):
    global open_file_label
    open_file_label.config(foreground="#0D6EFD")


# Define
images_name = None
pdf_name = None

# Root
root = tk.Tk()
root.title("Convert images to PDF")
root.geometry("300x220")
root.resizable(0, 0)

# Frames
frame_1 = ttk.Frame(root, width=400, padding=5)
frame_2 = ttk.Frame(root, width=400, padding=5)

frame_1.grid(row=0, column=0)
frame_2.grid(row=1, column=0)

frame_1.pack_propagate(0)
frame_2.pack_propagate(0)

# Images Section
images_label = ttk.Label(frame_1, text="Select images")
images_label.grid(row=0, column=0, sticky="w", padx=10)

images_entry = ttk.Entry(frame_1, width=40)
images_entry.grid(row=1, column=0, padx=5)

images_btn = ttk.Button(frame_1, text="...", width=3, command=select_files)
images_btn.grid(row=1, column=1)

images_error = ttk.Label(frame_1, text="", foreground="red")
images_error.grid(row=2, column=0, columnspan=2)

# PDF Section
pdf_label = ttk.Label(frame_2, text="Select destination")
pdf_label.grid(row=0, column=0, sticky="w", padx=10)

pdf_entry = ttk.Entry(frame_2, width=40)
pdf_entry.grid(row=1, column=0, padx=5)


pdf_btn = ttk.Button(frame_2, text="...", width=3, command=ask_save_file)
pdf_btn.grid(row=1, column=1)

pdf_error = ttk.Label(frame_2, text="", foreground="red")
pdf_error.grid(row=2, column=0, columnspan=2)

# Convert button
convert_btn = ttk.Button(text="Convert", command=main)
convert_btn.grid(row=2, column=0, columnspan=2)

# Finished Label
fisnished_label = ttk.Label(text="", foreground="green")
fisnished_label.grid(row=3, column=0, columnspan=2)

# Open file Label
open_file_label = ttk.Label(text="Open destination file", foreground="#0D6EFD", font="Verdana 8 underline", cursor="hand2")

# Mainloop
root.mainloop()
