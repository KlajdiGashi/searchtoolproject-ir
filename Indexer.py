import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

file_path = ''

def read_file():
    global file_path
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

def search_word(index):
    search_term = search_entry.get().strip().lower()
    if search_term:
        if search_term in index:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f'{search_term}: {index[search_term]}\n')
        else:
            messagebox.showinfo("Word Not Found", f"The word '{search_term}' does not exist in the file.")
            add_word(search_term, index)

def add_word(word, index):
    global file_path
    response = messagebox.askyesno("Word Not Found", f"The word '{word}' does not exist. Would you like to add it?")
    if response:
        with open(file_path, 'a') as file:
            file.write(f'\n{word}')
        messagebox.showinfo("Word Added", f"The word '{word}' has been added to the file.")
        refresh_index()

def refresh_index():
    global index
    index = build_index(split_text(read_file()))
    output_index(index)

app = tk.Tk()
app.title("Inverted Index Application")
app.configure(bg="black")

file_label = tk.Label(app, text="Select File:", bg="black", fg="white")
result_label = tk.Label(app, text="Result:", bg="black", fg="white")

file_label.pack()
file_button = tk.Button(app, text="Open File", command=refresh_index, bg="black", fg="white")
file_button.pack()

search_label = tk.Label(app, text="Search Word:", bg="black", fg="white")
search_label.pack()

search_entry = tk.Entry(app, bg="white", fg="black")
search_entry.pack()

search_button = tk.Button(app, text="Search", command=lambda: search_word(index), bg="black", fg="white")
search_button.pack()

result_label.pack()
result_text = tk.Text(app, width=50, height=20, bg="black", fg="white")
result_text.pack()

index = {}

app.mainloop()
