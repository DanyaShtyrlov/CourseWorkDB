from tkinter import *
from tkinter import ttk, filedialog
from sqlite3 import *
from tkinter.messagebox import askyesno, showinfo
from time import localtime
from tkcalendar import Calendar

global database_viewport

connection = connect('CourseWorkFullDB.db')
cursor = connection.cursor()

main_window = Tk()
main_window.title("Успеваемость учащихся")
main_window.geometry("1280x450")
main_window.resizable(False, False)

viewport_columns = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")

database_viewport = ttk.Treeview(main_window, show="headings", columns=viewport_columns, height=19)

database_viewport.column("1", stretch=NO, width=40)
database_viewport.column("3", stretch=NO, width=100)
database_viewport.column("4", stretch=NO, width=100)
database_viewport.column("5", stretch=NO, width=70)
database_viewport.column("6", stretch=NO, width=70)
database_viewport.column("7", stretch=NO, width=70)
database_viewport.column("8", stretch=NO, width=70)
database_viewport.column("9", stretch=NO, width=70)
database_viewport.column("10", stretch=NO, width=70)

database_viewport.grid(row=1, columnspan=4, sticky=NW, padx=20, pady=10)

def add_current_date():
    month = localtime().tm_mon
    if len(str(month)) == 1:
        month = "0" + str(month)
    day = localtime().tm_mday
    if len(str(day)) == 1:
        day = "0" + str(day)
    cursor.execute("SELECT name FROM pragma_table_info('Grade') ORDER BY cid DESC LIMIT 1")
    if cursor.fetchall()[0][0] != "{0}.{1}".format(day, month):
        cursor.execute("ALTER TABLE Grade ADD '{0}.{1}' INTEGER".format(day, month))
        connection.commit()
    else:
        pass

def write_to_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)

def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data

def add_photo_to_chosen():
    photo_path = filedialog.askopenfile()
    photo = convert_to_binary_data(photo_path.name)
    cursor.execute("UPDATE {0} SET {0}_photo = ? WHERE ID = {2}".format(choice_table_combobox.get(), photo, database_viewport.item(database_viewport.focus())["values"][0]), [photo])
    connection.commit()

def get_image_from_database(id):
        cursor.execute("SELECT {0}_photo FROM {0} WHERE ID = {1}".format(choice_table_combobox.get(),id))
        photo = cursor.fetchall()
        photo = photo[0][0]
        write_to_file(photo, "Photo/photo.png")

def show_image_in_canvas():
    global database_image
    try:
        current_id = database_viewport.item(database_viewport.focus())["values"][0]
        get_image_from_database(current_id)
        database_image = PhotoImage(file="Photo/photo.png")
        database_image_canvas.create_image(10, 10, anchor=NW, image=database_image)
    except:
        showinfo(title="Ошибка", message="Нет фото!")

def grade_complition():
    students = []
    subjects = []
    info = []
    cursor.execute("SELECT Full_name FROM Student")
    students_fetch = cursor.fetchall()
    cursor.execute("SELECT Subject_name FROM Subject")
    subjects_fetch = cursor.fetchall()
    for i in range(len(students_fetch)):
        students.append(students_fetch[i][0])
    for i in range(len(subjects_fetch)):
        subjects.append(subjects_fetch[i][0])
    info_students = cursor.execute("SELECT Student_name FROM Grade").fetchall()
    for i in range(len(info_students)):
        info.append(info_students[i][0])
    for i in students:
        for j in subjects:
                if not (i in info):
                    cursor.execute("""
                    INSERT INTO Grade
                    ('Student_name', 'Subject_name')
                    VALUES
                    (?, ?)
                    """, [i, j])
                    connection.commit()
                else:
                    pass

