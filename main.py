# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import json
from datetime import datetime
import logging
import functions as fun
import constants as c

# ---------- Window Setup ----------
root = tk.Tk()
root.title("Note Organizer")
root.geometry("450x450")
root.resizable(False, False)
root.configure(bg="#222222")

style = ttk.Style()
style.theme_use("clam")  # Use a nice modern theme
style.configure(
    "TButton",
    padding=6,
    relief="flat",
    background=c.button_color,
    foreground=c.button_text_color,
    font=c.button_font,
)
style.configure(
    "Danger.TButton",
    background=c.danger_color,
    foreground=c.button_text_color,
    font=c.button_font,
)
style.configure("TEntry", padding=5, relief="sunken", font=c.entry_font)

# ---------- Load Notes ----------
with open(c.filename, "r") as file:
    note = json.load(file)


# ---------- Functions ----------
def on_add_note():
    get_note_data_from_display = display.get()
    fun.insert_note(get_note_data_from_display)
    display.delete(0, tk.END)


def on_read_note():
    text_box.delete("1.0", tk.END)
    for dic in fun.note:
        text_box.insert(
            "1.0", f"{dic["id"]}: {dic['text']}\n"
        )  # FIXED: use single quotes inside f-string
    if len(fun.note) == 0:
        text_box.insert("1.0", "<Note is empty>")
    display.delete(0, tk.END)


def on_delete_note():
    try:
        delete_data_from_display = int(display.get())
        fun.delete_note(delete_data_from_display)
        display.delete(0, tk.END)
    except ValueError:
        logging.error("Not a valid ID")


# ---------- Widgets ----------
display = ttk.Entry(root, width=40)
display.pack(pady=20)

# Buttons
add_note = ttk.Button(root, text="➕ Add Note", command=on_add_note)
add_note.pack(pady=5)

read_note = ttk.Button(root, text="📗 Read Note", command=on_read_note)
read_note.pack(pady=5)

delete_note = ttk.Button(
    root, text="❌ Delete Note", style="Danger.TButton", command=on_delete_note
)
delete_note.pack(pady=5)

# Text box
text_box = tk.Text(root, font=c.text_font, bg=c.text_color, fg=c.text_foreground)
text_box.pack()
# ---------- Loop ----------
root.mainloop()
