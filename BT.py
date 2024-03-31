import re
import tkinter as tk

def generate_playfair_matrix(key):
    key = re.sub(r'[^A-Za-z]', '', key.upper())
    key = key.replace("J", "I")
    key = "".join(dict.fromkeys(key))
    
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    for char in key:
        alphabet = alphabet.replace(char, "")
    key += alphabet
    
    matrix = [key[i:i+5] for i in range(0, 25, 5)]
    return matrix

def find_char_positions(matrix, char):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j

def encrypt(plain_text, key):
    matrix = generate_playfair_matrix(key)
    plain_text = re.sub(r'[^A-Za-z]', '', plain_text.upper())
    plain_text = re.sub(r'((.)(?=\2))', r'\1X', plain_text)
    if len(plain_text) % 2 != 0:
        plain_text += 'X'
    
    encrypted_text = ''
    for i in range(0, len(plain_text), 2):
        char1 = plain_text[i]
        char2 = plain_text[i+1]
        row1, col1 = find_char_positions(matrix, char1)
        row2, col2 = find_char_positions(matrix, char2)
        if row1 == row2:
            encrypted_text += matrix[row1][(col1 + 1) % 5]
            encrypted_text += matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            encrypted_text += matrix[(row1 + 1) % 5][col1]
            encrypted_text += matrix[(row2 + 1) % 5][col2]
        else:
            encrypted_text += matrix[row1][col2]
            encrypted_text += matrix[row2][col1]
    return encrypted_text

def on_encrypt():
    key = key_entry.get()
    plain_text = plain_text_entry.get().strip()
    if not key or not plain_text:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Vui lòng nhập khóa và văn bản cần mã hóa.")
        return
    encrypted_text = encrypt(plain_text, key)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, encrypted_text)

# Tạo cửa sổ
window = tk.Tk()
window.title("Ứng dụng mã hóa Playfair")
window.geometry("400x350")

# Tạo các widget
header_label = tk.Label(window, text="Mã hóa theo mã Playfair", font=("Arial", 16))
header_label.pack(pady=10)

key_label = tk.Label(window, text="Khóa:", font=("Arial", 12))
key_label.pack()

key_entry = tk.Entry(window, font=("Arial", 12))
key_entry.pack()

plain_text_label = tk.Label(window, text="Văn bản:", font=("Arial", 12))
plain_text_label.pack()

plain_text_entry = tk.Entry(window, font=("Arial", 12))
plain_text_entry.pack()

encrypt_button = tk.Button(window, text="Mã hóa", command=on_encrypt, font=("Arial", 12), bg="blue", fg="white")
encrypt_button.pack(pady=10)

result_label = tk.Label(window, text="Kết quả:", font=("Arial", 12))
result_label.pack()

result_text = tk.Text(window, height=3, width=30, font=("Arial", 12))
result_text.pack()

# Chạy ứng dụng
window.mainloop()
