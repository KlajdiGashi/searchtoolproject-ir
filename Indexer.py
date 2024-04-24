import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def read_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as file:
            text = file.read()
        return text
    else:
        messagebox.showwarning("Warning", "No file selected.")

def split_text(text):   
    words = text.split()
    return words

def build_index(words):
    index = {}
    for i, word in enumerate(words):
        word = word.lower()
        if word in index:
            index[word].append(i)
        else:
            index[word] = [i]
    return index

def output_index(index):
    result_text.delete(1.0, tk.END)
    for word, positions in index.items():
        result_text.insert(tk.END, f'{word}: {positions}\n')

# Create GUI
app = tk.Tk()
app.title("Inverted Index Application")

app.configure(bg="black")
file_label = tk.Label(app, text="Select File:", bg="black", fg="white")
result_label = tk.Label(app, text="Result:", bg="black", fg="white")

file_label.pack()
file_button = tk.Button(app, text="Open File", command=lambda: output_index(build_index(split_text(read_file()))), bg="black", fg="white")
file_button.pack()
result_label.pack()
result_text = tk.Text(app, width=50, height=20, bg="black", fg="white")
result_text.pack()

app.mainloop()
