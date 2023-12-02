from tkinter import *
import tkinter as tk
import sqlite3
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import pyautogui
from io import BytesIO
import pandas as pd
import os
import cv2
from datetime import datetime
import winsound
import numpy as np
from pyzbar.pyzbar import decode

camera_list = [f'Camera {i}' for i in range(10) if cv2.VideoCapture(i).read()[0]]
print(f'Detected cameras: {", ".join(camera_list)}')
Number_of_camera = len(camera_list)
print("Total number of cameras:", Number_of_camera)

try:
    if not os.path.exists('DATABASES'):
        os.makedirs('DATABASES')
except OSError:
    print('Error: Creating directory of DATABASES')

current_date = datetime.now().strftime("%d-%m-%Y")

for recording in range(Number_of_camera):
    print(recording)


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


def start_recording1():
    global recording, start_time1, writer1, current_date, starting_time1, started_time1, elapsed_time_str1, first_detection_times1, camera1, data1, qr_codes_array1, video_name1
    recording = True
    start_time1 = None
    data1 = ' '
    qr_codes_array1 = []
    first_detection_times1 = {}
    live_time1 = datetime.now()
    started_time1 = live_time1.strftime("%I:%M %p")
    camera1 = "CAM1"
    time_1 = time1.get()
    video_name1 = f'{camera1}-{time_1}'
    num1.config(text=0)
    strt1.config(text=0)
    drn1.config(text=0)
    print("Camera1 Recording")
    writer1 = cv2.VideoWriter(f"./{current_date}/{video_name1}.mp4", fourcc1, 23.0,
                              (640, 480))


def stop_recording1():
    global recording, writer1, start_time1, elapsed_time_str1, code_array1
    print("Camera1 Stopped")
    if writer1 is not None:
        writer1.release()

    elapsed_time1 = datetime.now() - start_time1
    elapsed_time_str1 = str(elapsed_time1).split(".")[0]
    dur1 = elapsed_time_str1
    code_array1 = len(qr_codes_array1)
    print("no in 1 camera", code_array1)

    if len(first_detection_times1) == 0:
        print("no DATA DETECTED")

    else:
        strt1.config(text=started_time1)
        drn1.config(text=dur1)
        num1.config(text=code_array1)
        # dispatch1(video_name1, elapsed_time_str1, len(qr_codes_array1), present_date,  present_time, username)
        rec1_data = sqlite3.connect('./DATABASES/recording.db')
        df = pd.read_sql_query(
            f"SELECT * from record1data WHERE VIDEO_NAME = '{video_name1}'", rec1_data)
        df.to_excel(f"./{current_date}/{video_name1}.xlsx", index=False)
        rec1_data.close()


def process_frame():
    global recording, start_time1, writer1, end_time1, present_date, present_time, elapsed_time_str1, data1
    # CAM CCTV
    ret1, frame1 = cap1.read()
    cv2.putText(frame1, "CAM1", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    if ret1:
        if recording:
            qr_codes1 = decode(frame1)
            for qr_code1 in qr_codes1:
                data1 = qr_code1.data.decode('utf-8')
                if data1 not in first_detection_times1:
                    first_detection_times1[data1] = cap1.get(cv2.CAP_PROP_POS_MSEC) / 1000
                    qr_codes_array1.append(data1)

                    frequency = 1000
                    duration = 500
                    winsound.Beep(frequency, duration)
                    present_date = datetime.now().strftime('%Y-%m-%d')
                    present_time = datetime.now().strftime('%I:%M %p')

                    print(
                        f"QR code {data1} detected for the first time at{elapsed_time_str1} on {present_date}-{present_time} in {video_name1}")
                    # scan1(data1, elapsed_time_str1, present_date, present_time, video_name1,  username)

                for qr_code1 in qr_codes1:
                    (x, y, w, h) = qr_code1.rect
                    cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    pts2 = qr_code1.rect
                    cv2.putText(frame1, data1, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                0.9, (255, 0, 255), 1)

                if len(qr_codes_array1) == 0:
                    print("No QR codes detected!!!!!")

            if start_time1 is None:
                start_time1 = datetime.now()

            elapsed_time1 = datetime.now() - start_time1
            elapsed_time_str1 = str(elapsed_time1).split(".")[0]
            cv2.putText(frame1, "CAM1", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255), 1)
            cv2.putText(frame1, f"START TIME:  {started_time1}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255), 1)
            cv2.putText(frame1, f"DURATION:    {elapsed_time_str1}", (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 0, 255), 1)
            cv2.putText(frame1, f"NO OF DATA:  {len(qr_codes_array1)}", (10, 120),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 255), 1)
            cv2.putText(frame1, f"LAST DATA:   {data1}", (10, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255),
                        1)
            writer1.write(frame1)
        cv2.imshow("Recording Camera 1", frame1)

    if not ret1:
        blank_frame1 = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(blank_frame1, "CAM1 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 255),
                    1)
        cv2.imshow("Recording Camera CAM1", blank_frame1)

    controller.after(1, process_frame)


