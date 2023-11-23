from tkinter import *
import tkinter as tk
import sqlite3
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk


conn = sqlite3.connect('EAN.db')
cursor = conn.cursor()
data = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS details (
                    manager_name TEXT NOT NULL,
                    company_name TEXT NOT NULL,
                    location TEXT NOT NULL,
                    year TEXT NOT NULL,
                    Images BLOB
                )''')


def check_company_name_not_null():
    connection = sqlite3.connect('EAN.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM details WHERE company_name IS NOT NULL")
    result = cursor.fetchall()
    connection.close()
    return len(result) > 0


def login():
    connect = sqlite3.connect('EAN.db')
    to_connect = connect.cursor()
    to_connect.execute("SELECT company_name FROM details")
    company_names = to_connect.fetchall()
    company_names_str = "\n".join([name[0] for name in company_names])
    comp_name = company_names_str.upper()
    log = Tk()
    log.geometry("700x360")
    log.resizable(0, 0)
    log.config(bg='#f0f0f0')
    log.title(f"{comp_name} LOGIN")

    font1 = ('Helvetica', 25, 'bold')
    font2 = ('Arial', 15, 'bold')

    frame1 = Frame(log, bg='#f0f0f0', width=470, height=360)
    frame1.place(x=250, y=20)

    login_label2 = Label(frame1, font=font1, text=f'{comp_name} LOGIN', fg='black', bg='#f0f0f0')
    login_label2.place(x=180, y=20)

    original_img = Image.open("demoza.png")
    desired_width = 300
    desired_height = 300
    resized_img = original_img.resize((desired_width, desired_height), Image.LANCZOS)
    img = ImageTk.PhotoImage(resized_img)
    label = Label(log, image=img)
    label.place(x=20, y=20)

    username_label = Label(frame1, text="USERNAME", fg='black', bg='#f0f0f0', font='poppins, 10')
    username_label.place(x=180, y=80)

    username_entry2 = Entry(frame1, font=font2, bg='#fff')
    username_entry2.place(x=180, y=100)

    password_label = Label(frame1, text="PASSWORD", fg='black', bg='#f0f0f0', font='poppins, 10')
    password_label.place(x=180, y=150)

    password_entry2 = Entry(frame1, font=font2, bg='#fff')
    password_entry2.place(x=180, y=170)

    login_button2 = Button(frame1, font=font2, fg='#fff', bg='#001220', text='LOGIN')
    login_button2.place(x=230, y=220)

    log.mainloop()




if check_company_name_not_null():
    print(f"Entry with company  exists.")
    login()

else:
    print(f"Entry with company does not exist.")
    w = Tk()
    w.geometry("600x400")
    w.title("Company details")

    def filedialogs():
        global get_image
        get_image = filedialog.askopenfilenames(title="SELECT IMAGE", filetypes=(("png", "*.png"), ("jpg", "*.jpg"), ("All files", "*.*")))


    def conver_image_into_binary(filename):
        with open(filename, 'rb') as file:
            photo_image = file.read()
        return photo_image


    def insert_image():
        image_db = sqlite3.connect('EAN.db')
        data = image_db.cursor()

        for image_path in get_image:
            insert_photo = conver_image_into_binary(image_path)
            data.execute("INSERT INTO details VALUES (?)", (insert_photo,))

        image_db.commit()
        image_db.close()


    def submit_btn():
        manager_name = man_name.get()
        company_name = name.get()
        company_location = location.get()
        started_year = year.get()

        connection = sqlite3.connect('EAN.db')
        cur = connection.cursor()
        for image_path in get_image:
            insert_photo = conver_image_into_binary(image_path)
            cur.execute(
                f"INSERT INTO details (manager_name, company_name, location, year, Images) VALUES (?, ?, ?, ?, ?)",
                (manager_name, company_name, company_location, started_year, insert_photo))

        connection.commit()
        cur.close()
        connection.close()
        messagebox.showinfo('SUCCESS', f'{company_name} Details Created Successfully')
        w.destroy()
        login()


    m_name = tk.Label(w, text="Manager Name", font=('Arial', 15, 'bold'), )
    m_name.place(x=100, y=80)

    man_name = tk.Entry()
    man_name.place(x=330, y=80)

    c_name = tk.Label(w, text="Company Name", font=('Arial', 15, 'bold'))
    c_name.place(x=100, y=120)

    name = tk.Entry()
    name.place(x=330, y=120)

    c_location = tk.Label(w, text="Company Location", font=('Arial', 15, 'bold'))
    c_location.place(x=100, y=160)

    location = tk.Entry()
    location.place(x=330, y=160)

    c_year = tk.Label(w, text="Started Year", font=('Arial', 15, 'bold'))
    c_year.place(x=100, y=200)

    year = tk.Entry()
    year.place(x=330, y=200)

    c_image = tk.Label(w, text="Upload Image", font=('Arial', 15, 'bold'))
    c_image.place(x=100, y=240)

    s_image = tk.Button(w, text="Select Image", font=('Arial', 15, 'bold'), command=filedialogs)
    s_image.place(x=330, y=240)

    submit = tk.Button(w, text='Submit', font=('Arial', 15, 'bold'), command=submit_btn)
    submit.place(x=250, y=310)

    w.mainloop()


