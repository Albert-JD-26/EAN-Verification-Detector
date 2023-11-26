from tkinter import *
import tkinter as tk
import sqlite3
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import pyautogui

# Get the screen resolution to fix with its screen size #
def get_display_resolution():
    width, height = pyautogui.size()
    return width, height


display_resolution = get_display_resolution()
print(f"Display Resolution: {display_resolution[0]}x{display_resolution[1]}")


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

cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                    user_name TEXT NOT NULL,
                    designation TEXT NOT NULL,
                    password TEXT NOT NULL
                    )''')


def check_company_name_not_null():
    connection = sqlite3.connect('EAN.db')
    check = connection.cursor()
    check.execute("SELECT * FROM details WHERE company_name IS NOT NULL")
    result = check.fetchall()
    connection.close()
    return len(result) > 0

# With user credentials user can logged into the software ↓ #


def login_account():
    u_name = username_entry2.get()
    password = password_entry2.get()
    designation = user_designation.get()
    print(u_name, password, designation)

    def check_user_name_not_null():
        connection = sqlite3.connect('EAN.db')
        check = connection.cursor()
        check.execute("SELECT * FROM users WHERE user_name IS NOT NULL")
        result = check.fetchall()
        connection.close()
        return len(result) > 0

    def is_admin(u_name, password):
        connection = sqlite3.connect('EAN.db')
        a_cursor = connection.cursor()
        a_cursor.execute("SELECT designation FROM users WHERE user_name=? AND password=?", (u_name, password))
        result = a_cursor.fetchone()
        connection.close()
        return result and result[0] == 'admin'

    def is_user(u_name, password):
        connection = sqlite3.connect('EAN.db')
        u_cursor = connection.cursor()
        u_cursor.execute("SELECT designation FROM users WHERE user_name=? AND password=?", (u_name, password))
        result = u_cursor.fetchone()
        connection.close()
        return result and result[0] == 'employee'

    def admin_portal(u_name, password):

        # In this function by if condition users can be classified whether admin or employee #
        # If condition for admin #
        if is_admin(u_name, password):
            print('Hello admin')

            def create_user():
                admin_panel.destroy()

                def create_user_key():
                    users_name = name_user.get()
                    users_password = password_set.get()

                    connection = sqlite3.connect('EAN.db')
                    u_connection = connection.cursor()
                    u_connection.execute("INSERT INTO users (user_name,designation, password) VALUES (?, 'employee', ?)",
                                         (users_name, users_password))
                    connection.commit()
                    u_connection.close()
                    connection.close()
                    c_user.destroy()
                    admin_portal(u_name, password)

                c_user = Tk()
                c_user.geometry('600x400')
                c_user.title('Create User')

                user_name = Label(c_user, text='User Name')
                user_name.pack()

                name_user = Entry(c_user)
                name_user.pack()

                set_password = Label(c_user, text='Password')
                set_password.pack()

                password_set = Entry(c_user)
                password_set.pack()

                create_button = Button(c_user, text='CREATE', command=create_user_key)
                create_button.pack()

                c_user.mainloop()

            admin_panel = Tk()
            admin_panel.geometry('500x200')
            admin_panel.title('ADMIN PANEL')
            cre_user = Button(admin_panel, text='Create user', command=create_user)
            cre_user.pack()
            admin_panel.mainloop()

        # Elif condition for employee #
        elif is_user(u_name, password):
            print('Hello User')

            user_panel = Tk()
            user_panel.geometry('500x200')
            user_panel.title('USER PANEL')

        else:
            print('Invalid credentials or you do not have access to the admin portal.')
            messagebox.showerror('Invalid Credentials', f'Username or password is wrong')

    if check_user_name_not_null():
        if display_resolution[0] == 1920 and display_resolution[1] == 1080:
            log.destroy()
            admin_portal(u_name, password)
            print('laptop')

        elif display_resolution[0] == 800 and display_resolution[1] == 600:
            log.destroy()
            admin_portal(u_name, password)
            print('pc')

    else:
        print("Create an account please!!!")

        def create_btn():
            user_name = name_us.get()
            desig = des.get()
            passwords = passw.get()

            connection = sqlite3.connect('EAN.db')
            cur = connection.cursor()

            cur.execute("INSERT INTO users (user_name, designation, password) VALUES (?, ?, ?)", (user_name, desig, passwords))

            connection.commit()
            cur.close()
            connection.close()
            messagebox.showinfo('SUCCESS', f'User {user_name} Created Successfully')
            user_tab.destroy()

        user_tab = Tk()
        user_tab.geometry("600x400")
        user_tab.title("User details")

        label = tk.Label(user_tab, text="Create User", font=('Arial', 20, 'bold'), )
        label.place(x=200, y=40)

        us_name = tk.Label(user_tab, text="User Name", font=('Arial', 15), )
        us_name.place(x=100, y=120)

        name_us = Entry(user_tab)
        name_us.place(x=330, y=120)

        designation = tk.Label(user_tab, text="Designation", font=('Arial', 15))
        designation.place(x=100, y=160)

        des = Entry(user_tab)
        des.place(x=330, y=160)

        set_pass = tk.Label(user_tab, text="Set password", font=('Arial', 15))
        set_pass.place(x=100, y=200)

        passw = Entry(user_tab)
        passw.place(x=330, y=200)

        create = tk.Button(user_tab, text='Create', font=('Arial', 15, 'bold'), command=create_btn)
        create.place(x=250, y=240)


# Login box is created with company name. ↓ #

def login():

    global log
    connect = sqlite3.connect('EAN.db')

    to_connect_name = connect.cursor()
    to_connect_location = connect.cursor()

    to_connect_name.execute("SELECT company_name FROM details")
    to_connect_location.execute("SELECT location FROM details")

    company_names = to_connect_name.fetchall()
    company_names_str = "\n".join([name[0] for name in company_names])
    comp_name = company_names_str.upper()

    company_location = to_connect_location.fetchall()
    company_location_str = "\n".join([name[0] for name in company_location])
    location_company = company_location_str.upper()

    log = Tk()
    log.geometry("900x430")
    log.resizable(0, 0)
    log.config(bg='#f0f0f0')
    log.title(f"{comp_name} LOGIN")

    font1 = ('Helvetica', 20, 'bold')
    font2 = ('MS Serif', 15 )
    font3 = ('Kozuka Gothic Pro B', 10, 'italic')

    frame1 = Frame(log, bg='#f0f0f0', width=470, height=360)
    frame1.place(x=250, y=20)

    login_label2 = Label(frame1, font=font1, text=f'{comp_name} LOGIN', fg='black', bg='#f0f0f0')
    login_label2.place(x=180, y=2)

    to_connect_name.execute("SELECT Images FROM details")
    image_data = to_connect_name.fetchone()[0]

    from io import BytesIO
    image_stream = BytesIO(image_data)

    original_img = Image.open(image_stream)
    desired_width = 300
    desired_height = 300
    resized_img = original_img.resize((desired_width, desired_height), Image.LANCZOS)
    img = ImageTk.PhotoImage(resized_img)

    label = Label(log, image=img)
    label.place(x=65, y=65)

    username_label = Label(frame1, text="USERNAME", fg='black', bg='#f0f0f0', font=('poppins', 10,'bold'))
    username_label.place(x=180, y=80)

    global username_entry2
    username_entry2 = Entry(frame1, font=font2, bg='#fff')
    username_entry2.place(x=180, y=110)

    design_label = Label(frame1, text="DESIGNATION", fg='black', bg='#f0f0f0',font=('poppins', 10,'bold'))
    design_label.place(x=180, y=150)

    global user_designation
    user_designation = Entry(frame1, font=font2, bg='#fff')
    user_designation.place(x=180, y=180)

    password_label = Label(frame1, text="PASSWORD", fg='black', bg='#f0f0f0', font=('poppins', 10,'bold'))
    password_label.place(x=180, y=220)

    global password_entry2
    password_entry2 = Entry(frame1, font=font2, bg='#fff')
    password_entry2.place(x=180, y=250)

    login_button2 = Button(frame1, font=font2, fg='#fff', bg='#001220', text='LOGIN', command=login_account)
    login_button2.place(x=260, y=310)

    company_name_display = Label(log, text=f'{comp_name}', font=font3)
    company_name_display.place(x=770, y=370)

    company_location =  Label(log, text=f'{location_company}', font=font3)
    company_location.place(x=770, y=390)

    log.mainloop()


if check_company_name_not_null():
    print(f"Entry with company  exists.")
    login()


# If no one is worked on this application then else condition works. ↓ #


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


