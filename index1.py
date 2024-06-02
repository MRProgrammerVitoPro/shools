import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import mysql.connector

def quit_app():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()

def open_classes():
    # Implement logic to open classes
    pass

def open_teachers():
    pass

def open_materials():
    # Implement logic to open materials
    pass

def display_students():
    global root, tree
    # Подключение к базе данных
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="shool_25"  # Название вашей базы данных
    )

    # Создание курсора для выполнения запросов
    mycursor = mydb.cursor()

    # Выполнение запроса для получения списка всех студентов с их классами
    query = """
        SELECT students.name, students.fname, students.contakt, class.class_name
        FROM students
        JOIN class ON students.class_id = class.id
        """
    mycursor.execute(query)

    # Получение результатов запроса
    students = mycursor.fetchall()

    # Создание и настройка окна tkinter
    root = tk.Tk()
    root.title("Student List")
    root.geometry("1000x800")

    # Создание меню
    menu_bar = tk.Menu(root)

    # Меню "Классы"
    classes_menu = tk.Menu(menu_bar, tearoff=0)
    classes_menu.add_command(label="Open Classes", command=open_classes)
    menu_bar.add_cascade(label="Classes", menu=classes_menu)

    # Меню "Учителя"
    teachers_menu = tk.Menu(menu_bar, tearoff=0)
    teachers_menu.add_command(label="Open Teachers", command=open_teachers)
    menu_bar.add_cascade(label="Teachers", menu=teachers_menu)

    # Меню "Материалы"
    materials_menu = tk.Menu(menu_bar, tearoff=0)
    materials_menu.add_command(label="Open Materials", command=open_materials)
    menu_bar.add_cascade(label="Materials", menu=materials_menu)

    # Меню "Выход"
    menu_bar.add_command(label="Quit", command=quit_app)

    # Установка созданного меню как основного меню окна
    root.config(menu=menu_bar)

    # Создание таблицы для отображения студентов
    tree = ttk.Treeview(root)

    # Определение заголовков столбцов таблицы
    tree["columns"] = ("FirstName", "LastName", "Contacts", "Class")

    # Настройка ширины столбцов
    tree.column("#0", width=0, stretch=tk.NO)  # Пустой столбец
    tree.column("FirstName", anchor=tk.W, width=100)
    tree.column("LastName", anchor=tk.W, width=100)
    tree.column("Contacts", anchor=tk.W, width=150)
    tree.column("Class", anchor=tk.W, width=100)

    # Настройка заголовков столбцов
    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("FirstName", text="Имя", anchor=tk.W)
    tree.heading("LastName", text="Фамилия", anchor=tk.W)
    tree.heading("Contacts", text="Контакты", anchor=tk.W)
    tree.heading("Class", text="Класс", anchor=tk.W)

    # Добавление данных в таблицу
    for student in students:
        tree.insert("", tk.END, values=student)

    tree.pack(expand=tk.YES, fill=tk.BOTH)

    # Добавление кнопок
    add_button = tk.Button(root, text="Добавить", command=add_student)
    add_button.pack(side=tk.LEFT, padx=(20, 10), pady=(10, 20))

    edit_button = tk.Button(root, text="Изменить", command=edit_student)
    edit_button.pack(side=tk.LEFT, padx=10, pady=(10, 20))

    delete_button = tk.Button(root, text="Удалить", command=delete_student)
    delete_button.pack(side=tk.LEFT, padx=10, pady=(10, 20))

    root.mainloop()

def add_student():
    name = simpledialog.askstring("Добавить студента", "Введите имя студента:")
    fname = simpledialog.askstring("Добавить студента", "Введите фамилию студента:")
    contakt = simpledialog.askstring("Добавить студента", "Введите контакты студента:")
    class_name = simpledialog.askstring("Добавить студента", "Введите класс студента:")
    
    if name and fname and contakt and class_name:
        # Подключение к базе данных
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="shool_25"
        )
        mycursor = mydb.cursor()

        # Проверка существования класса в базе данных
        class_query = "SELECT id FROM class WHERE class_name = %s"
        mycursor.execute(class_query, (class_name,))
        class_result = mycursor.fetchone()

        if class_result:
            # Если класс существует, добавляем студента
            query = "INSERT INTO students (name, fname, contakt, class_id) VALUES (%s, %s, %s, %s)"
            mycursor.execute(query, (name, fname, contakt, class_result[0]))
            mydb.commit()
            # Обновление отображения
            tree.insert("", tk.END, values=(name, fname, contakt, class_name))
        else:
            messagebox.showerror("Ошибка", "Класс '{}' не существует.".format(class_name))

def edit_student():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите студента для изменения.")
        return
    
    current_values = tree.item(selected_item, 'value')
    name = simpledialog.askstring("Изменить студента", "Введите новое имя студента: ", initialvalue=current_values[0])
    fname = simpledialog.askstring("Изменить студента", "Введите фамилию имя студента: ", initialvalue=current_values[1])
    contakt = simpledialog.askstring("Изменить студента", "Введите новый контакт студента: ", initialvalue=current_values[2])
    class_name = simpledialog.askstring("Изменить студента", "Введите новый класс студента: ", initialvalue=current_values[3])

    if name and fname and contakt and class_name:
        # Подключение к базе данных  Маша привет
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="shool_25"
        )
        mycursor = mydb.cursor()

        query = """
            UPDATE students SET name = %s, fname = %s, contakt = %s, class_id = (SELECT id FROM class WHERE class_name = %s)
            WHERE name = %s AND fname = %s AND contakt = %s AND class_id = (SELECT id FROM class WHERE class_name = %s)
        """
        mycursor.execute(query, (name, fname, contakt, class_name, current_values[0], current_values[1], current_values[2], current_values[3]))
        mydb.commit()
        #Обновление отображения
        tree.item(selected_item, values=(name, fname, contakt, class_name))


def delete_student():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите студента для удаления.")
        return
    
    current_values = tree.item(selected_item, "value")
    # Подключение к базе данных
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="shool_25"
    )
    mycursor = mydb.cursor()
    query = "DELETE FROM students WHERE name = %s AND fname = %s AND contakt = %s AND class_id = (SELECT id FROM class WHERE class_name = %s)"
    mycursor.execute(query, (current_values[0], current_values[1], current_values[2], current_values[3]))
    mydb.commit()
    tree.delete(selected_item)

display_students()