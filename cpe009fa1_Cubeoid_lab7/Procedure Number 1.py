import tkinter as tk
from tkinter import messagebox
import math

# Functions for calculation
def addition():
    validate_input()
    result_value = float(entry1.get()) + float(entry2.get())
    result.set(result_value)
    history_list.insert(tk.END, f"{entry1.get()} + {entry2.get()} = {result_value}")

def subtract():
    validate_input()
    result_value = float(entry1.get()) - float(entry2.get())
    result.set(result_value)
    history_list.insert(tk.END, f"{entry1.get()} - {entry2.get()} = {result_value}")

def multiply():
    validate_input()
    result_value = float(entry1.get()) * float(entry2.get())
    result.set(result_value)
    history_list.insert(tk.END, f"{entry1.get()} * {entry2.get()} = {result_value}")

def divide():
    validate_input()
    try:
        result_value = float(entry1.get()) / float(entry2.get())
        result.set(result_value)
        history_list.insert(tk.END, f"{entry1.get()} / {entry2.get()} = {result_value}")
    except ZeroDivisionError:
        result.set("Error! Division by zero.")
        messagebox.showerror("Error", "Cannot divide by zero.")

def square_root():
    validate_input(entry1)
    value = float(entry1.get())
    result_value = math.sqrt(value)
    result.set(result_value)
    history_list.insert(tk.END, f"√{value} = {result_value}")

def power():
    validate_input()
    base = float(entry1.get())
    exponent = float(entry2.get())
    result_value = math.pow(base, exponent)
    result.set(result_value)
    history_list.insert(tk.END, f"{base}^{exponent} = {result_value}")

def clear():
    entry1.delete(0, tk.END)
    entry2.delete(0, tk.END)
    result.set("")
    history_list.delete(0, tk.END)

def validate_input(entry=None):
    if entry:
        try:
            float(entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number.")
            entry.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Simple Calculator")
root.geometry("500x400")  # Set a larger window size

# Create StringVar to hold the result
result = tk.StringVar()

# Create the layout with padding
tk.Label(root, text="Enter first number:").grid(row=0, column=0)
entry1 = tk.Entry(root)
entry1.grid(row=0, column=1)

tk.Label(root, text="Enter second number:").grid(row=1, column=0)
entry2 = tk.Entry(root)
entry2.grid(row=1, column=1)

# Operation Buttons
buttons = [
    ("Addition", addition),
    ("Subtract", subtract),
    ("Multiply", multiply),
    ("Divide", divide),
    ("√", square_root),
    ("**", power),
    ("Clear", clear)
]

for i, (text, command) in enumerate(buttons):
    tk.Button(root, text=text, command=command, bg="DarkSlateGray1",
              font=("Purisa", 5)).grid(row=2 + i // 2, column=i % 2)

# Result Display
tk.Label(root, text="Result:").grid(row=6, column=0)
tk.Entry(root, textvariable=result, state="readonly").grid(row=6, column=1)

# History Listbox
tk.Label(root, text="History:").grid(row=7, column=0)
history_list = tk.Listbox(root, width=50, height=5)
history_list.grid(row=10, column=1)

# Styling
for widget in root.winfo_children():
    if isinstance(widget, tk.Button):
        widget.config(font=("Arial", 12), padx=10, pady=5)
    elif isinstance(widget, tk.Label):
        widget.config(font=("Arial", 12))
    elif isinstance(widget, tk.Entry):
        widget.config(font=("Arial", 12), width=20)

root.mainloop()