def add_student_data_to_database():

    def add_entry_to_student_table():
        ask_if_sure = askyesno(title="Подтверждение", message="Хотите  добавить?")
        if ask_if_sure:
            one_student_data = [name_entry.get(), date_entry.get(), class_entry.get()]
            cursor.execute("""
                INSERT INTO Student
                ('Full_name', 'Birth_date', 'Study_class')   
                VALUES
                (?, ?, ?)""", one_student_data)
            connection.commit()
            showinfo("Результат", "Элемент добавлен!")
            add_window.destroy()
        else:
            showinfo("Результат", "Операция отменена!")

    add_window = Tk()
    add_window.title("Добавить ученика")
    add_window.geometry("500x100")
    add_window.resizable(False, False)

    name_label = ttk.Label(add_window, text="ФИО", width=30)
    name_label.grid(row=0, column=0, sticky=NW, padx=20)
    date_label = ttk.Label(add_window, text="Дата рождения")
    date_label.grid(row=0, column=1, sticky=N)
    class_label = ttk.Label(add_window, text="Класс, группа")
    class_label.grid(row=0, column=2, sticky=NE, padx=25)

    name_entry = ttk.Entry(add_window, width=30)
    name_entry.grid(row=1, column=0, padx=5)
    date_entry = ttk.Entry(add_window)
    date_entry.grid(row=1, column=1, padx=5)
    class_entry = ttk.Entry(add_window)
    class_entry.grid(row=1, column=2, padx=5)

    add_button = ttk.Button(add_window, text="Добавить", command=add_entry_to_student_table)
    add_button.grid(row=2, column=2, pady=10)

def add_teacher_to_database():

    def add_entry_to_teacher_tabel():
        ask_if_sure = askyesno(title="Подтверждение", message="Хотите  добавить?")
        if ask_if_sure:
            one_teacher_data = [name_entry.get(), graduation_entry.get(), period_entry.get()]
            cursor.execute("""
                INSERT INTO Teacher
                ('Full_name', 'Graduation', 'Work_period')   
                VALUES
                (?, ?, ?)""", one_teacher_data)
            connection.commit()
            showinfo("Результат", "Элемент добавлен!")
            add_teacher_window.destroy()
        else:
            showinfo("Результат", "Операция отменена!")

    add_teacher_window = Tk()
    add_teacher_window.title("Добавить преподавателя")
    add_teacher_window.geometry("500x100")
    add_teacher_window.resizable(False, False)

    name_label = ttk.Label(add_teacher_window, text="ФИО")
    name_label.grid(row=0, column=0, sticky=NW, padx=75)
    graduation_label = ttk.Label(add_teacher_window, text="Ученая степень")
    graduation_label.grid(row=0, column=1, sticky=N, padx=30)
    period_label = ttk.Label(add_teacher_window, text="Стаж")
    period_label.grid(row=0, column=2, sticky=NE, padx=50)

    name_entry = ttk.Entry(add_teacher_window, width=30)
    name_entry.grid(row=1, column=0, padx=5)
    graduation_entry = ttk.Entry(add_teacher_window)
    graduation_entry.grid(row=1, column=1, padx=5)
    period_entry = ttk.Entry(add_teacher_window)
    period_entry.grid(row=1, column=2, padx=5)

    add_button = ttk.Button(add_teacher_window, text="Добавить", command=add_entry_to_teacher_tabel)
    add_button.grid(row=2, column=2, pady=10)

def add_subject_to_database():
    def add_entry_to_subject_tabel():
        ask_if_sure = askyesno(title="Подтверждение", message="Хотите  добавить?")
        if ask_if_sure:
            one_subject_data = [name_entry.get(), teacher_entry.get(), hours_entry.get()]
            cursor.execute("""
                INSERT INTO Subject
                ('Subject_name', 'Teacher_name', 'Study_hours')   
                VALUES
                (?, ?, ?)""", one_subject_data)
            connection.commit()
            showinfo("Результат", "Элемент добавлен!")
            add_subject_window.destroy()
        else:
            showinfo("Результат", "Операция отменена!")
    add_subject_window = Tk()
    add_subject_window.title("Добавить предмет")
    add_subject_window.geometry("600x100")
    add_subject_window.resizable(False, False)

    name_label = ttk.Label(add_subject_window, text="Название")
    name_label.grid(row=0, column=0, sticky=NW, padx=5)
    teacher_label = ttk.Label(add_subject_window, text="Имя преподавателя")
    teacher_label.grid(row=0, column=1, sticky=N, padx=0)
    hours_label = ttk.Label(add_subject_window, text="Академические часы")
    hours_label.grid(row=0, column=2, sticky=NE, padx=50)

    name_entry = ttk.Entry(add_subject_window, width=30)
    name_entry.grid(row=1, column=0, padx=5)
    values = []
    cursor.execute("SELECT Full_name FROM Teacher")
    teacher_data = cursor.fetchall()
    for i in range(len(teacher_data)):
        values.append(teacher_data[i][0])  
    teacher_entry = ttk.Combobox(add_subject_window, width=30, values=values)
    teacher_entry.grid(row=1, column=1, padx=5)
    hours_entry = ttk.Entry(add_subject_window, width=25)
    hours_entry.grid(row=1, column=2, padx=5)
    add_button = ttk.Button(add_subject_window, text="Добавить", command=add_entry_to_subject_tabel)
    add_button.grid(row=2, column=1, pady=10)

