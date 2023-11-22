from tkinter import *
import tkinter as tk
import sqlite3
from tkinter import filedialog
from tkinter import messagebox

conn = sqlite3.connect('EAN.db')
cursor = conn.cursor()
data = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS details (
                    manager_name TEXT NOT NULL,
                    company_name TEXT NOT NULL,
                    location TEXT NOT NULL,
                    year TEXT NOT NULL,
                    Image BLOB
                )''')

def check_company_exists(company_name):
    connection = sqlite3.connect('EAN.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM details WHERE company_name=?", (company_name,))
    result = cursor.fetchone()
    connection.close()
    return result is not None

company_name_to_check = "de moza"

if check_company_exists(company_name_to_check):
    print(f"Entry with company name '{company_name_to_check}' exists.")
    w = Tk()
    w.geometry("600x400")
    w.title("Company details")

    def filedialogs():
        global get_image
        get_image = filedialog.askopenfilenames(title="SELECT IMAGE",  filetypes=(("png", "*.png"), ("jpg", "*.jpg"), ("All files", "*.*")))

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
                f"INSERT INTO details (manager_name, company_name, location, year, Image) VALUES (?, ?, ?, ?, ?)", (manager_name, company_name, company_location, started_year, insert_photo))

        connection.commit()
        cur.close()
        connection.close()

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

else:
    print(f"Entry with company name '{company_name_to_check}' does not exist.")
    messagebox.showwarning("Alert", "Please fill company details.")