def close_window():
    cap1.release()
    cv2.destroyAllWindows()
    controller.destroy()


def camera():
    global cap1, fourcc1
    cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    fourcc1 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')


def record():
    # Detect the number of camera connected to system #
    if Number_of_camera == 1:
        print("One camera is connected to system")

        global controller, time1, strt1, drn1, num1

        camera()

        controller = tk.Tk()
        controller.geometry("300x300")
        controller.title("VIDEO CONTROLLER")
        controller.resizable(0, 0)

        ################### CAM1
        cam1 = tk.Label(controller, text="CAMERA 1", fg='blue')
        cam1.place(x=20, y=60)
        get_time1 = tk.Label(controller, text='Enter Time')
        get_time1.place(x=60, y=90)
        time1 = tk.Entry(controller)
        time1.place(x=160, y=90)
        start_button_1 = tk.Button(controller, text="START CAM1", command=start_recording1)
        start_button_1.place(x=60, y=120)
        stop_button_1 = tk.Button(controller, text="STOP CAM1", command=stop_recording1)
        stop_button_1.place(x=160, y=120)

        ####################    CAM1
        Start_timing1 = tk.Label(controller, text="START TIME")
        Start_timing1.place(x=60, y=150)
        strt1 = tk.Label(controller, text="0:0")
        strt1.place(x=210, y=150)
        Duration_time1 = tk.Label(controller, text="DURATION")
        Duration_time1.place(x=60, y=180)
        drn1 = tk.Label(controller, text="0:0:0")
        drn1.place(x=210, y=180)
        NOD1 = tk.Label(controller, text="NO OF CAPTURED DATA")
        NOD1.place(x=60, y=210)
        num1 = tk.Label(controller, text="0")
        num1.place(x=210, y=210)

        close_button = tk.Button(controller, text="Close", command=close_window)
        close_button.place(x=130, y=250)

        controller.after(1, process_frame)
        controller.mainloop()



    elif Number_of_camera == 2:
        print("Two camera is connected to system")


def display_summary():
    frame = tk.Frame(main_frame)
    frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(frame)
    canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    output_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=output_frame, anchor=tk.NW)

    p1 = tk.Label(output_frame, text="VIDEO NAME", font="time 15 bold")
    p1.grid(row=1, column=0, padx=10, pady=10)

    p4 = tk.Label(output_frame, text="DURATION", font="time 15 bold")
    p4.grid(row=1, column=1, padx=10, pady=10)

    p2 = tk.Label(output_frame, text="NO OF DATA", font="time 15 bold")
    p2.grid(row=1, column=2, padx=10, pady=10)

    p3 = tk.Label(output_frame, text="DATE", font="time 15 bold")
    p3.grid(row=1, column=3, padx=10, pady=10)

    p5 = tk.Label(output_frame, text="TIME", font="time 15 bold")
    p5.grid(row=1, column=4, padx=10, pady=10)

    p6 = tk.Label(output_frame, text="USERNAME", font="time 15 bold")
    p6.grid(row=1, column=5, padx=10, pady=10)

    conn = sqlite3.connect("DATABASES/recording.db")
    c = conn.cursor()
    c.execute("SELECT * FROM recordsummary")
    r = c.fetchall()

    num = 2
    for i in r:
        video_name = tk.Label(output_frame, text=i[0], font="time 11 bold", fg="black")
        video_name.grid(row=num, column=0, padx=10, pady=5)

        duration = tk.Label(output_frame, text=i[1], font="time 11 bold", fg="blue")
        duration.grid(row=num, column=1, padx=10, pady=5)

        no_od_data = tk.Label(output_frame, text=i[2], font="time 11 bold", fg="red")
        no_od_data.grid(row=num, column=2, padx=10, pady=5)

        date = tk.Label(output_frame, text=i[3], font="time 11 bold", fg="green")
        date.grid(row=num, column=3, padx=10, pady=5)

        time = tk.Label(output_frame, text=i[4], font="time 11 bold", fg="pink")
        time.grid(row=num, column=4, padx=10, pady=5)

        username = tk.Label(output_frame, text=i[5], font="time 11 bold", fg="grey")
        username.grid(row=num, column=5, padx=10, pady=5)

        num = num + 1

    output_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.bind_all("<MouseWheel>",  lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))