def clear_colums_name():
    for columns in database_viewport['columns']:
        database_viewport.heading(columns, text='')

def refresh_viewport_data():
    cursor.execute("SELECT * FROM {0}".format(choice_table_combobox.get()))
    rows = cursor.fetchall()
    match choice_table_combobox.get():
        case "Student":
            clear_colums_name()
            database_viewport.heading("1", text="№")
            database_viewport.heading("2", text="ФИО") 
            database_viewport.heading("3", text="Дата рождения")
            database_viewport.heading("4", text="Класс, группа")
            cursor.execute("SELECT ID, Full_name, Birth_date, Study_class FROM {0}".format(choice_table_combobox.get()))
            rows = cursor.fetchall()
        case "Teacher":
            clear_colums_name()
            database_viewport.heading("1", text="№")
            database_viewport.heading("2", text="ФИО") 
            database_viewport.heading("3", text="Ученая степень")
            database_viewport.heading("4", text="Стаж")
            cursor.execute("SELECT ID, Full_name, Graduation, Work_period FROM {0}".format(choice_table_combobox.get()))
            rows = cursor.fetchall()
        case "Grade": 
            clear_colums_name()
            database_viewport.heading("1", text="№")
            database_viewport.heading("2", text="ФИО") 
            database_viewport.heading("3", text="Предмет")
            database_viewport.heading("4", text=cursor.description[-7][0])
            database_viewport.heading("5", text=cursor.description[-6][0])
            database_viewport.heading("6", text=cursor.description[-5][0])
            database_viewport.heading("7", text=cursor.description[-4][0])
            database_viewport.heading("8", text=cursor.description[-3][0])
            database_viewport.heading("9", text=cursor.description[-2][0])
            database_viewport.heading("10", text=cursor.description[-1][0])
            cursor.execute("SELECT * FROM {0}".format(choice_table_combobox.get()))
            rows  = cursor.fetchall()
            rows_prepared = []
            for i in rows:
                rows_prepared.append(list(i))
            for i in range(len(rows_prepared)):
                for j in range(len(rows_prepared[i])):
                    if rows_prepared[i][j] == None:
                        rows_prepared[i][j] = " "
                while len(rows_prepared[i]) != 10:
                    rows_prepared[i].pop(3)
            
            rows = rows_prepared

        case "Subject":
            clear_colums_name()
            database_viewport.heading("1", text="№")
            database_viewport.heading("2", text="Название") 
            database_viewport.heading("3", text="Имя преподавателя")
            database_viewport.heading("4", text="Часы обучения")
            cursor.execute("SELECT * FROM {0}".format(choice_table_combobox.get()))
            rows = cursor.fetchall()

    grade_complition()

    

    for i in database_viewport.get_children():
        database_viewport.delete(i)

    for row in rows:
        database_viewport.insert("", END, values=row)

