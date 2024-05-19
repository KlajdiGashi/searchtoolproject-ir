import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import math

file_path = ''
num_documents = 0
document_frequencies = {}

def read_file():
    global file_path, num_documents
    file_path = filedialog.askopenfilename()
    if file_path:
        num_documents += 1
        with open(file_path, 'r') as file:
            text = file.read()
        return text
    else:
        messagebox.showwarning("Warning", "No file selected.")

def split_text(text):   
    words = text.split()
    return words

def build_index(words):
    global document_frequencies
    index = {}
    for i, word in enumerate(words):
        word = word.lower()
        if word in index:
            index[word].append(i)
        else:
            index[word] = [i]
            if word in document_frequencies:
                document_frequencies[word] += 1
            else:
                document_frequencies[word] = 1
    return index

def calculate_tf(words):
    tf = {}
    total_words = len(words)
    for word in words:
        word = word.lower()
        if word in tf:
            tf[word] += 1
        else:
            tf[word] = 1
    for word, count in tf.items():
        tf[word] = count / total_words
    return tf

def calculate_idf():
    idf = {}
    for word, df in document_frequencies.items():
        idf[word] = math.log(num_documents / df)
    return idf

def calculate_tfidf(tf, idf):
    tfidf = {}
    for word, tf_value in tf.items():
        tfidf[word] = tf_value * idf.get(word, 0)
    return tfidf

def output_index(index, tfidf, tf, idf):
    result_text.delete(1.0, tk.END)
    for word, positions in index.items():
        tf_value = tf.get(word, 0)
        idf_value = idf.get(word, 0)
        tfidf_value = tfidf.get(word, 0)
        result_text.insert(tk.END, f'{word}: {positions} (TF: {tf_value:.4f}, IDF: {idf_value:.4f}, TF-IDF: {tfidf_value:.4f})\n')

def search_word(index):
    global tfidf, tf, idf
    search_term = search_entry.get().strip().lower()
    if not search_term:  # If search term is empty
        result_text.delete(1.0, tk.END)
        for word, positions in index.items():
            tf_value = tf.get(word, 0)
            idf_value = idf.get(word, 0)
            tfidf_value = tfidf.get(word, 0)
            result_text.insert(tk.END, f'{word}: {positions} (TF: {tf_value:.4f}, IDF: {idf_value:.4f}, TF-IDF: {tfidf_value:.4f})\n')
    elif search_term in index:
        result_text.delete(1.0, tk.END)
        tf_value = tf.get(search_term, 0)
        idf_value = idf.get(search_term, 0)
        tfidf_value = tfidf.get(search_term, 0)
        result_text.insert(tk.END, f'{search_term}: {index[search_term]} (TF: {tf_value:.4f}, IDF: {idf_value:.4f}, TF-IDF: {tfidf_value:.4f})\n')
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
    global index, num_documents, document_frequencies, tfidf, tf, idf
    text = read_file()
    if text:
        words = split_text(text)
        new_index = build_index(words)
        
        # Find the maximum position in the existing index
        max_position = max([position for positions in index.values() for position in positions], default=-1) + 1
        
        for word, positions in new_index.items():
            if word in index:
                # Update each position individually to reflect its correct position in the overall document corpus
                updated_positions = [position + max_position for position in positions]
                index[word].extend(updated_positions)
            else:
                # Update positions with the offset and add the word to the index
                index[word] = [position + max_position for position in positions]
                if word in document_frequencies:
                    document_frequencies[word] += 1
                else:
                    document_frequencies[word] = 1
        
        num_documents += 1
        tf = calculate_tf(words)
        idf = calculate_idf()
        tfidf = calculate_tfidf(tf, idf)
        output_index(index, tfidf, tf, idf)

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
tfidf = {}
tf = {}
idf = {}

app.mainloop()