def export_summary():

    conn = sqlite3.connect('DATABASES/recording.db')
    df = pd.read_sql_query("SELECT * from recordsummary", conn)
    df.to_excel(f"RECORDING SUMMARY.xlsx", index=False)
    conn.close()
    print("Data exported to Excel successfully.")
    messagebox.showinfo("Exported", "Overall data exported to Excel successfully.")


# With user credentials user can log into the software ↓ #


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
            admin_portal_1920x1080(u_name, password)

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

    def admin_portal_1920x1080(u_name, password):

        # In this function by if condition users can be classified whether admin or employee #
        # If condition for admin #
        if is_admin(u_name, password):
            print('Admin Panel')
            global admin_panel
            admin_panel = Tk()
            admin_panel.geometry("1920x1080")
            admin_panel.title('ADMIN PANEL')

            options_frame = tk.Frame(admin_panel, bg="#c3c3c3", highlightbackground='black', highlightthickness=2)
            options_frame.pack(side=tk.LEFT)
            options_frame.pack_propagate(False)
            options_frame.configure(width=210, height=1500)

            # BUTTONS
            general = tk.Label(options_frame, text="GENERAL", font=10, bg="#c3c3c3")
            general.place(x=50, y=20)

            rec_btn = tk.Button(options_frame, text="RECORD", font=('Bold', 15), fg='white', bd=0, bg='#4392fa',width=15,borderwidth=5, command=record)
            rec_btn.place(x=10, y=50)

            summary_btn = tk.Button(options_frame, text="DISPLAY \n SUMMARY", font=('Bold', 15), fg='white', bd=0,bg='#4392fa',width=15, borderwidth=5, command=display_summary)
            summary_btn.place(x=10, y=110)

            exp_rec_summary_bt = tk.Button(options_frame, text="EXPORT REC\n SUMMARY", font=('Bold', 15),fg='white', bd=0,bg='#4392fa',width=15, borderwidth=5, command=export_summary)
            exp_rec_summary_bt.place(x=10, y=195)

            options = tk.Label(options_frame, text="OPTIONS", font=15, bg="#c3c3c3")
            options.place(x=50, y=280)

            input_btn = tk.Button(options_frame, text="INPUT \n VIDEO", font=('Bold', 15), fg='white', bd=0,bg='#4392fa', width=15,borderwidth=5)
            input_btn.place(x=10, y=320)

            data_btn = tk.Button(options_frame, text="EXPORT\nCAPTURED\nDATA", font=('Bold', 15), fg='white', bd=0,bg='#4392fa',width=15, borderwidth=5)
            data_btn.place(x=10, y=400)

            exp_input_summary_bt = tk.Button(options_frame, text="EXPORT INPUT\n SUMMARY", font=('Bold', 15),fg='white', bd=0,bg='#4392fa',width=15, borderwidth=5)
            exp_input_summary_bt.place(x=10, y=505)

            download_btn = tk.Button(options_frame, text="DOWNLOAD \n CLIP", font=('Bold', 15), fg='white', bd=0,bg='#4392fa',width=15, borderwidth=5)
            download_btn.place(x=10, y=590)

            cre_user = Button(options_frame, text='CREATE USER', font=('Bold', 15), fg='white', bd=0,bg='#4392fa',width=15, borderwidth=5, command=create_user)
            cre_user.place(x=10, y=680)

            delete_db = tk.Button(options_frame, text="Delete DB", bg='red', fg='white')
            delete_db.place(x=60, y=750)

            # MAIN FRAME
            global main_frame
            main_frame = tk.Frame(admin_panel, highlightbackground='black', highlightthickness=2)
            main_frame.pack(side=tk.LEFT)
            main_frame.pack_propagate(False)
            main_frame.configure(height=1500, width=7100, bg='#2c2f33')

            admin_panel.mainloop()

        # Elif condition for employee #
        elif is_user(u_name, password):
            print('User Panel')

            user_panel = Tk()
            user_panel.geometry("1920x1080")
            user_panel.title('USER PANEL')
            connect = sqlite3.connect('EAN.db')
            to_connect_name = connect.cursor()
            to_connect_name.execute("SELECT Images FROM details")
            image_data = to_connect_name.fetchone()[0]

            image_stream = BytesIO(image_data)
            original_img = Image.open(image_stream)
            desired_width = 80
            desired_height = 80
            resized_img = original_img.resize((desired_width, desired_height), Image.LANCZOS)
            img = ImageTk.PhotoImage(resized_img)

            # OPTION FRAME
            options_frame = tk.Frame(user_panel, bg="#c3c3c3", highlightbackground='black', highlightthickness=2)
            options_frame.pack(side=tk.LEFT)
            options_frame.pack_propagate(False)
            options_frame.configure(width=210, height=1500)

            # BUTTONS
            general = tk.Label(options_frame, text="GENERAL", font=10, bg="#c3c3c3")
            general.place(x=50, y=150)

            rec_btn = tk.Button(options_frame, text="RECORD", font=('Bold', 15), fg='white', bd=0, bg='#4392fa', width=15, borderwidth=5)
            rec_btn.place(x=10, y=200)

            summary_btn = tk.Button(options_frame, text="DISPLAY \n SUMMARY", font=('Bold', 15), fg='white', bd=0, bg='#4392fa', width=15, borderwidth=5)
            summary_btn.place(x=10, y=270)

            exp_rec_summary_bt = tk.Button(options_frame, text="EXPORT REC\n SUMMARY", font=('Bold', 15), fg='white', bd=0, bg='#4392fa', width=15, borderwidth=5, command=export_summary)
            exp_rec_summary_bt.place(x=10, y=370)

            label = Label(options_frame, image=img)
            label.place(x=58, y=800)

            company_name_display = Label(options_frame, text=f'{comp_name}', font=('Kozuka Gothic Pro B', 10, 'italic'), bg="#c3c3c3")
            company_name_display.place(x=70, y=900)

            company_location = Label(options_frame, text=f'{location_company}', font=('Kozuka Gothic Pro B', 10, 'italic'), bg="#c3c3c3")
            company_location.place(x=70, y=920)

            # MAIN FRAME
            main_frame = tk.Frame(user_panel, highlightbackground='black', highlightthickness=2)
            main_frame.pack(side=tk.LEFT)
            main_frame.pack_propagate(False)
            main_frame.configure(height=1500, width=7100, bg='#2c2f33')

            user_panel.mainloop()

        else:
            print('Invalid credentials or you do not have access to the admin portal.')
            messagebox.showerror('Invalid Credentials', f'Username or password is wrong')

    def admin_portal_1280x720(u_name, password):

        # In this function by if condition users can be classified whether admin or employee #
        # If condition for admin #
        if is_admin(u_name, password):
            print('Admin Panel')
            global admin_panel

            admin_panel = Tk()
            admin_panel.geometry("1280x720")
            admin_panel.title('ADMIN PANEL')

            options_frame = tk.Frame(admin_panel, bg="#c3c3c3", highlightbackground='black', highlightthickness=2)
            options_frame.pack(side=tk.LEFT)
            options_frame.pack_propagate(False)
            options_frame.configure(width=210, height=1500)

            # BUTTONS
            general = tk.Label(options_frame, text="GENERAL", font=10, bg="#c3c3c3")
            general.place(x=50, y=15)

            rec_btn = tk.Button(options_frame, text="RECORD", font=('Bold', 13), fg='white', bd=0, bg='#4392fa',
                                width=15, borderwidth=5)
            rec_btn.place(x=23, y=45)

            summary_btn = tk.Button(options_frame, text="DISPLAY \n SUMMARY", font=('Bold', 13), fg='white', bd=0,
                                    bg='#4392fa', width=15, borderwidth=5, command=display_summary)
            summary_btn.place(x=23, y=100)

            exp_rec_summary_bt = tk.Button(options_frame, text="EXPORT REC\n SUMMARY", font=('Bold', 13), fg='white',
                                           bd=0, bg='#4392fa', width=15, borderwidth=5, command=export_summary)
            exp_rec_summary_bt.place(x=23, y=175)

            options = tk.Label(options_frame, text="OPTIONS", font=15, bg="#c3c3c3")
            options.place(x=50, y=245)

            input_btn = tk.Button(options_frame, text="INPUT \n VIDEO", font=('Bold', 13), fg='white', bd=0,
                                  bg='#4392fa', width=15, borderwidth=5)
            input_btn.place(x=23, y=280)

            data_btn = tk.Button(options_frame, text="EXPORT\nCAPTURED\nDATA", font=('Bold', 13), fg='white', bd=0,
                                 bg='#4392fa', width=15, borderwidth=5)
            data_btn.place(x=23, y=360)

            exp_input_summary_bt = tk.Button(options_frame, text="EXPORT INPUT\n SUMMARY", font=('Bold', 13),
                                             fg='white', bd=0, bg='#4392fa', width=15, borderwidth=5)
            exp_input_summary_bt.place(x=23, y=465)

            download_btn = tk.Button(options_frame, text="DOWNLOAD \n CLIP", font=('Bold', 13), fg='white', bd=0,
                                     bg='#4392fa', width=15, borderwidth=5)
            download_btn.place(x=23, y=550)

            cre_user = Button(options_frame, text='CREATE USER', font=('Bold', 13), fg='white', bd=0, bg='#4392fa',
                              width=15, borderwidth=5)
            cre_user.place(x=23, y=635)

            # MAIN FRAME

            main_frame = tk.Frame(admin_panel, highlightbackground='black', highlightthickness=2)
            main_frame.pack(side=tk.LEFT)
            main_frame.pack_propagate(False)
            main_frame.configure(height=1500, width=7100, bg='#2c2f33')

            admin_panel.mainloop()

        # Elif condition for employee #
        elif is_user(u_name, password):
            print('User Panel')

            user_panel = Tk()
            user_panel.geometry("1280x720")
            user_panel.title('USER PANEL')
            connect = sqlite3.connect('EAN.db')
            to_connect_name = connect.cursor()
            to_connect_name.execute("SELECT Images FROM details")
            image_data = to_connect_name.fetchone()[0]

            image_stream = BytesIO(image_data)
            original_img = Image.open(image_stream)
            desired_width = 80
            desired_height = 80
            resized_img = original_img.resize((desired_width, desired_height), Image.LANCZOS)
            img = ImageTk.PhotoImage(resized_img)

            # OPTION FRAME
            options_frame = tk.Frame(user_panel, bg="#c3c3c3", highlightbackground='black', highlightthickness=2)
            options_frame.pack(side=tk.LEFT)
            options_frame.pack_propagate(False)
            options_frame.configure(width=210, height=1500)

            # BUTTONS
            general = tk.Label(options_frame, text="GENERAL", font=10, bg="#c3c3c3")
            general.place(x=50, y=150)

            rec_btn = tk.Button(options_frame, text="RECORD", font=('Bold', 15), fg='white', bd=0, bg='#4392fa', width=15, borderwidth=5)
            rec_btn.place(x=10, y=200)

            summary_btn = tk.Button(options_frame, text="DISPLAY \n SUMMARY", font=('Bold', 15), fg='white', bd=0, bg='#4392fa', width=15, borderwidth=5)
            summary_btn.place(x=10, y=270)

            exp_rec_summary_bt = tk.Button(options_frame, text="EXPORT REC\n SUMMARY", font=('Bold', 15), fg='white', bd=0, bg='#4392fa', width=15, borderwidth=5, command=export_summary)
            exp_rec_summary_bt.place(x=10, y=370)

            label = Label(options_frame, image=img)
            label.place(x=58, y=800)

            company_name_display = Label(options_frame, text=f'{comp_name}', font=('Kozuka Gothic Pro B', 10, 'italic'), bg="#c3c3c3")
            company_name_display.place(x=70, y=900)

            company_location = Label(options_frame, text=f'{location_company}', font=('Kozuka Gothic Pro B', 10, 'italic'), bg="#c3c3c3")
            company_location.place(x=70, y=920)

            # MAIN FRAME
            main_frame = tk.Frame(user_panel, highlightbackground='black', highlightthickness=2)
            main_frame.pack(side=tk.LEFT)
            main_frame.pack_propagate(False)
            main_frame.configure(height=1500, width=7100, bg='#2c2f33')

            user_panel.mainloop()

        else:
            print('Invalid credentials or you do not have access to the admin portal.')
            messagebox.showerror('Invalid Credentials', f'Username or password is wrong')

# Classified based on the screen resolution #

    if check_user_name_not_null():
        if display_resolution[0] == 1920 and display_resolution[1] == 1080:
            log.destroy()
            admin_portal_1920x1080(u_name, password)
            print('laptop')

        elif display_resolution[0] == 1280 and display_resolution[1] == 720:
            log.destroy()
            admin_portal_1280x720(u_name, password)
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

    global comp_name, location_company

    company_names = to_connect_name.fetchall()
    company_names_str = "\n".join([name[0] for name in company_names])
    comp_name = company_names_str.upper()

    company_location = to_connect_location.fetchall()
    company_location_str = "\n".join([name[0] for name in company_location])
    location_company = company_location_str.upper()

    log = Tk()
    log.geometry("900x430")
    log.resizable(0,0)
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