def mark_set():
    students = []
    subjects = []
    marks = [1, 2, 3, 4, 5]
    mark_window = Tk()
    mark_window.title("Выставление оценки")
    mark_window.geometry("550x300")
    mark_window.resizable(False,  False)

    date = Calendar(mark_window)
    date.grid(row=0, column=1)

    cursor.execute("SELECT * FROM Grade")
    all_data = cursor.fetchall()
    for i in range(len(all_data)):
            if all_data[i][1] in students:
                pass
            else:
                students.append(all_data[i][1])
    for i in range(len(all_data)):
            if all_data[i][2] in subjects:
                pass
            else:
                subjects.append(all_data[i][2])
    choice_student = ttk.Combobox(mark_window,values=students)
    choice_student.grid(row=1, column=0, pady=20, padx=5)
    choice_subject = ttk.Combobox(mark_window, values=subjects)
    choice_subject.grid(row=1, column=1)
    choice_mark = ttk.Combobox(mark_window, values=marks)
    choice_mark.grid(row=1, column=2)

    def set_mark_at_date():
        mark_date = date.get_date()[0:5]
        cursor.execute("UPDATE Grade SET '{0}' = ? WHERE Student_name = ? AND Subject_name = ?".format(mark_date), [choice_mark.get(), choice_student.get(), choice_subject.get()])

    get_date_button = ttk.Button(mark_window, text="Поставить", command=set_mark_at_date)
    get_date_button.grid(row=2, column=1)

    mark_window.mainloop()

def show_all_marks():
    show_window = Tk()
    show_window.geometry("1280x720")
    show_window.resizable(False, False)
    viewport_listbox = Listbox(show_window, height=720, width=1280)
    viewport_listbox.pack()
    cursor.execute("SELECT * FROM Grade")
    data = cursor.fetchall()
    for i in data:
        viewport_listbox.insert(END, i)
    show_window.mainloop()

def search_viewport():
    def search():
        childs = []
        childs_final = []
        for child in database_viewport.get_children():
            viewport_child = database_viewport.item(child)["values"]
            childs.append(viewport_child)
        
        for i in range(len(childs)):
            for j in range(3):
                childs[i][0] = str(childs[i][0])
                if what_search.get().lower() in childs[i][j].lower():
                    childs_final.append(childs[i])

        for i in database_viewport.get_children():
            database_viewport.delete(i)
        for row in childs_final:
            database_viewport.insert("", END, values=row)

    search_window = Tk()
    search_window.title("Поиск")
    search_window.geometry("300x100")
    search_window.resizable(False, False)
    what_search = ttk.Entry(search_window)
    search_button = ttk.Button(search_window, text="Поиск", command=search)
    what_search.pack(anchor=CENTER)
    search_button.pack(anchor=CENTER)

    search_window.mainloop()

tables = ["Student", "Teacher", "Subject", "Grade"]
take_table = StringVar(value=tables[3])
choice_table_combobox = ttk.Combobox(textvariable=take_table, values=tables)
choice_table_combobox.grid(row=0, column=0, sticky=W, padx=20)

main_menu = Menu()
add_menu = Menu(tearoff=0)
show_menu = Menu(tearoff=0)
search_menu = Menu(tearoff=0)

add_menu.add_cascade(label="Добавить ученика", command=add_student_data_to_database)
add_menu.add_cascade(label="Добавить преподавателя", command=add_teacher_to_database)
add_menu.add_cascade(label="Добавить предмет", command=add_subject_to_database)
add_menu.add_cascade(label="Добавить фото", command=add_photo_to_chosen)
show_menu.add_cascade(label="Показать все оценки", command=show_all_marks)
main_menu.add_cascade(label="Добавит...", menu=add_menu)
main_menu.add_cascade(label="Показать...", menu=show_menu)
main_menu.add_cascade(label="Поиск", command=search_viewport)
main_menu.add_cascade(label="Обновить", command=refresh_viewport_data)

refresh_button = ttk.Button(main_window, text="Обновить", command=refresh_viewport_data)
refresh_button.grid(row=0, column=1)
image_button = ttk.Button(main_window, text="Показать", command=show_image_in_canvas)
image_button.grid(row=0, column=2, sticky=N)
mark_set_button = ttk.Button(main_window, text="Выставить оценку", command=mark_set)
mark_set_button.grid(row=0, column=3)

database_image_canvas = Canvas(main_window, bg="white", width=400, height=400)
database_image_canvas.grid(row=1, column=4, sticky=N, pady=10)

add_current_date()

main_window.config(menu=main_menu)
main_window.mainloop()
connection.close()