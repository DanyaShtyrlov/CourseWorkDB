from tkinter import *
from tkinter import ttk
from sqlite3 import *

window = Tk()#Основное окно

connection = connect('C:/Users/Даниил/Desktop/Курсовая работа/Тесты/CorseWorkDB.db')

cursor = connection.cursor()

main_listbox = Listbox(window, width=100)
main_listbox.pack(side=LEFT, pady=20, padx=20, fill=Y)

def refresh_main_listbox():
    main_listbox.delete(0, END)
    cursor.execute('SELECT * FROM Students')
    students = cursor.fetchall()
    for i in students:
        main_listbox.insert(END, i)

def main_window():#Основные параметры окна
    window.title("Успеваемость учащихся")
    window.geometry("1280x720")
    window.resizable(False, False)
    window.attributes("-toolwindow", True)

def add_student_to_db_window():
    
    def add_student_to_db_table():
        one_student_data = [entry_name.get(), entry_date.get(), entry_class.get()]
        print(one_student_data)
        cursor.execute("""
            INSERT INTO Students
            ('Full_name', 'Birth_date', 'Study_class')   
            VALUES
            (?, ?, ?)""", one_student_data)
        connection.commit()
        
    
    add_window = Tk()
    add_window.geometry("640x480")
    add_window.resizable(False, False)

    entry_name = ttk.Entry(add_window)
    entry_date = ttk.Entry(add_window)
    entry_class = ttk.Entry(add_window)
    entry_name.pack(anchor=NW, padx=20)
    entry_date.pack(anchor=N, padx=20)
    entry_class.pack(anchor=NE, padx=20)

    ttk.Button(add_window, text="Добавить", command=add_student_to_db_table).pack(anchor=SE, pady=20, padx=20)
    

    add_window.mainloop()

add_button = ttk.Button(window,text="Добавить ученика", command=add_student_to_db_window)
add_button.pack(side=RIGHT, padx=20, pady=20,)

refresh_button = ttk.Button(window, text="Обновить", command=refresh_main_listbox)
refresh_button.pack(side=RIGHT, padx=20,pady=20)


main_window()
window.mainloop()
connection.close()