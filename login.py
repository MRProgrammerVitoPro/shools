import tkinter as tk
from tkinter import messagebox
import mysql.connector
import os
import runpy

# Подключение к базе данных
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="shool_25"
)

# Создание курсора для выполнения запроса
mycursor = mydb.cursor()

# Функция для проверки акторизации
def Login():
    username = username_entry.get()
    password = password_entry.get()

    sql = "SELECT * FROM users WHERE `username` = %s AND `userpassword` = %s"
    val = (username, password)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()

    if result:
        root.destroy()
        filename = "C:\\Users\\MrProgrammist\\Desktop\\Shools\\index.py"
        runpy.run_path(filename)
    else:
        messagebox.showerror("Error", "Такого пользователя не существует")

# Функция для регистрации нового пользователя
def Register():
    username = username_entry.get()
    password = password_entry.get()

    sql = "INSERT INTO `users` (`username`, `userpassword`) VALUES (%s, %s)"
    val = (username, password)
    mycursor.execute(sql, val)
    mydb.commit()
    messagebox.showinfo("Registration", "Вы зарегистрировались !")

root = tk.Tk()
root.title("Авторизация")
root.geometry("350x200")

username_label = tk.Label(root, text="Username:")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

password_label = tk.Label(root, text="Password:")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

login_batton = tk.Button(root, text="Login", command=Login)
login_batton.pack()

register_button = tk.Button(root, text="Register", command=Register)
register_button.pack()

root.mainloop()

