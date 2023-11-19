import bcrypt
from tkinter import *
import winsound
import tkinter as tk
from tkinter import filedialog
import cv2
import os
from pyzbar.pyzbar import decode
import sqlite3
import pandas as pd
from datetime import datetime
from moviepy.video.io.VideoFileClip import VideoFileClip
from tkcalendar import DateEntry
from tkinter import messagebox
import babel.numbers
import numpy as np
from PIL import Image, ImageTk
from datetime import date
from tkinter import ttk

current_time = datetime.now().time()
present_date = datetime.now().strftime("%d-%m-%Y")

recording1 = False
recording2 = False
recording3 = False
recording4 = False
recording5 = False
recording6 = False

writer1 = None
writer2 = None
writer3 = None
writer4 = None
writer5 = None
writer6 = None

current_date = datetime.now().strftime("%d-%m-%Y")
starting_time = current_time.strftime("%I-%M %p")

######################################### FILES CREATION ################################
try:
    if not os.path.exists('CAPTURED DATA EXCEL'):
        os.makedirs('CAPTURED DATA EXCEL')
except OSError:
    print('Error: Creating directory of CAPTURED DATA EXCEL')
try:
    if not os.path.exists('SUMMARY DATA EXCEL'):
        os.makedirs('SUMMARY DATA EXCEL')
except OSError:
    print('Error: Creating directory of SUMMARY DATA')
try:
    if not os.path.exists('CAPTURED DATA IMAGES'):
        os.makedirs('CAPTURED DATA IMAGES')
except OSError:
    print('Error: Creating directory of CAPTURED DATA IMAGES')
try:
    if not os.path.exists('DATABASES'):
        os.makedirs('DATABASES')
except OSError:
    print('Error: Creating directory of DATABASES')
try:
    if not os.path.exists(f"{current_date}"):
        os.makedirs(f"{current_date}")
except OSError:
    print('Error: Creating directory of current_date')

############################################# DATABASE CREATION #############################################

if not os.path.exists('DATABASES/recording.db'):  ##overall
    conn1 = sqlite3.connect('DATABASES/recording.db')
    conn1.execute(
        '''CREATE TABLE record1data(DETETCTED_DATA TEXT NOT NULL, DETECTED_TIME TIMESTAMP NOT NULL, VIDEO_NAME TEXT NOT NULL, DATE DATE NOT NULL,TIME TIMESTAMP NOT NULL, USER_NAME NOT NULL);''')
    conn1.execute(
        '''CREATE TABLE record2data(DETETCTED_DATA TEXT NOT NULL, DETECTED_TIME TIMESTAMP NOT NULL, VIDEO_NAME TEXT NOT NULL, DATE DATE NOT NULL,TIME TIMESTAMP NOT NULL, USER_NAME NOT NULL);''')
    conn1.execute(
        '''CREATE TABLE record3data(DETETCTED_DATA TEXT NOT NULL, DETECTED_TIME TIMESTAMP NOT NULL, VIDEO_NAME TEXT NOT NULL, DATE DATE NOT NULL,TIME TIMESTAMP NOT NULL, USER_NAME NOT NULL);''')
    conn1.execute(
        '''CREATE TABLE record4data(DETETCTED_DATA TEXT NOT NULL, DETECTED_TIME TIMESTAMP NOT NULL, VIDEO_NAME TEXT NOT NULL, DATE DATE NOT NULL,TIME TIMESTAMP NOT NULL, USER_NAME NOT NULL);''')
    conn1.execute(
        '''CREATE TABLE record5data(DETETCTED_DATA TEXT NOT NULL, DETECTED_TIME TIMESTAMP NOT NULL, VIDEO_NAME TEXT NOT NULL, DATE DATE NOT NULL,TIME TIMESTAMP NOT NULL, USER_NAME NOT NULL);''')
    conn1.execute(
        '''CREATE TABLE record6data(DETETCTED_DATA TEXT NOT NULL, DETECTED_TIME TIMESTAMP NOT NULL, VIDEO_NAME TEXT NOT NULL, DATE DATE NOT NULL,TIME TIMESTAMP NOT NULL, USER_NAME NOT NULL);''')
    conn1.execute(
        '''CREATE TABLE recordsummary(VIDEO_NAME TEXT NOT NULL, DURATION TIMESTAMP NOT NULL ,NO_OF_DATA TEXT NOT NULL, DATE DATE NOT NULL,TIME TIMESTAMP NOT NULL, USER_NAME NOT NULL);''')

if not os.path.exists('DATABASES/input.db'):  # cap_data
    conn2 = sqlite3.connect('DATABASES/input.db')
    conn2.execute(
        '''CREATE TABLE input_data(DETECTED_DATA TEXT NOT NULL, DETETCTED_TIME TIMESTAMP NOT NULL,VIDEO_NAME TEXT NOT NULL, UPLOADED_DATE DATE NOT NULL, UPLOADED_TIME TIMESTAMP NOT NULL );''')
    conn2.execute(
        '''CREATE TABLE input_summary(VIDEO_NAME TEXT NOT NULL, NO_OF_DATA TEXT NOT NULL, UPLOADED_DATE DATE NOT NULL,UPLOADED_TIME TIMESTAMP NOT NULL );''')

app = Tk()
app.title('LOGIN')
app.geometry('450x360')
app.resizable(0,0)
app.config(bg='#001220')

font1 = ('Helvetica',25,'bold')
font2 = ('Arial',15,'bold')
font3 = ('Arial',13,'bold')
font4 = ('Arial',13,'bold','underline')

con = sqlite3.connect('DATABASES/users.db')
cursor = con.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT NOT NULL, password TEXT NOT NULL)''')

def login_account():
    username = username_entry2.get()
    password = password_entry2.get()

    if username == 'admin' and password != '':

        cursor.execute('SELECT password FROM users WHERE username=?', [username])
        result = cursor.fetchone()
        if result:
            if bcrypt.checkpw(password.encode('utf-8'), result[0]):
                messagebox.showinfo('Success', 'admin Logged success')

                app.destroy()
                w = Tk()
                w.geometry('1366x768')
                w.configure(bg='#262626')
                w.title('EAN DETECTOR')

                current_time = datetime.now().time()
                present_date = datetime.now().strftime("%d-%m-%Y")


                def create_user():
                    app = Tk()
                    app.title('CREATE USER')
                    app.geometry('450x360')
                    app.resizable(0,0)
                    app.config(bg='#001220')

                    font1 = ('Helvetica', 25, 'bold')
                    font2 = ('Arial', 17, 'bold')

                    con = sqlite3.connect('DATABASES/users.db')
                    cursor = con.cursor()
                    cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT NOT NULL, password TEXT NOT NULL)''')

                    def user_create():
                        username = username_entry.get()
                        password = password_entry.get()
                        if username != '' and password != '':
                            cursor.execute('SELECT username FROM users WHERE username=?', [username])
                            if cursor.fetchone() is not None:
                                messagebox.showerror('Error', 'Username already exists')
                            else:
                                encoded_password = password.encode('utf-8')
                                hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
                                print("hash pass", hashed_password)
                                cursor.execute('INSERT INTO users VALUES (?, ?)', [username, hashed_password])
                                con.commit()
                                messagebox.showinfo('Success', 'Account created')
                                app.destroy()
                        else:
                            messagebox.showerror('Error', 'Enter all data')

                    frame1 = Frame(app, bg='#001220',  width=470, height=360)
                    frame1.place(x=0, y=0)

                    signup_label = Label(frame1, font=font1, text='CREATE USER', fg='#fff', bg='#001220')
                    signup_label.place(x=110, y=20)

                    username_entry = Entry(frame1, font=font2, bg='#fff')
                    username_entry.place(x=110, y=80)

                    password_entry = Entry(frame1, font=font2, bg='#fff')
                    password_entry.place(x=110, y=150)

                    signup_button = Button(frame1, font=font2, command=user_create,  fg='#fff',bg='#001220', text='CREATE')
                    signup_button.place(x=190, y=220)
                    app.mainloop()

                def change_password():
                    app = Tk()
                    app.title('NEW PASSWORD')
                    app.geometry('450x360')
                    app.resizable(0,0)
                    app.config(bg='#001220')

                    font1 = ('Helvetica', 25, 'bold')
                    font2 = ('Arial', 17, 'bold')

                    def password_change():
                        global new_pass

                        new_name = username_entry.get()
                        new_pass = new_pass_entry.get()

                        encoded_password = new_pass.encode('utf-8')
                        hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
                        print("update hash pass", hashed_password)

                        conn = sqlite3.connect('DATABASES/users.db')
                        cursor = conn.cursor()

                        cursor.execute(
                            '''UPDATE users SET password = ? WHERE username = ?''',
                            (hashed_password, new_name)
                        )
                        print('\n Updated...\n')
                        app.destroy()

                        conn.commit()
                        conn.close()


                    frame1 = Frame(app, bg='#001220',  width=470, height=360)
                    frame1.place(x=0, y=0)

                    pass_change_label = Label(frame1, font=font1, text='CHANGE PASSWORD',fg='#fff', bg='#001220')
                    pass_change_label.place(x=80, y=20)

                    username_entry = Entry(frame1, font=font2, bg='#fff')
                    username_entry.place(x=110, y=80)

                    new_pass_entry = Entry(frame1, font=font2, bg='#fff')
                    new_pass_entry.place(x=110, y=150)

                    change_button = Button(frame1, font=font2, command=password_change, fg='#fff', text='CHANGE',  bg='#121111', cursor='hand2')
                    change_button.place(x=190, y=220)
                    app.mainloop()

                menubar = Menu(w)
                filemenu = Menu(menubar, tearoff=0)
                filemenu.add_command(label='CHANGE PASSWORD', command=change_password)
                filemenu.add_command(label='CREATE USER', command=create_user)
                filemenu.add_separator()
                filemenu.add_command(label='EXIT', command=w.quit)
                menubar.add_cascade(label="OPTIONS", menu=filemenu)
                w.config(menu=menubar)

                def record():
                    options = ["6", "5", "4", "3", "2", "1"]
                    selected_option = tk.StringVar()

                    select = ttk.Label(main_frame, text="Select Cameras:-", font=10)
                    select.place(x=250, y=200)

                    combo_box = ttk.Combobox(main_frame, textvariable=selected_option, values=options, font=10, width=4)
                    combo_box.place(x=450, y=200)
                    combo_box.current(0)

                    def scan1(data1, elapsed_time_str1, present_date, present_time, video_name1, username):
                        rec_d1 = sqlite3.connect('./DATABASES/recording.db')
                        rec_d1.execute(
                            "INSERT INTO record1data (DETETCTED_DATA, DETECTED_TIME, DATE ,TIME , VIDEO_NAME, USER_NAME) VALUES (?,?,?,?,?,?)",
                            (data1, elapsed_time_str1, present_date, present_time, video_name1, username))
                        rec_d1.commit()
                        rec_d1.close()

                    def scan2(data2, elapsed_time_str2, present_date, present_time, video_name2, username):
                        rec_d2 = sqlite3.connect('./DATABASES/recording.db')
                        rec_d2.execute(
                            "INSERT INTO record2data (DETETCTED_DATA, DETECTED_TIME, DATE ,TIME , VIDEO_NAME, USER_NAME) VALUES (?,?,?,?,?,?)",
                            (data2, elapsed_time_str2, present_date, present_time, video_name2, username))
                        rec_d2.commit()
                        rec_d2.close()

                    def scan3(data3, elapsed_time_str3, present_date, present_time, video_name3, username):
                        rec_d3 = sqlite3.connect('./DATABASES/recording.db')
                        rec_d3.execute(
                            "INSERT INTO record3data (DETETCTED_DATA, DETECTED_TIME, DATE ,TIME , VIDEO_NAME, USER_NAME) VALUES (?,?,?,?,?,?)",
                            (data3, elapsed_time_str3, present_date, present_time, video_name3, username))
                        rec_d3.commit()
                        rec_d3.close()

                    def scan4(data4, elapsed_time_str4, present_date, present_time, video_name4, username):
                        rec_d4 = sqlite3.connect('./DATABASES/recording.db')
                        rec_d4.execute(
                            "INSERT INTO record4data (DETETCTED_DATA, DETECTED_TIME, DATE ,TIME , VIDEO_NAME, USER_NAME) VALUES (?,?,?,?,?,?)",
                            (data4, elapsed_time_str4, present_date, present_time, video_name4, username))
                        rec_d4.commit()
                        rec_d4.close()

                    def scan5(data5, elapsed_time_str5, present_date, present_time, video_name5, username):
                        rec_d5 = sqlite3.connect('./DATABASES/recording.db')
                        rec_d5.execute(
                            "INSERT INTO record5data (DETETCTED_DATA, DETECTED_TIME, DATE ,TIME , VIDEO_NAME, USER_NAME) VALUES (?,?,?,?,?,?)",
                            (data5, elapsed_time_str5, present_date, present_time, video_name5, username))
                        rec_d5.commit()
                        rec_d5.close()

                    def scan6(data6, elapsed_time_str6, present_date, present_time, video_name6, username):
                        rec_d6 = sqlite3.connect('./DATABASES/recording.db')
                        rec_d6.execute(
                            "INSERT INTO record6data (DETETCTED_DATA, DETECTED_TIME, DATE ,TIME , VIDEO_NAME, USER_NAME) VALUES (?,?,?,?,?,?)",
                            (data6, elapsed_time_str6, present_date, present_time, video_name6, username))
                        rec_d6.commit()
                        rec_d6.close()

                    def dispatch1(camera1, elapsed_time_str1, code_array1, present_date, present_time, username):
                        sum1 = sqlite3.connect('./DATABASES/recording.db')
                        sum1.execute(
                            "INSERT INTO recordsummary (VIDEO_NAME, DURATION, NO_OF_DATA, DATE, TIME, USER_NAME) VALUES (?,?,?,?,?,?)",
                            (camera1, elapsed_time_str1, code_array1, present_date, present_time, username))
                        sum1.commit()
                        sum1.close()

                    def dispatch2(camera2, elapsed_time_str2, code_array2, present_date, present_time, username):
                        sum2 = sqlite3.connect('./DATABASES/recording.db')
                        sum2.execute(
                            "INSERT INTO recordsummary (VIDEO_NAME, DURATION, NO_OF_DATA, DATE, TIME, USER_NAME) VALUES (?,?,?,?,?,?)",
                            (camera2, elapsed_time_str2, code_array2, present_date, present_time, username))
                        sum2.commit()
                        sum2.close()

                    def dispatch3(camera3, elapsed_time_str3, code_array2, present_date, present_time, username):
                        sum3 = sqlite3.connect('./DATABASES/recording.db')
                        sum3.execute(
                            "INSERT INTO recordsummary (VIDEO_NAME, DURATION, NO_OF_DATA, DATE, TIME, USER_NAME) VALUES (?,?,?,?,?,?)",
                            (camera3, elapsed_time_str3, code_array2, present_date, present_time, username))
                        sum3.commit()
                        sum3.close()

                    def dispatch4(camera4, elapsed_time_str4, code_array4, present_date, present_time, username):
                        sum4 = sqlite3.connect('./DATABASES/recording.db')
                        sum4.execute(
                            "INSERT INTO recordsummary (VIDEO_NAME, DURATION, NO_OF_DATA, DATE, TIME, USER_NAME) VALUES (?,?,?,?,?,?)",
                            (camera4, elapsed_time_str4, code_array4, present_date, present_time, username))
                        sum4.commit()
                        sum4.close()

                    def dispatch5(camera5, elapsed_time_str5, code_array5, present_date, present_time, username):
                        sum5 = sqlite3.connect('./DATABASES/recording.db')
                        sum5.execute(
                            "INSERT INTO recordsummary (VIDEO_NAME, DURATION, NO_OF_DATA, DATE, TIME, USER_NAME) VALUES (?,?,?,?,?,?)",
                            (camera5, elapsed_time_str5, code_array5, present_date, present_time, username))
                        sum5.commit()
                        sum5.close()

                    def dispatch6(camera6, elapsed_time_str6, code_array6, present_date, present_time, username):
                        sum6 = sqlite3.connect('./DATABASES/recording.db')
                        sum6.execute(
                            "INSERT INTO recordsummary (VIDEO_NAME, DURATION, NO_OF_DATA, DATE, TIME, USER_NAME) VALUES (?,?,?,?,?,?)",
                            (camera6, elapsed_time_str6, code_array6, present_date, present_time, username))
                        sum6.commit()
                        sum6.close()

                    def reco():
                        selected_value = selected_option.get()

                        if selected_value == "1":
                            def start_recording1():
                                global recording1, start_time1, writer1, current_date, starting_time1, started_time1, elapsed_time_str1, first_detection_times1, camera1, data1, qr_codes_array1, video_name1
                                recording1 = True
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
                                global recording1, writer1, start_time1, elapsed_time_str1, code_array1
                                recording1 = False
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
                                    dispatch1(video_name1, elapsed_time_str1, len(qr_codes_array1), present_date,
                                              present_time, username)
                                    rec1_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record1data WHERE VIDEO_NAME = '{video_name1}'", rec1_data)
                                    df.to_excel(f"./{current_date}/{video_name1}.xlsx", index=False)
                                    rec1_data.close()

                            cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)

                            cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            fourcc1 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

                            def process_frame():
                                global recording1, start_time1, writer1, end_time1, present_date, present_time, elapsed_time_str1, data1
                                # CAM CCTV
                                ret1, frame1 = cap1.read()
                                cv2.putText(frame1, "CAM1", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret1:
                                    if recording1:
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
                                                scan1(data1, elapsed_time_str1, present_date, present_time, video_name1,
                                                      username)

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

                            def disable_event():
                                pass

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

                        elif selected_value == "2":
                            ################################    CAM1    RECORDING    ##################################
                            def start_recording1():
                                global recording1, start_time1, writer1, current_date, starting_time1, started_time1, elapsed_time_str1, first_detection_times1, qr_codes_array1, data1, camera1, video_name1
                                recording1 = True
                                data1 = ' '
                                start_time1 = None
                                qr_codes_array1 = []
                                live_time1 = datetime.now()
                                first_detection_times1 = {}
                                starting_time1 = current_time.strftime("%I-%M %p")
                                started_time1 = live_time1.strftime("%I:%M %p")
                                start_time1 = None
                                num1.config(text=0)
                                strt1.config(text=0)
                                drn1.config(text=0)
                                camera1 = "CAM1"
                                time_1 = time1.get()
                                video_name1 = f'{camera1}-{time_1}'
                                print("Camera1 Recording")
                                writer1 = cv2.VideoWriter(f"./{current_date}/{video_name1}.mp4", fourcc1, 23.0,
                                                          (640, 480))

                            def stop_recording1():
                                global recording1, writer1, start_time1, elapsed_time_str1, code_array1
                                recording1 = False

                                print("Camera1 Stopped")
                                if writer1 is not None:
                                    writer1.release()

                                elapsed_time1 = datetime.now() - start_time1
                                elapsed_time_str1 = str(elapsed_time1).split(".")[0]
                                dur1 = elapsed_time_str1
                                print("Camera1 stopped")
                                code_array1 = len(qr_codes_array1)
                                print("No Of detected QR codes in camera1:", code_array1)
                                if len(first_detection_times1) == 0:
                                    print("No data in camera1")
                                else:
                                    strt1.config(text=started_time1)
                                    drn1.config(text=dur1)
                                    num1.config(text=code_array1)
                                    dispatch1(video_name1, elapsed_time_str1, len(qr_codes_array1), present_date,
                                              present_time, username)
                                    rec1_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record1data WHERE VIDEO_NAME = '{video_name1}'", rec1_data)
                                    df.to_excel(f"./{current_date}/{video_name1}.xlsx", index=False)
                                    rec1_data.close()

                                    ################################    CAM2    RECORDING    ##################################

                            def start_recording2():
                                global recording2, start_time2, writer2, current_date, starting_time2, qr_codes_array2, data2, started_time2, camera2, first_detection_times2, elapsed_time_str2, video_name2
                                recording2 = True
                                start_time2 = None
                                data2 = ' '
                                qr_codes_array2 = []
                                first_detection_times2 = {}
                                live_time = datetime.now()
                                starting_time2 = current_time.strftime("%I-%M %p")
                                started_time2 = live_time.strftime("%I:%M %p")
                                num2.config(text=0)
                                strt2.config(text=0)
                                drn2.config(text=0)
                                camera2 = "CAM2"
                                time_2 = time2.get()
                                video_name2 = f'{camera2}-{time_2}'

                                print("Camera2 Recording")
                                writer2 = cv2.VideoWriter(f"./{current_date}/{video_name2}.mp4", fourcc1, 23.0,
                                                          (640, 480))

                            def stop_recording2():
                                global recording2, writer2, start_time2, code_array2, elapsed_time_str2
                                recording2 = False

                                if writer2 is not None:
                                    writer2.release()

                                elapsed_time2 = datetime.now() - start_time2
                                elapsed_time_str2 = str(elapsed_time2).split(".")[0]
                                dur2 = elapsed_time_str2
                                print("Camera2 stopped")
                                code_array2 = len(qr_codes_array2)
                                print("No Of detected QR codes in camera2:", code_array2)

                                if len(first_detection_times2) == 0:
                                    print("No data in camera2")

                                else:
                                    strt2.config(text=started_time2)
                                    drn2.config(text=dur2)
                                    num2.config(text=code_array2)

                                    dispatch2(video_name2, elapsed_time_str2, len(qr_codes_array2), present_date,
                                              present_time, username)

                                    rec2_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record2data WHERE VIDEO_NAME = '{video_name2}'", rec2_data)
                                    df.to_excel(f"./{current_date}/{video_name2}.xlsx", index=False)
                                    rec2_data.close()

                            cap1 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
                            cap2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)

                            cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            fourcc1 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time1 = datetime.now().strftime("%H-%M")

                            fourcc2 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time2 = datetime.now().strftime("%H-%M")

                            def process_frame():
                                global recording1, recording2, recording3, start_time1, start_time2, start_time3, writer1, writer2, writer3, end_time1, end_time2, end_time3, data1, data2, code_array1, code_array2, present_date, present_time, elapsed_time_str1, elapsed_time_str2
                                # CAM1
                                ret1, frame1 = cap1.read()
                                cv2.putText(frame1, "CAM1", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret1:
                                    if recording1:
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
                                                    f"QR code {data1} detected for the first time at{elapsed_time_str1} on {present_date}-{present_time} ")
                                                scan1(data1, elapsed_time_str1, present_date, present_time, video_name1,
                                                      username)

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
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame1, f"NO OF DATA:  {len(qr_codes_array1)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame1, f"LAST DATA:   {data1}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        writer1.write(frame1)
                                    cv2.imshow("Recording Camera cctv", frame1)
                                if not ret1:
                                    blank_frame1 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame1, "CAM1 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera cctv", blank_frame1)

                                # CAM2
                                ret2, frame2 = cap2.read()
                                cv2.putText(frame2, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret2:
                                    if recording2:
                                        qr_codes2 = decode(frame2)
                                        for qr_code2 in qr_codes2:
                                            data2 = qr_code2.data.decode('utf-8')
                                            if data2 not in first_detection_times2:
                                                first_detection_times2[data2] = cap2.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array2.append(data2)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data2} detected for the first time at{elapsed_time_str2} on {present_date}-{present_time} ")
                                                scan2(data2, elapsed_time_str2, present_date, present_time, video_name2,
                                                      username)

                                            for qr_code2 in qr_codes2:
                                                (x, y, w, h) = qr_code2.rect
                                                cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code2.rect
                                                cv2.putText(frame2, data2, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array2) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time2 is None:
                                            start_time2 = datetime.now()

                                        elapsed_time2 = datetime.now() - start_time2
                                        elapsed_time_str2 = str(elapsed_time2).split(".")[0]
                                        cv2.putText(frame2, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame2, f"START TIME:  {started_time2}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame2, f"DURATION:    {elapsed_time_str2}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame2, f"NO OF DATA:  {len(qr_codes_array2)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame2, f"LAST DATA:   {data2}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        writer2.write(frame2)
                                    cv2.imshow("Recording Camera 2", frame2)

                                if not ret2:
                                    blank_frame2 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame2, "CAM2 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 2", blank_frame2)

                                cv2.waitKey(1)
                                controller.after(1, process_frame)

                            def start():
                                start_recording1()
                                start_recording2()

                            def stop():
                                stop_recording1()
                                stop_recording2()

                            def close_window():
                                cap1.release()
                                cap2.release()
                                cv2.destroyAllWindows()
                                controller.destroy()

                            controller = tk.Tk()
                            controller.geometry("300x500")
                            controller.title("VIDEO CONTROLLER")
                            controller.resizable(0, 0)
                            start = tk.Button(controller, text="START", command=start)
                            start.place(x=80, y=20)
                            stop = tk.Button(controller, text="STOP", command=stop)
                            stop.place(x=180, y=20)
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
                            ####################    CAM2
                            cam2 = tk.Label(controller, text="CAMERA 2", fg='red')
                            cam2.place(x=20, y=240)
                            get_time2 = tk.Label(controller, text='Enter Time')
                            get_time2.place(x=60, y=270)
                            time2 = tk.Entry(controller)
                            time2.place(x=160, y=270)
                            start_button_2 = tk.Button(controller, text="START CAM2", command=start_recording2)
                            start_button_2.place(x=60, y=300)
                            stop_button_2 = tk.Button(controller, text="STOP CAM2", command=stop_recording2)
                            stop_button_2.place(x=160, y=300)
                            ####################    CAM2
                            Start_timing2 = tk.Label(controller, text="START TIME")
                            Start_timing2.place(x=60, y=330)
                            strt2 = tk.Label(controller, text="0:0")
                            strt2.place(x=210, y=330)
                            Duration_time2 = tk.Label(controller, text="DURATION")
                            Duration_time2.place(x=60, y=360)
                            drn2 = tk.Label(controller, text="0:0:0")
                            drn2.place(x=210, y=360)
                            NOD2 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD2.place(x=60, y=390)
                            num2 = tk.Label(controller, text="0")
                            num2.place(x=210, y=390)
                            ######################  CLOSE

                            close_button = tk.Button(controller, text="CLOSE", command=close_window)
                            close_button.place(x=130, y=430)

                            process_frame()
                            controller.mainloop()
                            cap1.release()
                            cap2.release()
                            cv2.destroyAllWindows()

                        elif selected_value == "3":
                            ################################    CAM1    RECORDING    ##################################
                            def start_recording1():
                                global recording1, start_time1, writer1, current_date, starting_time1, started_time1, elapsed_time_str1, first_detection_times1, camera1, data1, qr_codes_array1, video_name2
                                recording1 = True
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
                                global recording1, writer1, start_time1, elapsed_time_str1, code_array1
                                recording1 = False
                                print("Camera1 Stopped")
                                if writer1 is not None:
                                    writer1.release()

                                elapsed_time1 = datetime.now() - start_time1
                                elapsed_time_str1 = str(elapsed_time1).split(".")[0]
                                dur1 = elapsed_time_str1
                                code_array1 = len(qr_codes_array1)
                                print("no in 1 camera", code_array1)

                                if len(first_detection_times1) == 0:
                                    print("no")

                                else:
                                    strt1.config(text=started_time1)
                                    drn1.config(text=dur1)
                                    num1.config(text=code_array1)
                                    dispatch1(video_name1, elapsed_time_str1, len(qr_codes_array1), present_date,
                                              present_time, username)
                                    rec1_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record1data WHERE VIDEO_NAME = '{video_name1}'", rec1_data)
                                    df.to_excel(f"./{current_date}/{video_name1}.xlsx", index=False)
                                    rec1_data.close()

                                    ################################    CAM2    RECORDING    ##################################

                            def start_recording2():
                                global recording2, start_time2, writer2, current_date, starting_time2, qr_codes_array2, data2, started_time2, camera2, first_detection_times2, elapsed_time_str2, video_name2
                                recording2 = True
                                start_time2 = None
                                data2 = ' '
                                qr_codes_array2 = []
                                first_detection_times2 = {}
                                live_time = datetime.now()
                                starting_time2 = current_time.strftime("%I-%M %p")
                                started_time2 = live_time.strftime("%I:%M %p")
                                num2.config(text=0)
                                strt2.config(text=0)
                                drn2.config(text=0)
                                camera2 = "CAM2"
                                time_2 = time2.get()
                                video_name2 = f'{camera2}-{time_2}'

                                print("Camera2 Recording")
                                writer2 = cv2.VideoWriter(f"./{current_date}/{video_name2}.mp4", fourcc1, 23.0,
                                                          (640, 480))

                            def stop_recording2():
                                global recording2, writer2, start_time2, code_array2, elapsed_time_str2
                                recording2 = False

                                if writer2 is not None:
                                    writer2.release()

                                elapsed_time2 = datetime.now() - start_time2
                                elapsed_time_str2 = str(elapsed_time2).split(".")[0]
                                dur2 = elapsed_time_str2
                                print("Camera2 stopped")
                                code_array2 = len(qr_codes_array2)
                                print("No Of detected QR codes in camera2:", code_array2)

                                if len(first_detection_times2) == 0:
                                    print("No data in camera2")

                                else:
                                    strt2.config(text=started_time2)
                                    drn2.config(text=dur2)
                                    num2.config(text=code_array2)

                                    dispatch2(video_name2, elapsed_time_str2, len(qr_codes_array2), present_date,
                                              present_time, username)

                                    rec2_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record2data WHERE VIDEO_NAME = '{video_name2}'", rec2_data)
                                    df.to_excel(f"./{current_date}/{video_name2}.xlsx", index=False)
                                    rec2_data.close()

                            def start_recording3():
                                global recording3, start_time3, writer3, current_date, starting_time3, qr_codes_array3, data3, started_time3, camera3, elapsed_time_str3, first_detection_times3, video_name3
                                recording3 = True
                                start_time3 = None
                                data3 = ' '
                                qr_codes_array3 = []
                                camera3 = "CAM3"
                                time_3 = time3.get()
                                video_name3 = f'{camera3}-{time_3}'
                                live_time = datetime.now()
                                first_detection_times3 = {}
                                starting_time3 = current_time.strftime("%I-%M %p")
                                started_time3 = live_time.strftime("%I:%M %p")
                                start_time3 = None
                                print("Camera3 Recording")
                                writer3 = cv2.VideoWriter(f"./{current_date}/{video_name3}.mp4", fourcc3, 23.0,
                                                          (640, 480))

                            def stop_recording3():
                                global recording3, writer3, start_time3, clip_name3, code_array3, elapsed_time_str3
                                recording3 = False
                                if writer3 is not None:
                                    writer3.release()
                                elapsed_time3 = datetime.now() - start_time3
                                elapsed_time_str3 = str(elapsed_time3).split(".")[0]
                                dur3 = elapsed_time_str3
                                print("Camera3 stopped")
                                code_array3 = len(qr_codes_array3)
                                print("No Of detected QR codes in camera3:", code_array3)

                                if len(first_detection_times3) == 0:
                                    print("No data")
                                else:
                                    strt3.config(text=started_time3)
                                    drn3.config(text=dur3)
                                    num3.config(text=code_array3)
                                    dispatch3(video_name3, elapsed_time_str3, len(qr_codes_array3), present_date,
                                              present_time, username)
                                    rec3_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record3data WHERE VIDEO_NAME = '{video_name3}'", rec3_data)
                                    df.to_excel(f"./{current_date}/{video_name3}.xlsx", index=False)
                                    rec3_data.close()

                            cap1 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
                            cap2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)
                            cap3 = cv2.VideoCapture(3, cv2.CAP_DSHOW)

                            cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap3.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap3.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            fourcc1 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time1 = datetime.now().strftime("%H-%M")

                            fourcc2 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time2 = datetime.now().strftime("%H-%M")

                            fourcc3 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time3 = datetime.now().strftime("%H-%M")

                            def process_frame():
                                global recording1, recording2, recording3, start_time1, start_time2, start_time3, writer1, writer2, writer3, end_time1, end_time2, end_time3, data1, data2, code_array1, code_array2, present_date, present_time, elapsed_time_str1, elapsed_time_str2, elapsed_time_str3, recording1, start_time1, writer1, end_time1, present_date, present_time, elapsed_time_str1, data1
                                # CAM CCTV
                                ret1, frame1 = cap1.read()
                                cv2.putText(frame1, "CAM1", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret1:
                                    if recording1:
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
                                                    f"QR code {data1} detected for the first time at{elapsed_time_str1} on {present_date}-{present_time} ")
                                                scan1(data1, elapsed_time_str1, present_date, present_time, video_name1,
                                                      username)

                                            for qr_code1 in qr_codes1:
                                                (x, y, w, h) = qr_code1.rect
                                                cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code1.rect
                                                cv2.putText(frame1, data1, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

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
                                    cv2.imshow("Recording Camera cctv", blank_frame1)

                                # CAM2
                                ret2, frame2 = cap2.read()
                                cv2.putText(frame2, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret2:
                                    if recording2:
                                        qr_codes2 = decode(frame2)
                                        for qr_code2 in qr_codes2:
                                            data2 = qr_code2.data.decode('utf-8')
                                            if data2 not in first_detection_times2:
                                                first_detection_times2[data2] = cap2.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array2.append(data2)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data2} detected for the first time at{elapsed_time_str2} on {present_date}-{present_time} ")
                                                scan2(data2, elapsed_time_str2, present_date, present_time, video_name2,
                                                      username)

                                            for qr_code2 in qr_codes2:
                                                (x, y, w, h) = qr_code2.rect
                                                cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code2.rect
                                                cv2.putText(frame2, data2, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array2) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time2 is None:
                                            start_time2 = datetime.now()

                                        elapsed_time2 = datetime.now() - start_time2
                                        elapsed_time_str2 = str(elapsed_time2).split(".")[0]
                                        cv2.putText(frame2, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame2, f"START TIME:  {started_time2}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame2, f"DURATION:    {elapsed_time_str2}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame2, f"NO OF DATA:  {len(qr_codes_array2)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame2, f"LAST DATA:   {data2}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        writer2.write(frame2)
                                    cv2.imshow("Recording Camera 2", frame2)

                                if not ret2:
                                    blank_frame2 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame2, "CAM2 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 2", blank_frame2)

                                # CAM3
                                ret3, frame3 = cap3.read()
                                cv2.putText(frame3, "CAM3", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret3:
                                    if recording3:
                                        qr_codes3 = decode(frame3)
                                        for qr_code3 in qr_codes3:
                                            data3 = qr_code3.data.decode('utf-8')
                                            if data3 not in first_detection_times3:
                                                first_detection_times3[data3] = cap2.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array3.append(data3)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data3} detected for the first time at{elapsed_time_str3} on {present_date}-{present_time} ")
                                                scan3(data3, elapsed_time_str3, present_date, present_time, video_name3,
                                                      username)

                                            for qr_code3 in qr_codes3:
                                                (x, y, w, h) = qr_code3.rect
                                                cv2.rectangle(frame3, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code3.rect
                                                cv2.putText(frame3, data3, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array3) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time3 is None:
                                            start_time3 = datetime.now()

                                        elapsed_time3 = datetime.now() - start_time3
                                        elapsed_time_str3 = str(elapsed_time3).split(".")[0]
                                        cv2.putText(frame3, "CAM3", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame3, f"START TIME:  {started_time3}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame3, f"DURATION:    {elapsed_time_str3}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame3, f"NO OF DATA:  {len(qr_codes_array3)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame3, f"LAST DATA:   {data2}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        writer3.write(frame3)
                                    cv2.imshow("Recording Camera 3", frame3)

                                if not ret3:
                                    blank_frame3 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame3, "CAM3 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 3", blank_frame3)

                                cv2.waitKey(1)
                                controller.after(1, process_frame)

                            def start():
                                start_recording1()
                                start_recording2()
                                start_recording3()

                            def stop():
                                stop_recording1()
                                stop_recording2()
                                stop_recording3()

                            def close_window():
                                cap1.release()
                                cap2.release()
                                cap3.release()
                                cv2.destroyAllWindows()
                                controller.destroy()

                            controller = tk.Tk()
                            controller.geometry("300x650")
                            controller.title("VIDEO CONTROLLER")
                            controller.resizable(0, 0)
                            start = tk.Button(controller, text="START", command=start)
                            start.place(x=80, y=20)
                            stop = tk.Button(controller, text="STOP", command=stop)
                            stop.place(x=180, y=20)
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
                            ####################    CAM2
                            cam2 = tk.Label(controller, text="CAMERA 2", fg='red')
                            cam2.place(x=20, y=240)
                            get_time2 = tk.Label(controller, text='Enter Time')
                            get_time2.place(x=60, y=270)
                            time2 = tk.Entry(controller)
                            time2.place(x=160, y=270)
                            start_button_2 = tk.Button(controller, text="START CAM2", command=start_recording2)
                            start_button_2.place(x=60, y=300)
                            stop_button_2 = tk.Button(controller, text="STOP CAM2", command=stop_recording2)
                            stop_button_2.place(x=160, y=300)
                            ####################    CAM2
                            Start_timing2 = tk.Label(controller, text="START TIME")
                            Start_timing2.place(x=60, y=330)
                            strt2 = tk.Label(controller, text="0:0")
                            strt2.place(x=210, y=330)
                            Duration_time2 = tk.Label(controller, text="DURATION")
                            Duration_time2.place(x=60, y=360)
                            drn2 = tk.Label(controller, text="0:0:0")
                            drn2.place(x=210, y=360)
                            NOD2 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD2.place(x=60, y=390)
                            num2 = tk.Label(controller, text="0")
                            num2.place(x=210, y=390)
                            ####################    CAM3
                            cam3 = tk.Label(controller, text="CAMERA 3", fg='violet')
                            cam3.place(x=20, y=420)
                            get_time3 = tk.Label(controller, text='Enter Time')
                            get_time3.place(x=60, y=450)
                            time3 = tk.Entry(controller)
                            time3.place(x=160, y=450)
                            start_button_3 = tk.Button(controller, text="START CAM3", command=start_recording3)
                            start_button_3.place(x=60, y=480)
                            stop_button_3 = tk.Button(controller, text="STOP CAM3", command=stop_recording3)
                            stop_button_3.place(x=160, y=480)
                            ####################    CAM3
                            Start_timing3 = tk.Label(controller, text="START TIME")
                            Start_timing3.place(x=60, y=510)
                            strt3 = tk.Label(controller, text="0:0")
                            strt3.place(x=210, y=510)
                            Duration_time3 = tk.Label(controller, text="DURATION")
                            Duration_time3.place(x=60, y=540)
                            drn3 = tk.Label(controller, text="0:0:0")
                            drn3.place(x=210, y=540)
                            NOD3 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD3.place(x=60, y=570)
                            num3 = tk.Label(controller, text="0")
                            num3.place(x=210, y=570)
                            ######################  CLOSE

                            close_button = tk.Button(controller, text="CLOSE", command=close_window)
                            close_button.place(x=130, y=600)

                            process_frame()
                            controller.mainloop()
                            cap1.release()
                            cap2.release()
                            cap3.release()
                            cv2.destroyAllWindows()

                        elif selected_value == "4":

                            ################################    CAM1    RECORDING    ##################################
                            def start_recording1():
                                global recording1, start_time1, writer1, current_date, starting_time1, started_time1, elapsed_time_str1, first_detection_times1, camera1, data1, qr_codes_array1, video_name1
                                recording1 = True
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
                                global recording1, writer1, start_time1, elapsed_time_str1, code_array1
                                recording1 = False
                                print("Camera1 Stopped")
                                if writer1 is not None:
                                    writer1.release()

                                elapsed_time1 = datetime.now() - start_time1
                                elapsed_time_str1 = str(elapsed_time1).split(".")[0]
                                dur1 = elapsed_time_str1
                                code_array1 = len(qr_codes_array1)
                                print("no in 1 camera", code_array1)

                                if len(first_detection_times1) == 0:
                                    print("no")

                                else:
                                    strt1.config(text=started_time1)
                                    drn1.config(text=dur1)
                                    num1.config(text=code_array1)
                                    dispatch1(video_name1, elapsed_time_str1, len(qr_codes_array1), present_date,
                                              present_time, username)
                                    rec1_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record1data WHERE VIDEO_NAME = '{video_name1}'", rec1_data)
                                    df.to_excel(f"./{current_date}/{video_name1}.xlsx", index=False)
                                    rec1_data.close()

                            def start_recording2():
                                global recording2, start_time2, writer2, current_date, starting_time2, qr_codes_array2, data2, started_time2, camera2, first_detection_times2, elapsed_time_str2, video_name2
                                recording2 = True
                                start_time2 = None
                                data2 = ' '
                                qr_codes_array2 = []
                                first_detection_times2 = {}
                                live_time = datetime.now()
                                starting_time2 = current_time.strftime("%I-%M %p")
                                started_time2 = live_time.strftime("%I:%M %p")
                                num2.config(text=0)
                                strt2.config(text=0)
                                drn2.config(text=0)
                                camera2 = "CAM2"
                                time_2 = time2.get()
                                video_name2 = f'{camera2}-{time_2}'

                                print("Camera2 Recording")
                                writer2 = cv2.VideoWriter(f"./{current_date}/{video_name2}.mp4", fourcc1, 23.0,
                                                          (640, 480))

                            def stop_recording2():
                                global recording2, writer2, start_time2, code_array2, elapsed_time_str2
                                recording2 = False

                                if writer2 is not None:
                                    writer2.release()

                                elapsed_time2 = datetime.now() - start_time2
                                elapsed_time_str2 = str(elapsed_time2).split(".")[0]
                                dur2 = elapsed_time_str2
                                print("Camera2 stopped")
                                code_array2 = len(qr_codes_array2)
                                print("No Of detected QR codes in camera2:", code_array2)

                                if len(first_detection_times2) == 0:
                                    print("No data in camera2")

                                else:
                                    strt2.config(text=started_time2)
                                    drn2.config(text=dur2)
                                    num2.config(text=code_array2)

                                    dispatch2(video_name2, elapsed_time_str2, len(qr_codes_array2), present_date,
                                              present_time, username)

                                    rec2_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record2data WHERE VIDEO_NAME = '{video_name2}'", rec2_data)
                                    df.to_excel(f"./{current_date}/{video_name2}.xlsx", index=False)
                                    rec2_data.close()

                                    ################################    CAM3    RECORDING    ##################################

                            def start_recording3():
                                global recording3, start_time3, writer3, current_date, starting_time3, qr_codes_array3, data3, started_time3, camera3, elapsed_time_str3, first_detection_times3, video_name3
                                recording3 = True
                                start_time3 = None
                                data3 = ' '
                                qr_codes_array3 = []
                                camera3 = "CAM3"
                                time_3 = time3.get()
                                video_name3 = f'{camera3}-{time_3}'
                                live_time = datetime.now()
                                first_detection_times3 = {}
                                starting_time3 = current_time.strftime("%I-%M %p")
                                started_time3 = live_time.strftime("%I:%M %p")
                                start_time3 = None
                                print("Camera3 Recording")
                                writer3 = cv2.VideoWriter(f"./{current_date}/{video_name3}.mp4", fourcc3, 23.0,
                                                          (640, 480))

                            def stop_recording3():
                                global recording3, writer3, start_time3, clip_name3, code_array3, elapsed_time_str3
                                recording3 = False
                                if writer3 is not None:
                                    writer3.release()
                                elapsed_time3 = datetime.now() - start_time3
                                elapsed_time_str3 = str(elapsed_time3).split(".")[0]
                                dur3 = elapsed_time_str3
                                print("Camera3 stopped")
                                code_array3 = len(qr_codes_array3)
                                print("No Of detected QR codes in camera3:", code_array3)

                                if len(first_detection_times3) == 0:
                                    print("No data")
                                else:
                                    strt3.config(text=started_time3)
                                    drn3.config(text=dur3)
                                    num3.config(text=code_array3)
                                    dispatch3(video_name3, elapsed_time_str3, len(qr_codes_array3), present_date,
                                              present_time, username)
                                    rec3_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record3data WHERE VIDEO_NAME = '{video_name3}'", rec3_data)
                                    df.to_excel(f"./{current_date}/{video_name3}.xlsx", index=False)
                                    rec3_data.close()

                                    ################################    CAM4    RECORDING    ##################################

                            def start_recording4():
                                global recording4, start_time4, writer4, current_datz, starting_time4, qr_codes_array4, data4, started_time4, camera4, first_detection_times4, elapsed_time_str4, video_name4
                                recording4 = True
                                start_time4 = None
                                data4 = ' '
                                qr_codes_array4 = []
                                first_detection_times4 = {}
                                live_time = datetime.now()
                                starting_time4 = current_time.strftime("%I-%M %p")
                                started_time4 = live_time.strftime("%I:%M %p")
                                num4.config(text=0)
                                strt4.config(text=0)
                                drn4.config(text=0)
                                camera4 = "CAM4"
                                time_4 = time4.get()
                                video_name4 = f'{camera4}-{time_4}'
                                print("Camera4 Recording")
                                writer4 = cv2.VideoWriter(f"./{current_date}/{video_name4}.mp4", fourcc4, 23.0,
                                                          (640, 480))

                            def stop_recording4():
                                global recording4, writer4, start_time4, code_array4, elapsed_time_str4
                                recording4 = False
                                if writer4 is not None:
                                    writer4.release()
                                elapsed_time4 = datetime.now() - start_time4
                                elapsed_time_str4 = str(elapsed_time4).split(".")[0]
                                dur4 = elapsed_time_str4
                                print("Camera4 stopped")
                                code_array4 = len(qr_codes_array4)
                                print("No Of detected QR codes in camera4:", code_array4)
                                if len(first_detection_times4) == 0:
                                    print("No data in camera4")
                                else:
                                    strt4.config(text=started_time4)
                                    drn4.config(text=dur4)
                                    num4.config(text=code_array4)
                                    dispatch4(video_name4, elapsed_time_str4, len(qr_codes_array4), present_date,
                                              present_time, username)
                                    rec4_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record4data WHERE VIDEO_NAME = '{video_name4}'", rec4_data)
                                    df.to_excel(f"./{current_date}/{video_name4}.xlsx", index=False)
                                    rec4_data.close()

                            cap1 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
                            cap2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)
                            cap3 = cv2.VideoCapture(3, cv2.CAP_DSHOW)
                            cap4 = cv2.VideoCapture(4, cv2.CAP_DSHOW)

                            cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap3.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap3.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap4.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap4.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            fourcc1 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time1 = datetime.now().strftime("%H-%M")
                            fourcc2 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time2 = datetime.now().strftime("%H-%M")
                            fourcc3 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time3 = datetime.now().strftime("%H-%M")
                            fourcc4 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time4 = datetime.now().strftime("%H-%M")

                            def process_frame():
                                global recording1, recording2, recording3, start_time1, start_time2, start_time3, start_time4, writer1, writer2, writer3, writer4, end_time1, end_time2, end_time3, data1, data2, data3, data4, code_array1, code_array2, present_date, present_time, elapsed_time_str1, elapsed_time_str2, elapsed_time_str3, elapsed_time_str4
                                # CAM CCTV
                                ret1, frame1 = cap1.read()
                                cv2.putText(frame1, "CAM1", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret1:
                                    if recording1:
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
                                                    f"QR code {data1} detected for the first time at{elapsed_time_str1} on {present_date}-{present_time} ")
                                                scan1(data1, elapsed_time_str1, present_date, present_time, video_name1,
                                                      username)

                                            for qr_code1 in qr_codes1:
                                                (x, y, w, h) = qr_code1.rect
                                                cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code1.rect
                                                cv2.putText(frame1, data1, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

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
                                    cv2.imshow("Recording Camera cctv", blank_frame1)

                                # CAM2
                                ret2, frame2 = cap2.read()
                                cv2.putText(frame2, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret2:
                                    if recording2:
                                        qr_codes2 = decode(frame2)
                                        for qr_code2 in qr_codes2:
                                            data2 = qr_code2.data.decode('utf-8')
                                            if data2 not in first_detection_times2:
                                                first_detection_times2[data2] = cap2.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array2.append(data2)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data2} detected for the first time at{elapsed_time_str2} on {present_date}-{present_time} ")
                                                scan2(data2, elapsed_time_str2, present_date, present_time, video_name2,
                                                      username)

                                            for qr_code2 in qr_codes2:
                                                (x, y, w, h) = qr_code2.rect
                                                cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code2.rect
                                                cv2.putText(frame2, data2, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array2) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time2 is None:
                                            start_time2 = datetime.now()

                                        elapsed_time2 = datetime.now() - start_time2
                                        elapsed_time_str2 = str(elapsed_time2).split(".")[0]
                                        cv2.putText(frame2, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame2, f"START TIME:  {started_time2}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame2, f"DURATION:    {elapsed_time_str2}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame2, f"NO OF DATA:  {len(qr_codes_array2)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame2, f"LAST DATA:   {data2}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        writer2.write(frame2)
                                    cv2.imshow("Recording Camera 2", frame2)

                                if not ret2:
                                    blank_frame2 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame2, "CAM2 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 2", blank_frame2)

                                # CAM3
                                ret3, frame3 = cap3.read()
                                cv2.putText(frame3, "CAM3", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret3:
                                    if recording3:
                                        qr_codes3 = decode(frame3)
                                        for qr_code3 in qr_codes3:
                                            data3 = qr_code3.data.decode('utf-8')
                                            if data3 not in first_detection_times3:
                                                first_detection_times3[data3] = cap2.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array3.append(data3)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data3} detected for the first time at{elapsed_time_str3} on {present_date}-{present_time} ")
                                                scan3(data3, elapsed_time_str3, present_date, present_time, video_name3,
                                                      username)

                                            for qr_code3 in qr_codes3:
                                                (x, y, w, h) = qr_code3.rect
                                                cv2.rectangle(frame3, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code3.rect
                                                cv2.putText(frame3, data3, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array3) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time3 is None:
                                            start_time3 = datetime.now()

                                        elapsed_time3 = datetime.now() - start_time3
                                        elapsed_time_str3 = str(elapsed_time3).split(".")[0]
                                        cv2.putText(frame3, "CAM3", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame3, f"START TIME:  {started_time3}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame3, f"DURATION:    {elapsed_time_str3}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame3, f"NO OF DATA:  {len(qr_codes_array3)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame3, f"LAST DATA:   {data3}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        writer3.write(frame3)
                                    cv2.imshow("Recording Camera 3", frame3)

                                if not ret3:
                                    blank_frame3 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame3, "CAM3 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 3", blank_frame3)

                                # CAM4
                                ret4, frame4 = cap4.read()
                                cv2.putText(frame4, "CAM4", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret4:
                                    if recording4:
                                        qr_codes4 = decode(frame4)
                                        for qr_code4 in qr_codes4:
                                            data4 = qr_code4.data.decode('utf-8')
                                            if data4 not in first_detection_times4:
                                                first_detection_times4[data4] = cap2.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array4.append(data4)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data4} detected for the first time at{elapsed_time_str4} on {present_date}-{present_time} ")
                                                scan4(data4, elapsed_time_str4, present_date, present_time, video_name4,
                                                      username)

                                            for qr_code4 in qr_codes4:
                                                (x, y, w, h) = qr_code4.rect
                                                cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code4.rect
                                                cv2.putText(frame4, data4, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array4) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time4 is None:
                                            start_time4 = datetime.now()

                                        elapsed_time4 = datetime.now() - start_time4
                                        elapsed_time_str4 = str(elapsed_time4).split(".")[0]
                                        cv2.putText(frame4, "CAM4", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame4, f"START TIME:  {started_time4}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame4, f"DURATION:    {elapsed_time_str4}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame4, f"NO OF DATA:  {len(qr_codes_array4)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame4, f"LAST DATA:   {data4}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255),
                                                    1)
                                        writer4.write(frame4)
                                    cv2.imshow("Recording Camera 4", frame4)

                                if not ret4:
                                    blank_frame4 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame4, "CAM4 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 4", blank_frame4)

                                cv2.waitKey(1)
                                controller.after(1, process_frame)

                            def start():
                                start_recording1()
                                start_recording2()
                                start_recording3()
                                start_recording4()

                            def stop():
                                stop_recording1()
                                stop_recording2()
                                stop_recording3()
                                stop_recording4()

                            def close_window():
                                cap1.release()
                                cap2.release()
                                cap3.release()
                                cap4.release()
                                cv2.destroyAllWindows()
                                controller.destroy()

                            controller = tk.Tk()
                            controller.geometry("600x700")
                            controller.title("VIDEO CONTROLLER")
                            controller.resizable(0, 0)
                            start = tk.Button(controller, text="START", command=start)
                            start.place(x=80, y=20)
                            stop = tk.Button(controller, text="STOP", command=stop)
                            stop.place(x=180, y=20)
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
                            ####################    CAM2
                            cam2 = tk.Label(controller, text="CAMERA 2", fg='red')
                            cam2.place(x=20, y=240)
                            get_time2 = tk.Label(controller, text='Enter Time')
                            get_time2.place(x=60, y=270)
                            time2 = tk.Entry(controller)
                            time2.place(x=160, y=270)
                            start_button_2 = tk.Button(controller, text="START CAM2", command=start_recording2)
                            start_button_2.place(x=60, y=300)
                            stop_button_2 = tk.Button(controller, text="STOP CAM2", command=stop_recording2)
                            stop_button_2.place(x=160, y=300)
                            ####################    CAM2
                            Start_timing2 = tk.Label(controller, text="START TIME")
                            Start_timing2.place(x=60, y=330)
                            strt2 = tk.Label(controller, text="0:0")
                            strt2.place(x=210, y=330)
                            Duration_time2 = tk.Label(controller, text="DURATION")
                            Duration_time2.place(x=60, y=360)
                            drn2 = tk.Label(controller, text="0:0:0")
                            drn2.place(x=210, y=360)
                            NOD2 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD2.place(x=60, y=390)
                            num2 = tk.Label(controller, text="0")
                            num2.place(x=210, y=390)
                            ####################    CAM3
                            cam3 = tk.Label(controller, text="CAMERA 3", fg='violet')
                            cam3.place(x=20, y=420)
                            get_time3 = tk.Label(controller, text='Enter Time')
                            get_time3.place(x=60, y=450)
                            time3 = tk.Entry(controller)
                            time3.place(x=160, y=450)
                            start_button_3 = tk.Button(controller, text="START CAM3", command=start_recording3)
                            start_button_3.place(x=60, y=480)
                            stop_button_3 = tk.Button(controller, text="STOP CAM3", command=stop_recording3)
                            stop_button_3.place(x=160, y=480)
                            ####################    CAM3
                            Start_timing3 = tk.Label(controller, text="START TIME")
                            Start_timing3.place(x=60, y=510)
                            strt3 = tk.Label(controller, text="0:0")
                            strt3.place(x=210, y=510)
                            Duration_time3 = tk.Label(controller, text="DURATION")
                            Duration_time3.place(x=60, y=540)
                            drn3 = tk.Label(controller, text="0:0:0")
                            drn3.place(x=210, y=540)
                            NOD3 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD3.place(x=60, y=570)
                            num3 = tk.Label(controller, text="0")
                            num3.place(x=210, y=570)
                            ####################    CAM4
                            cam4 = tk.Label(controller, text="CAMERA 4", fg='skyblue')
                            cam4.place(x=320, y=60)
                            get_time4 = tk.Label(controller, text='Enter Time')
                            get_time4.place(x=360, y=90)
                            time4 = tk.Entry(controller)
                            time4.place(x=460, y=90)
                            start_button_4 = tk.Button(controller, text="START CAM4", command=start_recording4)
                            start_button_4.place(x=360, y=120)
                            stop_button_4 = tk.Button(controller, text="STOP CAM4", command=stop_recording4)
                            stop_button_4.place(x=460, y=120)
                            ####################    CAM4
                            Start_timing4 = tk.Label(controller, text="START TIME")
                            Start_timing4.place(x=360, y=150)
                            strt4 = tk.Label(controller, text="0:0")
                            strt4.place(x=510, y=150)
                            Duration_time4 = tk.Label(controller, text="DURATION")
                            Duration_time4.place(x=360, y=180)
                            drn4 = tk.Label(controller, text="0:0:0")
                            drn4.place(x=510, y=180)
                            NOD4 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD4.place(x=360, y=210)
                            num4 = tk.Label(controller, text="0")
                            num4.place(x=510, y=210)
                            ######################  CLOSE

                            close_button = tk.Button(controller, text="CLOSE", command=close_window)
                            close_button.place(x=130, y=640)

                            process_frame()
                            controller.mainloop()
                            cap1.release()
                            cap2.release()
                            cap3.release()
                            cap4.release()
                            cv2.destroyAllWindows()

                        elif selected_value == "5":

                            ################################    CAM1    RECORDING    ##################################
                            def start_recording1():
                                global recording1, start_time1, writer1, current_date, starting_time1, started_time1, elapsed_time_str1, first_detection_times1, camera1, data1, qr_codes_array1, video_name1
                                recording1 = True
                                data1 = ' '
                                start_time1 = None
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
                                global recording1, writer1, start_time1, elapsed_time_str1, code_array1
                                recording1 = False
                                print("Camera1 Stopped")
                                if writer1 is not None:
                                    writer1.release()

                                elapsed_time1 = datetime.now() - start_time1
                                elapsed_time_str1 = str(elapsed_time1).split(".")[0]
                                dur1 = elapsed_time_str1
                                code_array1 = len(qr_codes_array1)
                                print("no in 1 camera", code_array1)

                                if len(first_detection_times1) == 0:
                                    print("no")

                                else:
                                    strt1.config(text=started_time1)
                                    drn1.config(text=dur1)
                                    num1.config(text=code_array1)
                                    dispatch1(video_name1, elapsed_time_str1, len(qr_codes_array1), present_date,
                                              present_time, username)
                                    rec1_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record1data WHERE VIDEO_NAME = '{video_name1}'", rec1_data)
                                    df.to_excel(f"./{current_date}/{video_name1}.xlsx", index=False)
                                    rec1_data.close()

                            def start_recording2():
                                global recording2, start_time2, writer2, current_date, starting_time2, qr_codes_array2, data2, started_time2, camera2, first_detection_times2, elapsed_time_str2, video_name2
                                recording2 = True
                                start_time2 = None
                                data2 = ' '
                                qr_codes_array2 = []
                                first_detection_times2 = {}
                                live_time = datetime.now()
                                starting_time2 = current_time.strftime("%I-%M %p")
                                started_time2 = live_time.strftime("%I:%M %p")
                                num2.config(text=0)
                                strt2.config(text=0)
                                drn2.config(text=0)
                                camera2 = "CAM2"
                                time_2 = time2.get()
                                video_name2 = f'{camera2}-{time_2}'

                                print("Camera2 Recording")
                                writer2 = cv2.VideoWriter(f"./{current_date}/{video_name2}.mp4", fourcc1, 23.0,
                                                          (640, 480))

                            def stop_recording2():
                                global recording2, writer2, start_time2, code_array2, elapsed_time_str2
                                recording2 = False

                                if writer2 is not None:
                                    writer2.release()

                                elapsed_time2 = datetime.now() - start_time2
                                elapsed_time_str2 = str(elapsed_time2).split(".")[0]
                                dur2 = elapsed_time_str2
                                print("Camera2 stopped")
                                code_array2 = len(qr_codes_array2)
                                print("No Of detected QR codes in camera2:", code_array2)

                                if len(first_detection_times2) == 0:
                                    print("No data in camera2")

                                else:
                                    strt2.config(text=started_time2)
                                    drn2.config(text=dur2)
                                    num2.config(text=code_array2)

                                    dispatch2(video_name2, elapsed_time_str2, len(qr_codes_array2), present_date,
                                              present_time, username)

                                    rec2_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record2data WHERE VIDEO_NAME = '{video_name2}'", rec2_data)
                                    df.to_excel(f"./{current_date}/{video_name2}.xlsx", index=False)
                                    rec2_data.close()

                                    ################################    CAM3    RECORDING    ##################################

                            def start_recording3():
                                global recording3, start_time3, writer3, current_date, starting_time3, qr_codes_array3, data3, started_time3, camera3, elapsed_time_str3, first_detection_times3, video_name3
                                recording3 = True
                                start_time3 = None
                                data3 = ' '
                                qr_codes_array3 = []
                                camera3 = "CAM3"
                                time_3 = time3.get()
                                video_name3 = f'{camera3}-{time_3}'
                                live_time = datetime.now()
                                first_detection_times3 = {}
                                starting_time3 = current_time.strftime("%I-%M %p")
                                started_time3 = live_time.strftime("%I:%M %p")
                                start_time3 = None
                                print("Camera3 Recording")
                                writer3 = cv2.VideoWriter(f"./{current_date}/{camera3}-{starting_time}.mp4", fourcc3,
                                                          23.0, (640, 480))

                            def stop_recording3():
                                global recording3, writer3, start_time3, clip_name3, code_array3, elapsed_time_str3
                                recording3 = False
                                if writer3 is not None:
                                    writer3.release()
                                elapsed_time3 = datetime.now() - start_time3
                                elapsed_time_str3 = str(elapsed_time3).split(".")[0]
                                dur3 = elapsed_time_str3
                                print("Camera3 stopped")
                                code_array3 = len(qr_codes_array3)
                                print("No Of detected QR codes in camera3:", code_array3)

                                if len(first_detection_times3) == 0:
                                    print("No data")
                                else:
                                    strt3.config(text=started_time3)
                                    drn3.config(text=dur3)
                                    num3.config(text=code_array3)
                                    dispatch3(video_name3, elapsed_time_str3, len(qr_codes_array3), present_date,
                                              present_time, username)
                                    rec3_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record3data WHERE VIDEO_NAME = '{video_name3}'", rec3_data)
                                    df.to_excel(f"./{current_date}/{video_name3}.xlsx", index=False)
                                    rec3_data.close()

                                    ################################    CAM4    RECORDING    ##################################

                            def start_recording4():
                                global recording4, start_time4, writer4, current_data, starting_time4, qr_codes_array4, data4, started_time4, camera4, first_detection_times4, elapsed_time_str4, video_name4
                                recording4 = True
                                start_time4 = None
                                data4 = ' '
                                qr_codes_array4 = []
                                first_detection_times4 = {}
                                live_time = datetime.now()
                                starting_time4 = current_time.strftime("%I-%M %p")
                                started_time4 = live_time.strftime("%I:%M %p")
                                num4.config(text=0)
                                strt4.config(text=0)
                                drn4.config(text=0)
                                camera4 = "CAM4"
                                time_4 = time4.get()
                                video_name4 = f'{camera4}-{time_4}'
                                print("Camera4 Recording")
                                writer4 = cv2.VideoWriter(f"./{current_date}/{camera4}-{starting_time}.mp4", fourcc4,
                                                          23.0,
                                                          (640, 480))

                            def stop_recording4():
                                global recording4, writer4, start_time4, code_array4, elapsed_time_str4
                                recording4 = False
                                if writer4 is not None:
                                    writer4.release()
                                elapsed_time4 = datetime.now() - start_time4
                                elapsed_time_str4 = str(elapsed_time4).split(".")[0]
                                dur4 = elapsed_time_str4
                                print("Camera4 stopped")
                                code_array4 = len(qr_codes_array4)
                                print("No Of detected QR codes in camera4:", code_array4)
                                if len(first_detection_times4) == 0:
                                    print("No data in camera4")
                                else:
                                    strt4.config(text=started_time4)
                                    drn4.config(text=dur4)
                                    num4.config(text=code_array4)
                                    dispatch4(video_name4, elapsed_time_str4, len(qr_codes_array4), present_date,
                                              present_time, username)
                                    rec4_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record4data WHERE VIDEO_NAME = '{video_name4}'", rec4_data)
                                    df.to_excel(f"./{current_date}/{video_name4}.xlsx", index=False)
                                    rec4_data.close()

                            def start_recording5():
                                global recording5, start_time5, writer5, current_data, starting_time5, qr_codes_array5, data5, started_time5, camera5, first_detection_times5, elapsed_time_str5, video_name5
                                recording5 = True
                                start_time5 = None
                                data5 = ' '
                                qr_codes_array5 = []
                                first_detection_times5 = {}
                                live_time = datetime.now()
                                starting_time5 = current_time.strftime("%I-%M %p")
                                started_time5 = live_time.strftime("%I:%M %p")
                                num5.config(text=0)
                                strt5.config(text=0)
                                drn5.config(text=0)
                                camera5 = "CAM5"
                                time_5 = time5.get()
                                video_name5 = f'{camera5}-{time_5}'
                                print("Camera5 Recording")
                                writer5 = cv2.VideoWriter(f"./{current_date}/{camera5}-{starting_time}.mp4", fourcc5,
                                                          23.0,
                                                          (1280, 720))

                            def stop_recording5():
                                global recording5, writer5, start_time5, code_array5, elapsed_time_str5
                                recording5 = False
                                if writer5 is not None:
                                    writer5.release()
                                elapsed_time5 = datetime.now() - start_time5
                                elapsed_time_str5 = str(elapsed_time5).split(".")[0]
                                dur5 = elapsed_time_str5
                                print("Camera5 stopped")
                                code_array5 = len(qr_codes_array5)
                                print("No Of detected QR codes in camera5:", code_array5)
                                if len(first_detection_times5) == 0:
                                    print("No data in camera5")
                                else:
                                    strt5.config(text=started_time5)
                                    drn5.config(text=dur5)
                                    num5.config(text=code_array5)
                                    dispatch5(video_name5, elapsed_time_str5, len(qr_codes_array5), present_date,
                                              present_time, username)
                                    rec5_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record5data WHERE VIDEO_NAME = '{video_name5}'", rec5_data)
                                    df.to_excel(f"./{current_date}/{video_name5}.xlsx", index=False)
                                    rec5_data.close()

                            cap1 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
                            cap2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)
                            cap3 = cv2.VideoCapture(3, cv2.CAP_DSHOW)
                            cap4 = cv2.VideoCapture(4, cv2.CAP_DSHOW)
                            cap5 = cv2.VideoCapture(5, cv2.CAP_DSHOW)

                            cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap3.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap3.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap4.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap4.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap5.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap5.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            fourcc1 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time1 = datetime.now().strftime("%H-%M")
                            fourcc2 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time2 = datetime.now().strftime("%H-%M")
                            fourcc3 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time3 = datetime.now().strftime("%H-%M")
                            fourcc4 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time4 = datetime.now().strftime("%H-%M")
                            fourcc5 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time5 = datetime.now().strftime("%H-%M")

                            def process_frame():
                                global recording1, recording2, recording3, recording4, recording5, start_time1, start_time2, start_time3, start_time4, start_time5, writer1, writer2, writer3, writer4, writer5, end_time1, end_time2, end_time3, data1, data2, data3, data4, data5, code_array1, code_array2, present_date, present_time, elapsed_time_str1, elapsed_time_str2, elapsed_time_str3, elapsed_time_str4, elapsed_time_str5
                                # CAM CCTV
                                ret1, frame1 = cap1.read()
                                cv2.putText(frame1, "CAM1", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret1:
                                    if recording1:
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
                                                    f"QR code {data1} detected for the first time at{elapsed_time_str1} on {present_date}-{present_time} ")
                                                scan1(data1, elapsed_time_str1, present_date, present_time, video_name1,
                                                      username)

                                            for qr_code1 in qr_codes1:
                                                (x, y, w, h) = qr_code1.rect
                                                cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code1.rect
                                                cv2.putText(frame1, data1, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array1) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time1 is None:
                                            start_time1 = datetime.now()

                                        elapsed_time1 = datetime.now() - start_time1
                                        elapsed_time_str1 = str(elapsed_time1).split(".")[0]
                                        cv2.putText(frame1, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
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
                                    cv2.imshow("Recording Camera cctv", blank_frame1)

                                # CAM2
                                ret2, frame2 = cap2.read()
                                cv2.putText(frame2, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret2:
                                    if recording2:
                                        qr_codes2 = decode(frame2)
                                        for qr_code2 in qr_codes2:
                                            data2 = qr_code2.data.decode('utf-8')
                                            if data2 not in first_detection_times2:
                                                first_detection_times2[data2] = cap2.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array2.append(data2)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data2} detected for the first time at{elapsed_time_str2} on {present_date}-{present_time} ")
                                                scan2(data2, elapsed_time_str2, present_date, present_time, video_name2,
                                                      username)

                                            for qr_code2 in qr_codes2:
                                                (x, y, w, h) = qr_code2.rect
                                                cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code2.rect
                                                cv2.putText(frame2, data2, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array2) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time2 is None:
                                            start_time2 = datetime.now()

                                        elapsed_time2 = datetime.now() - start_time2
                                        elapsed_time_str2 = str(elapsed_time2).split(".")[0]
                                        cv2.putText(frame2, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame2, f"START TIME:  {started_time2}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame2, f"DURATION:    {elapsed_time_str2}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame2, f"NO OF DATA:  {len(qr_codes_array2)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame2, f"LAST DATA:   {data2}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255),
                                                    1)
                                        writer2.write(frame2)
                                    cv2.imshow("Recording Camera 2", frame2)

                                if not ret2:
                                    blank_frame2 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame2, "CAM2 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 2", blank_frame2)

                                # CAM3
                                ret3, frame3 = cap3.read()
                                cv2.putText(frame3, "CAM3", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret3:
                                    if recording3:
                                        qr_codes3 = decode(frame3)
                                        for qr_code3 in qr_codes3:
                                            data3 = qr_code3.data.decode('utf-8')
                                            if data3 not in first_detection_times3:
                                                first_detection_times3[data3] = cap3.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array3.append(data3)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data3} detected for the first time at{elapsed_time_str3} on {present_date}-{present_time} ")
                                                scan3(data3, elapsed_time_str3, present_date, present_time, video_name3,
                                                      username)

                                            for qr_code3 in qr_codes3:
                                                (x, y, w, h) = qr_code3.rect
                                                cv2.rectangle(frame3, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code3.rect
                                                cv2.putText(frame3, data3, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array3) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time3 is None:
                                            start_time3 = datetime.now()

                                        elapsed_time3 = datetime.now() - start_time3
                                        elapsed_time_str3 = str(elapsed_time3).split(".")[0]
                                        cv2.putText(frame3, "CAM3", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame3, f"START TIME:  {started_time3}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame3, f"DURATION:    {elapsed_time_str3}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame3, f"NO OF DATA:  {len(qr_codes_array3)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame3, f"LAST DATA:   {data3}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255),
                                                    1)
                                        writer3.write(frame3)
                                    cv2.imshow("Recording Camera 3", frame3)

                                if not ret3:
                                    blank_frame3 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame3, "CAM3 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 3", blank_frame3)

                                # CAM4
                                ret4, frame4 = cap4.read()
                                cv2.putText(frame4, "CAM4", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret4:
                                    if recording4:
                                        qr_codes4 = decode(frame4)
                                        for qr_code4 in qr_codes4:
                                            data4 = qr_code4.data.decode('utf-8')
                                            if data4 not in first_detection_times4:
                                                first_detection_times4[data4] = cap4.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array4.append(data4)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data4} detected for the first time at{elapsed_time_str4} on {present_date}-{present_time} ")
                                                scan4(data4, elapsed_time_str4, present_date, present_time, video_name4,
                                                      username)

                                            for qr_code4 in qr_codes4:
                                                (x, y, w, h) = qr_code4.rect
                                                cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code4.rect
                                                cv2.putText(frame4, data4, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array4) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time4 is None:
                                            start_time4 = datetime.now()

                                        elapsed_time4 = datetime.now() - start_time4
                                        elapsed_time_str4 = str(elapsed_time4).split(".")[0]
                                        cv2.putText(frame4, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame4, f"START TIME:  {started_time4}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame4, f"DURATION:    {elapsed_time_str4}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame4, f"NO OF DATA:  {len(qr_codes_array4)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame4, f"LAST DATA:   {data4}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255),
                                                    1)
                                        writer4.write(frame4)
                                    cv2.imshow("Recording Camera 4", frame4)

                                if not ret4:
                                    blank_frame4 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame4, "CAM4 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 4", blank_frame4)
                                # CAM5
                                ret5, frame5 = cap5.read()
                                cv2.putText(frame5, "CAM5", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret5:
                                    if recording5:
                                        qr_codes5 = decode(frame5)
                                        for qr_code5 in qr_codes5:
                                            data5 = qr_code5.data.decode('utf-8')
                                            if data5 not in first_detection_times5:
                                                first_detection_times5[data5] = cap5.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array5.append(data5)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data5} detected for the first time at{elapsed_time_str5} on {present_date}-{present_time} ")
                                                scan5(data5, elapsed_time_str5, present_date, present_time, video_name5,
                                                      username)

                                            for qr_code5 in qr_codes5:
                                                (x, y, w, h) = qr_code5.rect
                                                cv2.rectangle(frame5, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code5.rect
                                                cv2.putText(frame5, data5, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array5) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time5 is None:
                                            start_time5 = datetime.now()

                                        elapsed_time5 = datetime.now() - start_time5
                                        elapsed_time_str5 = str(elapsed_time5).split(".")[0]
                                        cv2.putText(frame5, "CAM5", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame5, f"START TIME:  {started_time5}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame5, f"DURATION:    {elapsed_time_str5}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame5, f"NO OF DATA:  {len(qr_codes_array5)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame5, f"LAST DATA:   {data5}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255),
                                                    1)
                                        writer5.write(frame5)
                                    cv2.imshow("Recording Camera 5", frame5)

                                if not ret5:
                                    blank_frame5 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame5, "CAM5 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 5", blank_frame5)

                                cv2.waitKey(1)
                                controller.after(1, process_frame)

                            def start():
                                start_recording1()
                                start_recording2()
                                start_recording3()
                                start_recording4()
                                start_recording5()

                            def stop():
                                stop_recording1()
                                stop_recording2()
                                stop_recording3()
                                stop_recording4()
                                stop_recording5()

                            def close_window():
                                cap1.release()
                                cap2.release()
                                cap3.release()
                                cap4.release()
                                cap5.release()
                                cv2.destroyAllWindows()
                                controller.destroy()

                            controller = tk.Tk()
                            controller.geometry("600x700")
                            controller.title("VIDEO CONTROLLER")
                            controller.resizable(0, 0)
                            start = tk.Button(controller, text="START", command=start)
                            start.place(x=80, y=20)
                            stop = tk.Button(controller, text="STOP", command=stop)
                            stop.place(x=180, y=20)
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
                            ####################    CAM2
                            cam2 = tk.Label(controller, text="CAMERA 2", fg='red')
                            cam2.place(x=20, y=240)
                            get_time2 = tk.Label(controller, text='Enter Time')
                            get_time2.place(x=60, y=270)
                            time2 = tk.Entry(controller)
                            time2.place(x=160, y=270)
                            start_button_2 = tk.Button(controller, text="START CAM2", command=start_recording2)
                            start_button_2.place(x=60, y=300)
                            stop_button_2 = tk.Button(controller, text="STOP CAM2", command=stop_recording2)
                            stop_button_2.place(x=160, y=300)
                            ####################    CAM2
                            Start_timing2 = tk.Label(controller, text="START TIME")
                            Start_timing2.place(x=60, y=330)
                            strt2 = tk.Label(controller, text="0:0")
                            strt2.place(x=210, y=330)
                            Duration_time2 = tk.Label(controller, text="DURATION")
                            Duration_time2.place(x=60, y=360)
                            drn2 = tk.Label(controller, text="0:0:0")
                            drn2.place(x=210, y=360)
                            NOD2 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD2.place(x=60, y=390)
                            num2 = tk.Label(controller, text="0")
                            num2.place(x=210, y=390)
                            ####################    CAM3
                            cam3 = tk.Label(controller, text="CAMERA 3", fg='violet')
                            cam3.place(x=20, y=420)
                            get_time3 = tk.Label(controller, text='Enter Time')
                            get_time3.place(x=60, y=450)
                            time3 = tk.Entry(controller)
                            time3.place(x=160, y=450)
                            start_button_3 = tk.Button(controller, text="START CAM3", command=start_recording3)
                            start_button_3.place(x=60, y=480)
                            stop_button_3 = tk.Button(controller, text="STOP CAM3", command=stop_recording3)
                            stop_button_3.place(x=160, y=480)
                            ####################    CAM3
                            Start_timing3 = tk.Label(controller, text="START TIME")
                            Start_timing3.place(x=60, y=510)
                            strt3 = tk.Label(controller, text="0:0")
                            strt3.place(x=210, y=510)
                            Duration_time3 = tk.Label(controller, text="DURATION")
                            Duration_time3.place(x=60, y=540)
                            drn3 = tk.Label(controller, text="0:0:0")
                            drn3.place(x=210, y=540)
                            NOD3 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD3.place(x=60, y=570)
                            num3 = tk.Label(controller, text="0")
                            num3.place(x=210, y=570)
                            ####################    CAM4
                            cam4 = tk.Label(controller, text="CAMERA 4", fg='skyblue')
                            cam4.place(x=320, y=60)
                            get_time4 = tk.Label(controller, text='Enter Time')
                            get_time4.place(x=360, y=90)
                            time4 = tk.Entry(controller)
                            time4.place(x=460, y=90)
                            start_button_4 = tk.Button(controller, text="START CAM4", command=start_recording4)
                            start_button_4.place(x=360, y=120)
                            stop_button_4 = tk.Button(controller, text="STOP CAM4", command=stop_recording4)
                            stop_button_4.place(x=460, y=120)
                            ####################    CAM4
                            Start_timing4 = tk.Label(controller, text="START TIME")
                            Start_timing4.place(x=360, y=150)
                            strt4 = tk.Label(controller, text="0:0")
                            strt4.place(x=510, y=150)
                            Duration_time4 = tk.Label(controller, text="DURATION")
                            Duration_time4.place(x=360, y=180)
                            drn4 = tk.Label(controller, text="0:0:0")
                            drn4.place(x=510, y=180)
                            NOD4 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD4.place(x=360, y=210)
                            num4 = tk.Label(controller, text="0")
                            num4.place(x=510, y=210)
                            ####################    CAM5
                            cam5 = tk.Label(controller, text="CAMERA 5", fg='black')
                            cam5.place(x=320, y=240)
                            get_time5 = tk.Label(controller, text='Enter Time')
                            get_time5.place(x=360, y=270)
                            time5 = tk.Entry(controller)
                            time5.place(x=460, y=270)
                            start_button_5 = tk.Button(controller, text="START CAM5", command=start_recording5)
                            start_button_5.place(x=360, y=300)
                            stop_button_5 = tk.Button(controller, text="STOP CAM5", command=stop_recording5)
                            stop_button_5.place(x=460, y=300)
                            ####################    CAM5
                            Start_timing5 = tk.Label(controller, text="START TIME")
                            Start_timing5.place(x=360, y=330)
                            strt5 = tk.Label(controller, text="0:0")
                            strt5.place(x=510, y=330)
                            Duration_time5 = tk.Label(controller, text="DURATION")
                            Duration_time5.place(x=360, y=360)
                            drn5 = tk.Label(controller, text="0:0:0")
                            drn5.place(x=510, y=360)
                            NOD5 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD5.place(x=360, y=390)
                            num5 = tk.Label(controller, text="0")
                            num5.place(x=510, y=390)

                            ######################  CLOSE

                            close_button = tk.Button(controller, text="CLOSE", command=close_window)
                            close_button.place(x=130, y=640)

                            process_frame()
                            controller.mainloop()
                            cap1.release()
                            cap2.release()
                            cap3.release()
                            cap4.release()
                            cv2.destroyAllWindows()

                        elif selected_value == "6":

                            ################################    CAM1    RECORDING    ##################################
                            def start_recording1():
                                global recording1, start_time1, writer1, current_date, starting_time1, started_time1, elapsed_time_str1, first_detection_times1, camera1, data1, qr_codes_array1, video_name1
                                recording1 = True
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
                                writer1 = cv2.VideoWriter(f"./{current_date}/{camera1}-{starting_time}.mp4", fourcc1,
                                                          23.0, (640, 480))

                            def stop_recording1():
                                global recording1, writer1, start_time1, elapsed_time_str1, code_array1
                                recording1 = False
                                print("Camera1 Stopped")
                                if writer1 is not None:
                                    writer1.release()

                                elapsed_time1 = datetime.now() - start_time1
                                elapsed_time_str1 = str(elapsed_time1).split(".")[0]
                                dur1 = elapsed_time_str1
                                code_array1 = len(qr_codes_array1)
                                print("no in 1 camera", code_array1)

                                if len(first_detection_times1) == 0:
                                    print("no")

                                else:
                                    strt1.config(text=started_time1)
                                    drn1.config(text=dur1)
                                    num1.config(text=code_array1)
                                    dispatch1(video_name1, elapsed_time_str1, len(qr_codes_array1), present_date,
                                              present_time, username)
                                    rec1_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record1data WHERE VIDEO_NAME = '{video_name1}'", rec1_data)
                                    df.to_excel(f"./{current_date}/{video_name1}.xlsx", index=False)
                                    rec1_data.close()

                            def start_recording2():
                                global recording2, start_time2, writer2, current_date, starting_time2, qr_codes_array2, data2, started_time2, camera2, first_detection_times2, elapsed_time_str2, video_name2
                                recording2 = True
                                start_time2 = None
                                data2 = ' '
                                qr_codes_array2 = []
                                first_detection_times2 = {}
                                live_time = datetime.now()
                                starting_time2 = current_time.strftime("%I-%M %p")
                                started_time2 = live_time.strftime("%I:%M %p")
                                num2.config(text=0)
                                strt2.config(text=0)
                                drn2.config(text=0)
                                camera2 = "CAM2"
                                time_2 = time2.get()
                                video_name2 = f'{camera2}-{time_2}'

                                print("Camera2 Recording")
                                writer2 = cv2.VideoWriter(f"./{current_date}/{camera2}-{starting_time}.mp4", fourcc2,
                                                          23.0, (640, 480))

                            def stop_recording2():
                                global recording2, writer2, start_time2, code_array2, elapsed_time_str2
                                recording2 = False

                                if writer2 is not None:
                                    writer2.release()

                                elapsed_time2 = datetime.now() - start_time2
                                elapsed_time_str2 = str(elapsed_time2).split(".")[0]
                                dur2 = elapsed_time_str2
                                print("Camera2 stopped")
                                code_array2 = len(qr_codes_array2)
                                print("No Of detected QR codes in camera2:", code_array2)

                                if len(first_detection_times2) == 0:
                                    print("No data in camera2")

                                else:
                                    strt2.config(text=started_time2)
                                    drn2.config(text=dur2)
                                    num2.config(text=code_array2)

                                    dispatch2(video_name2, elapsed_time_str2, len(qr_codes_array2), present_date,
                                              present_time, username)

                                    rec2_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record2data WHERE VIDEO_NAME = '{video_name2}'", rec2_data)
                                    df.to_excel(f"./{current_date}/{video_name2}.xlsx", index=False)
                                    rec2_data.close()

                                    ################################    CAM3    RECORDING    ##################################

                            def start_recording3():
                                global recording3, start_time3, writer3, current_date, starting_time3, qr_codes_array3, data3, started_time3, camera3, elapsed_time_str3, first_detection_times3, video_name3
                                recording3 = True
                                start_time3 = None
                                data3 = ' '
                                qr_codes_array3 = []
                                camera3 = "CAM3"
                                time_3 = time3.get()
                                video_name3 = f'{camera3}-{time_3}'
                                live_time = datetime.now()
                                first_detection_times3 = {}
                                starting_time3 = current_time.strftime("%I-%M %p")
                                started_time3 = live_time.strftime("%I:%M %p")
                                start_time3 = None
                                print("Camera3 Recording")
                                writer3 = cv2.VideoWriter(f"./{current_date}/{camera3}-{starting_time}.mp4", fourcc3,
                                                          23.0, (640, 480))

                            def stop_recording3():
                                global recording3, writer3, start_time3, clip_name3, code_array3, elapsed_time_str3
                                recording3 = False
                                if writer3 is not None:
                                    writer3.release()
                                elapsed_time3 = datetime.now() - start_time3
                                elapsed_time_str3 = str(elapsed_time3).split(".")[0]
                                dur3 = elapsed_time_str3
                                print("Camera3 stopped")
                                code_array3 = len(qr_codes_array3)
                                print("No Of detected QR codes in camera3:", code_array3)

                                if len(first_detection_times3) == 0:
                                    print("No data")
                                else:
                                    strt3.config(text=started_time3)
                                    drn3.config(text=dur3)
                                    num3.config(text=code_array3)
                                    dispatch3(video_name3, elapsed_time_str3, len(qr_codes_array3), present_date,
                                              present_time, username)
                                    rec3_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record3data WHERE VIDEO_NAME = '{video_name3}'", rec3_data)
                                    df.to_excel(f"./{current_date}/{video_name3}.xlsx", index=False)
                                    rec3_data.close()

                                    ################################    CAM4    RECORDING    ##################################

                            def start_recording4():
                                global recording4, start_time4, writer4, current_data, starting_time4, qr_codes_array4, data4, started_time4, camera4, first_detection_times4, elapsed_time_str4, video_name4
                                recording4 = True
                                start_time4 = None
                                data4 = ' '
                                qr_codes_array4 = []
                                first_detection_times4 = {}
                                live_time = datetime.now()
                                starting_time4 = current_time.strftime("%I-%M %p")
                                started_time4 = live_time.strftime("%I:%M %p")
                                num4.config(text=0)
                                strt4.config(text=0)
                                drn4.config(text=0)
                                camera4 = "CAM4"
                                time_4 = time4.get()
                                video_name4 = f'{camera4}-{time_4}'
                                print("Camera4 Recording")
                                writer4 = cv2.VideoWriter(f"./{current_date}/{camera4}-{starting_time}.mp4", fourcc4,
                                                          23.0,
                                                          (640, 480))

                            def stop_recording4():
                                global recording4, writer4, start_time4, code_array4, elapsed_time_str4
                                recording4 = False
                                if writer4 is not None:
                                    writer4.release()
                                elapsed_time4 = datetime.now() - start_time4
                                elapsed_time_str4 = str(elapsed_time4).split(".")[0]
                                dur4 = elapsed_time_str4
                                print("Camera4 stopped")
                                code_array4 = len(qr_codes_array4)
                                print("No Of detected QR codes in camera4:", code_array4)
                                if len(first_detection_times4) == 0:
                                    print("No data in camera4")
                                else:
                                    strt4.config(text=started_time4)
                                    drn4.config(text=dur4)
                                    num4.config(text=code_array4)
                                    dispatch4(video_name4, elapsed_time_str4, len(qr_codes_array4), present_date,
                                              present_time, username)
                                    rec4_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record4data WHERE VIDEO_NAME = '{video_name4}'", rec4_data)
                                    df.to_excel(f"./{current_date}/{video_name4}.xlsx", index=False)
                                    rec4_data.close()

                            def start_recording5():
                                global recording5, start_time5, writer5, current_data, starting_time5, qr_codes_array5, data5, started_time5, camera5, first_detection_times5, elapsed_time_str5, video_name5
                                recording5 = True
                                start_time5 = None
                                data5 = ' '
                                qr_codes_array5 = []
                                first_detection_times5 = {}
                                live_time = datetime.now()
                                starting_time5 = current_time.strftime("%I-%M %p")
                                started_time5 = live_time.strftime("%I:%M %p")
                                num5.config(text=0)
                                strt5.config(text=0)
                                drn5.config(text=0)
                                camera5 = "CAM5"
                                time_5 = time5.get()
                                video_name5 = f'{camera5}-{time_5}'
                                print("Camera5 Recording")
                                writer5 = cv2.VideoWriter(f"./{current_date}/{camera5}-{starting_time}.mp4", fourcc5,
                                                          23.0,
                                                          (640, 480))

                            def stop_recording5():
                                global recording5, writer5, start_time5, code_array5, elapsed_time_str5
                                recording5 = False
                                if writer5 is not None:
                                    writer5.release()
                                elapsed_time5 = datetime.now() - start_time5
                                elapsed_time_str5 = str(elapsed_time5).split(".")[0]
                                dur5 = elapsed_time_str5
                                print("Camera5 stopped")
                                code_array5 = len(qr_codes_array5)
                                print("No Of detected QR codes in camera5:", code_array5)
                                if len(first_detection_times5) == 0:
                                    print("No data in camera5")
                                else:
                                    strt5.config(text=started_time5)
                                    drn5.config(text=dur5)
                                    num5.config(text=code_array5)
                                    dispatch5(video_name5, elapsed_time_str5, len(qr_codes_array5), present_date,
                                              present_time, username)
                                    rec5_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record5data WHERE VIDEO_NAME = '{video_name5}'", rec5_data)
                                    df.to_excel(f"./{current_date}/{video_name5}.xlsx", index=False)
                                    rec5_data.close()

                            def start_recording6():
                                global recording6, start_time6, writer6, current_data, starting_time6, qr_codes_array6, data6, started_time6, camera6, first_detection_times6, elapsed_time_str6, video_name6
                                recording6 = True
                                start_time6 = None
                                data6 = ' '
                                qr_codes_array6 = []
                                first_detection_times6 = {}
                                live_time = datetime.now()
                                starting_time6 = current_time.strftime("%I-%M %p")
                                started_time6 = live_time.strftime("%I:%M %p")
                                num6.config(text=0)
                                strt6.config(text=0)
                                drn6.config(text=0)
                                camera6 = "CAM6"
                                time_6 = time6.get()
                                video_name6 = f'{camera6}-{time_6}'
                                print("Camera6 Recording")
                                writer6 = cv2.VideoWriter(f"./{current_date}/{camera6}-{starting_time}.mp4", fourcc6,
                                                          23.0,
                                                          (640, 480))

                            def stop_recording6():
                                global recording6, writer6, start_time6, code_array6, elapsed_time_str6
                                recording6 = False
                                if writer6 is not None:
                                    writer6.release()
                                elapsed_time6 = datetime.now() - start_time6
                                elapsed_time_str6 = str(elapsed_time6).split(".")[0]
                                dur6 = elapsed_time_str6
                                print("Camera6 stopped")
                                code_array6 = len(qr_codes_array6)
                                print("No Of detected QR codes in camera6:", code_array6)
                                if len(first_detection_times6) == 0:
                                    print("No data in camera6")
                                else:
                                    strt6.config(text=started_time6)
                                    drn6.config(text=dur6)
                                    num6.config(text=code_array6)
                                    dispatch6(video_name6, elapsed_time_str6, len(qr_codes_array6), present_date,
                                              present_time, username)
                                    rec6_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record6data WHERE VIDEO_NAME = '{video_name6}'", rec6_data)
                                    df.to_excel(f"./{current_date}/{video_name6}.xlsx", index=False)
                                    rec6_data.close()

                            cap1 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
                            cap2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)
                            cap3 = cv2.VideoCapture(3, cv2.CAP_DSHOW)
                            cap4 = cv2.VideoCapture(4, cv2.CAP_DSHOW)
                            cap5 = cv2.VideoCapture(5, cv2.CAP_DSHOW)
                            cap6 = cv2.VideoCapture(6, cv2.CAP_DSHOW)

                            cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap3.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap3.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap4.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap4.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap5.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap5.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap6.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap6.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            fourcc1 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time1 = datetime.now().strftime("%H-%M")
                            fourcc2 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time2 = datetime.now().strftime("%H-%M")
                            fourcc3 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time3 = datetime.now().strftime("%H-%M")
                            fourcc4 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time4 = datetime.now().strftime("%H-%M")
                            fourcc5 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time5 = datetime.now().strftime("%H-%M")
                            fourcc6 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time6 = datetime.now().strftime("%H-%M")

                            def process_frame():
                                global recording1, recording2, recording3, recording4, recording5, recording6, start_time1, start_time2, start_time3, start_time4, start_time5, start_time6, writer1, writer2, writer3, writer4, writer5, writer6, end_time1, end_time2, end_time3, data1, data2, data3, data4, data5, data6, code_array1, code_array2, present_date, present_time, elapsed_time_str1, elapsed_time_str2, elapsed_time_str3, elapsed_time_str4, elapsed_time_str5, elapsed_time_str6
                                # CAM CCTV
                                ret1, frame1 = cap1.read()
                                cv2.putText(frame1, "CAM1", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret1:
                                    if recording1:
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
                                                    f"QR code {data1} detected for the first time at{elapsed_time_str1} on {present_date}-{present_time} ")
                                                scan1(data1, elapsed_time_str1, present_date, present_time, video_name1,
                                                      username)

                                            for qr_code1 in qr_codes1:
                                                (x, y, w, h) = qr_code1.rect
                                                cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code1.rect
                                                cv2.putText(frame1, data1, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array1) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time1 is None:
                                            start_time1 = datetime.now()

                                        elapsed_time1 = datetime.now() - start_time1
                                        elapsed_time_str1 = str(elapsed_time1).split(".")[0]
                                        cv2.putText(frame1, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
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
                                    cv2.imshow("Recording Camera cctv", blank_frame1)

                                # CAM2
                                ret2, frame2 = cap2.read()
                                cv2.putText(frame2, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret2:
                                    if recording2:
                                        qr_codes2 = decode(frame2)
                                        for qr_code2 in qr_codes2:
                                            data2 = qr_code2.data.decode('utf-8')
                                            if data2 not in first_detection_times2:
                                                first_detection_times2[data2] = cap2.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array2.append(data2)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data2} detected for the first time at{elapsed_time_str2} on {present_date}-{present_time} ")
                                                scan2(data2, elapsed_time_str2, present_date, present_time, video_name2,
                                                      username)

                                            for qr_code2 in qr_codes2:
                                                (x, y, w, h) = qr_code2.rect
                                                cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code2.rect
                                                cv2.putText(frame2, data2, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array2) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time2 is None:
                                            start_time2 = datetime.now()

                                        elapsed_time2 = datetime.now() - start_time2
                                        elapsed_time_str2 = str(elapsed_time2).split(".")[0]
                                        cv2.putText(frame2, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame2, f"START TIME:  {started_time2}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame2, f"DURATION:    {elapsed_time_str2}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame2, f"NO OF DATA:  {len(qr_codes_array2)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame2, f"LAST DATA:   {data2}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255),
                                                    1)
                                        writer2.write(frame2)
                                    cv2.imshow("Recording Camera 2", frame2)

                                if not ret2:
                                    blank_frame2 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame2, "CAM2 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 2", blank_frame2)

                                # CAM3
                                ret3, frame3 = cap3.read()
                                cv2.putText(frame3, "CAM3", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret3:
                                    if recording3:
                                        qr_codes3 = decode(frame3)
                                        for qr_code3 in qr_codes3:
                                            data3 = qr_code3.data.decode('utf-8')
                                            if data3 not in first_detection_times3:
                                                first_detection_times3[data3] = cap3.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array3.append(data3)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data3} detected for the first time at{elapsed_time_str3} on {present_date}-{present_time} ")
                                                scan3(data3, elapsed_time_str3, present_date, present_time, video_name3,
                                                      username)

                                            for qr_code3 in qr_codes3:
                                                (x, y, w, h) = qr_code3.rect
                                                cv2.rectangle(frame3, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code3.rect
                                                cv2.putText(frame3, data3, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array3) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time3 is None:
                                            start_time3 = datetime.now()

                                        elapsed_time3 = datetime.now() - start_time3
                                        elapsed_time_str3 = str(elapsed_time3).split(".")[0]
                                        cv2.putText(frame3, "CAM3", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame3, f"START TIME:  {started_time3}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame3, f"DURATION:    {elapsed_time_str3}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame3, f"NO OF DATA:  {len(qr_codes_array3)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame3, f"LAST DATA:   {data3}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255),
                                                    1)
                                        writer3.write(frame3)
                                    cv2.imshow("Recording Camera 3", frame3)

                                if not ret3:
                                    blank_frame3 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame3, "CAM3 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 3", blank_frame3)

                                # CAM4
                                ret4, frame4 = cap4.read()
                                cv2.putText(frame4, "CAM4", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret4:
                                    if recording4:
                                        qr_codes4 = decode(frame4)
                                        for qr_code4 in qr_codes4:
                                            data4 = qr_code4.data.decode('utf-8')
                                            if data4 not in first_detection_times4:
                                                first_detection_times4[data4] = cap4.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array4.append(data4)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data4} detected for the first time at{elapsed_time_str4} on {present_date}-{present_time} ")
                                                scan4(data4, elapsed_time_str4, present_date, present_time, video_name4,
                                                      username)

                                            for qr_code4 in qr_codes4:
                                                (x, y, w, h) = qr_code4.rect
                                                cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code4.rect
                                                cv2.putText(frame4, data4, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array4) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time4 is None:
                                            start_time4 = datetime.now()

                                        elapsed_time4 = datetime.now() - start_time4
                                        elapsed_time_str4 = str(elapsed_time4).split(".")[0]
                                        cv2.putText(frame4, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame4, f"START TIME:  {started_time4}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame4, f"DURATION:    {elapsed_time_str4}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame4, f"NO OF DATA:  {len(qr_codes_array4)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame4, f"LAST DATA:   {data4}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255),
                                                    1)
                                        writer4.write(frame4)
                                    cv2.imshow("Recording Camera 4", frame4)

                                if not ret4:
                                    blank_frame4 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame4, "CAM4 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 4", blank_frame4)
                                # CAM5
                                ret5, frame5 = cap5.read()
                                cv2.putText(frame5, "CAM5", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret5:
                                    if recording5:
                                        qr_codes5 = decode(frame5)
                                        for qr_code5 in qr_codes5:
                                            data5 = qr_code5.data.decode('utf-8')
                                            if data5 not in first_detection_times5:
                                                first_detection_times5[data5] = cap5.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array5.append(data5)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data5} detected for the first time at{elapsed_time_str5} on {present_date}-{present_time} ")
                                                scan5(data5, elapsed_time_str5, present_date, present_time, video_name5,
                                                      username)

                                            for qr_code5 in qr_codes5:
                                                (x, y, w, h) = qr_code5.rect
                                                cv2.rectangle(frame5, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code5.rect
                                                cv2.putText(frame5, data5, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array5) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time5 is None:
                                            start_time5 = datetime.now()

                                        elapsed_time5 = datetime.now() - start_time5
                                        elapsed_time_str5 = str(elapsed_time5).split(".")[0]
                                        cv2.putText(frame5, "CAM5", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame5, f"START TIME:  {started_time5}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame5, f"DURATION:    {elapsed_time_str5}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame5, f"NO OF DATA:  {len(qr_codes_array5)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame5, f"LAST DATA:   {data5}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255),
                                                    1)
                                        writer5.write(frame5)
                                    cv2.imshow("Recording Camera 5", frame5)

                                if not ret5:
                                    blank_frame5 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame5, "CAM5 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 5", blank_frame5)

                                # CAM6
                                ret6, frame6 = cap6.read()
                                cv2.putText(frame6, "CAM6", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret6:
                                    if recording6:
                                        qr_codes6 = decode(frame6)
                                        for qr_code6 in qr_codes6:
                                            data6 = qr_code6.data.decode('utf-8')
                                            if data6 not in first_detection_times6:
                                                first_detection_times6[data6] = cap6.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array6.append(data6)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)

                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')
                                                print(
                                                    f"QR code {data6} detected for the first time at{elapsed_time_str6} on {present_date}-{present_time} ")
                                                scan6(data6, elapsed_time_str6, present_date, present_time, video_name6,
                                                      username)

                                            for qr_code6 in qr_codes6:
                                                (x, y, w, h) = qr_code6.rect
                                                cv2.rectangle(frame6, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code6.rect
                                                cv2.putText(frame6, data6, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array6) == 0:
                                                print("No QR codes detected!!!!!")
                                        if start_time6 is None:
                                            start_time6 = datetime.now()
                                        elapsed_time6 = datetime.now() - start_time6
                                        elapsed_time_str6 = str(elapsed_time6).split(".")[0]
                                        cv2.putText(frame6, "CAM5", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame6, f"START TIME:  {started_time6}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame6, f"DURATION:    {elapsed_time_str6}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame6, f"NO OF DATA:  {len(qr_codes_array6)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame6, f"LAST DATA:   {data6}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255),
                                                    1)
                                        writer6.write(frame6)
                                    cv2.imshow("Recording Camera 6", frame6)
                                if not ret6:
                                    blank_frame6 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame6, "CAM6 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 6", blank_frame6)

                                cv2.waitKey(1)
                                controller.after(1, process_frame)

                            def start():
                                start_recording1()
                                start_recording2()
                                start_recording3()
                                start_recording4()
                                start_recording5()
                                start_recording6()

                            def stop():
                                stop_recording1()
                                stop_recording2()
                                stop_recording3()
                                stop_recording4()
                                stop_recording5()
                                stop_recording6()

                            def close_window():
                                cap1.release()
                                cap2.release()
                                cap3.release()
                                cap4.release()
                                cap5.release()
                                cap6.release()
                                cv2.destroyAllWindows()
                                controller.destroy()

                            controller = tk.Tk()
                            controller.geometry("600x700")
                            controller.title("VIDEO CONTROLLER")
                            controller.resizable(0, 0)
                            start = tk.Button(controller, text="START", command=start)
                            start.place(x=80, y=20)
                            stop = tk.Button(controller, text="STOP", command=stop)
                            stop.place(x=180, y=20)
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
                            ####################    CAM2
                            cam2 = tk.Label(controller, text="CAMERA 2", fg='red')
                            cam2.place(x=20, y=240)
                            get_time2 = tk.Label(controller, text='Enter Time')
                            get_time2.place(x=60, y=270)
                            time2 = tk.Entry(controller)
                            time2.place(x=160, y=270)
                            start_button_2 = tk.Button(controller, text="START CAM2", command=start_recording2)
                            start_button_2.place(x=60, y=300)
                            stop_button_2 = tk.Button(controller, text="STOP CAM2", command=stop_recording2)
                            stop_button_2.place(x=160, y=300)
                            ####################    CAM2
                            Start_timing2 = tk.Label(controller, text="START TIME")
                            Start_timing2.place(x=60, y=330)
                            strt2 = tk.Label(controller, text="0:0")
                            strt2.place(x=210, y=330)
                            Duration_time2 = tk.Label(controller, text="DURATION")
                            Duration_time2.place(x=60, y=360)
                            drn2 = tk.Label(controller, text="0:0:0")
                            drn2.place(x=210, y=360)
                            NOD2 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD2.place(x=60, y=390)
                            num2 = tk.Label(controller, text="0")
                            num2.place(x=210, y=390)
                            ####################    CAM3
                            cam3 = tk.Label(controller, text="CAMERA 3", fg='violet')
                            cam3.place(x=20, y=420)
                            get_time3 = tk.Label(controller, text='Enter Time')
                            get_time3.place(x=60, y=450)
                            time3 = tk.Entry(controller)
                            time3.place(x=160, y=450)
                            start_button_3 = tk.Button(controller, text="START CAM3", command=start_recording3)
                            start_button_3.place(x=60, y=480)
                            stop_button_3 = tk.Button(controller, text="STOP CAM3", command=stop_recording3)
                            stop_button_3.place(x=160, y=480)
                            ####################    CAM3
                            Start_timing3 = tk.Label(controller, text="START TIME")
                            Start_timing3.place(x=60, y=510)
                            strt3 = tk.Label(controller, text="0:0")
                            strt3.place(x=210, y=510)
                            Duration_time3 = tk.Label(controller, text="DURATION")
                            Duration_time3.place(x=60, y=540)
                            drn3 = tk.Label(controller, text="0:0:0")
                            drn3.place(x=210, y=540)
                            NOD3 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD3.place(x=60, y=570)
                            num3 = tk.Label(controller, text="0")
                            num3.place(x=210, y=570)
                            ####################    CAM4
                            cam4 = tk.Label(controller, text="CAMERA 4", fg='skyblue')
                            cam4.place(x=320, y=60)
                            get_time4 = tk.Label(controller, text='Enter Time')
                            get_time4.place(x=360, y=90)
                            time4 = tk.Entry(controller)
                            time4.place(x=460, y=90)
                            start_button_4 = tk.Button(controller, text="START CAM4", command=start_recording4)
                            start_button_4.place(x=360, y=120)
                            stop_button_4 = tk.Button(controller, text="STOP CAM4", command=stop_recording4)
                            stop_button_4.place(x=460, y=120)
                            ####################    CAM4
                            Start_timing4 = tk.Label(controller, text="START TIME")
                            Start_timing4.place(x=360, y=150)
                            strt4 = tk.Label(controller, text="0:0")
                            strt4.place(x=510, y=150)
                            Duration_time4 = tk.Label(controller, text="DURATION")
                            Duration_time4.place(x=360, y=180)
                            drn4 = tk.Label(controller, text="0:0:0")
                            drn4.place(x=510, y=180)
                            NOD4 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD4.place(x=360, y=210)
                            num4 = tk.Label(controller, text="0")
                            num4.place(x=510, y=210)
                            ####################    CAM5
                            cam5 = tk.Label(controller, text="CAMERA 5", fg='black')
                            cam5.place(x=320, y=240)
                            get_time5 = tk.Label(controller, text='Enter Time')
                            get_time5.place(x=360, y=270)
                            time5 = tk.Entry(controller)
                            time5.place(x=460, y=270)
                            start_button_5 = tk.Button(controller, text="START CAM5", command=start_recording5)
                            start_button_5.place(x=360, y=300)
                            stop_button_5 = tk.Button(controller, text="STOP CAM5", command=stop_recording5)
                            stop_button_5.place(x=460, y=300)
                            ####################    CAM5
                            Start_timing5 = tk.Label(controller, text="START TIME")
                            Start_timing5.place(x=360, y=330)
                            strt5 = tk.Label(controller, text="0:0")
                            strt5.place(x=510, y=330)
                            Duration_time5 = tk.Label(controller, text="DURATION")
                            Duration_time5.place(x=360, y=360)
                            drn5 = tk.Label(controller, text="0:0:0")
                            drn5.place(x=510, y=360)
                            NOD5 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD5.place(x=360, y=390)
                            num5 = tk.Label(controller, text="0")
                            num5.place(x=510, y=390)
                            ####################    CAM6
                            cam6 = tk.Label(controller, text="CAMERA 6", fg='grey')
                            cam6.place(x=320, y=420)
                            get_time6 = tk.Label(controller, text='Enter Time')
                            get_time6.place(x=360, y=450)
                            time6 = tk.Entry(controller)
                            time6.place(x=460, y=450)
                            start_button_6 = tk.Button(controller, text="START CAM6", command=start_recording6)
                            start_button_6.place(x=360, y=480)
                            stop_button_6 = tk.Button(controller, text="STOP CAM6", command=stop_recording6)
                            stop_button_6.place(x=460, y=480)
                            ####################    CAM6
                            Start_timing6 = tk.Label(controller, text="START TIME")
                            Start_timing6.place(x=360, y=510)
                            strt6 = tk.Label(controller, text="0:0")
                            strt6.place(x=510, y=510)
                            Duration_time6 = tk.Label(controller, text="DURATION")
                            Duration_time6.place(x=360, y=540)
                            drn6 = tk.Label(controller, text="0:0:0")
                            drn6.place(x=510, y=540)
                            NOD6 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD6.place(x=360, y=570)
                            num6 = tk.Label(controller, text="0")
                            num6.place(x=510, y=570)
                            ######################  CLOSE
                            close_button = tk.Button(controller, text="CLOSE", command=close_window)
                            close_button.place(x=130, y=640)
                            process_frame()
                            controller.mainloop()
                            cap1.release()
                            cap2.release()
                            cap3.release()
                            cap4.release()
                            cap5.release()
                            cap6.release()
                            cv2.destroyAllWindows()

                    rec = tk.Button(main_frame, text="record", font=10, command=reco)
                    rec.place(x=400, y=250)

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

                        num = num + 1

                    output_frame.update_idletasks()
                    canvas.configure(scrollregion=canvas.bbox("all"))
                    canvas.bind_all("<MouseWheel>",
                                    lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

                def export_captured_data():
                    output = main_frame

                    def expo_date():
                        selected_date = calendar.get_date()
                        conn = sqlite3.connect('DATABASES/input.db')
                        query = "SELECT * FROM input_data WHERE UPLOADED_DATE = ?"
                        df = pd.read_sql_query(query, conn, params=(selected_date,))
                        df.to_excel(f"./CAPTURED DATA EXCEL/{selected_date}.xlsx", index=False)
                        messagebox.showinfo("Exported", "Overall data exported to Excel successfully.")

                    def expo_name():
                        video_name = v_name.get()
                        conv = sqlite3.connect('DATABASES/input.db')
                        queryv = "SELECT * FROM input_data WHERE VIDEO_NAME = ?"
                        df = pd.read_sql_query(queryv, conv, params=(video_name,))
                        df.to_excel(f"./CAPTURED DATA EXCEL/{video_name}.xlsx", index=False)
                        messagebox.showinfo("Exported", "Overall data exported to Excel successfully.")

                    select_date = Label(output, text="SELECT DATE:", font=10, fg='white', bg='#2c2f33')
                    select_date.place(x=300, y=200)

                    calendar = DateEntry(output, width=12, background='darkblue', foreground='white',
                                         font=('Arial', 14))
                    calendar.place(x=500, y=200)

                    exportd = Button(output, text="EXPORT", font=5, command=expo_date)
                    exportd.place(x=700, y=200)

                    type_name = Label(output, text="VIDEO NAME", font=10, fg='white', bg='#2c2f33')
                    type_name.place(x=300, y=300)
                    ext = Label(output, text="*with extension", fg='white', bg='#2c2f33')
                    ext.place(x=320, y=330)

                    v_name = Entry(output, font=10, width=14)
                    v_name.place(x=500, y=300)

                    exportv = Button(output, text="EXPORT", font=5, command=expo_name)
                    exportv.place(x=700, y=300)

                def export_summary():
                    conn = sqlite3.connect('DATABASES/recording.db')
                    df = pd.read_sql_query("SELECT * from recordsummary", conn)
                    df.to_excel(f"./SUMMARY DATA EXCEL/{current_date}-RECORDING SUMMARY.xlsx", index=False)
                    conn.close()
                    print("Data exported to Excel successfully.")
                    messagebox.showinfo("Exported", "Overall data exported to Excel successfully.")

                def export_input_summary():
                    conn = sqlite3.connect('DATABASES/input.db')
                    df = pd.read_sql_query("SELECT * from input_summary", conn)
                    df.to_excel(f"./SUMMARY DATA EXCEL/{current_date}-INPUT SUMMARY.xlsx", index=False)
                    conn.close()
                    print("Data exported to Excel successfully.")
                    messagebox.showinfo("Exported", "Overall data exported to Excel successfully.")

                def download_clip():
                    box = main_frame
                    try:
                        if not os.path.exists('DOWNLOADED CLIPS'):
                            os.makedirs('DOWNLOADED CLIPS')
                    except OSError:
                        print('Error: Creating directory of DOWNLOADED CLIPS')

                    result = Frame(box, bg='white', width=500, height=400, highlightbackground='black',
                                   highlightthickness=2)
                    result.pack(pady=100, padx=20)

                    def select_file():
                        file_path = filedialog.askopenfilename()
                        return file_path

                    def clip():

                        start_hour_str = start_hour.get()
                        start_minute_str = start_minute.get()
                        start_second_str = start_second.get()
                        end_hour_str = end_hour.get()
                        end_minute_str = end_minute.get()
                        end_second_str = end_second.get()
                        start_time_str = f"{start_hour_str}:{start_minute_str}:{start_second_str}"
                        end_time_str = f"{end_hour_str}:{end_minute_str}:{end_second_str}"
                        clip_name = name_ent.get()
                        file_path = select_file()
                        video = VideoFileClip(file_path)
                        location = 'DOWNLOADED CLIPS'
                        clip = video.subclip(start_time_str, end_time_str)
                        clip.write_videofile('./DOWNLOADED CLIPS/' + clip_name + '.mp4')
                        os.startfile(location)
                        clip.close()
                        video.close()

                    start_label = tk.Label(result, text="Start Time: ", font=3, bg='white')
                    start_label.place(x=80, y=100)
                    start_hour = tk.StringVar(value='0')
                    start_hour_spinbox = tk.Spinbox(result, from_=0, to=23, width=2, font=3, textvariable=start_hour)
                    start_hour_spinbox.place(x=260, y=100)
                    start_minute = tk.StringVar(value='0')
                    start_minute_spinbox = tk.Spinbox(result, from_=0, to=59, width=2, textvariable=start_minute,
                                                      font=3)
                    start_minute_spinbox.place(x=310, y=100)
                    start_second = tk.StringVar(value='0')
                    start_second_spinbox = tk.Spinbox(result, from_=0, to=59, width=2, textvariable=start_second,
                                                      font=3)
                    start_second_spinbox.place(x=360, y=100)
                    end_label = tk.Label(result, text="End Time: ", font=3, bg='white')
                    end_label.place(x=80, y=160)
                    end_hour = tk.StringVar(value='0')
                    end_hour_spinbox = tk.Spinbox(result, from_=0, to=23, width=2, font=3, textvariable=end_hour)
                    end_hour_spinbox.place(x=260, y=160)
                    end_minute = tk.StringVar(value='0')
                    end_minute_spinbox = tk.Spinbox(result, from_=0, to=59, width=2, font=3, textvariable=end_minute)
                    end_minute_spinbox.place(x=310, y=160)
                    end_second = tk.StringVar(value='0')
                    end_second_spinbox = tk.Spinbox(result, from_=0, to=59, width=2, font=3, textvariable=end_second)
                    end_second_spinbox.place(x=360, y=160)
                    name = Label(result, text="Enter Clip Name", font=3, bg='white')
                    name.place(x=80, y=230)
                    name_ent = Entry(result, width=12, font=3, highlightbackground='black', highlightthickness=2)
                    name_ent.place(x=260, y=230)
                    button = Button(result, text="CUT", command=clip, width=10, font=2, fg='white', height=1, bg='grey')
                    button.place(x=200, y=300)
                    box.mainloop()

                def delete_db():
                    conn = sqlite3.connect('cap_data.db')
                    c = conn.cursor()
                    c.execute('DELETE FROM data;')
                    print('We have deleted', c.rowcount, 'records from the table.')
                    conn.commit()
                    conn.close()
                    output = main_frame
                    out = Label(output, text="DATA CLEARED", font=4, fg='white', bg='#2c2f33')
                    out.place(x=400, y=300)

                def open_file_dialog():
                    file_path = filedialog.askopenfilename()
                    print("Selected file:", file_path)
                    return file_path

                def input_video():

                    instruction = Label(main_frame, text="Press 'q' to stop video", font=2, bg='#2c2f33', fg='white')
                    instruction.place(x=20, y=20)

                    file_path = open_file_dialog()
                    cap = cv2.VideoCapture(file_path)
                    video_name = os.path.basename(file_path)
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    playback_speed = 2
                    modified_fps = fps * playback_speed

                    first_detection_times = {}
                    qr_codes_array = []
                    cv2.namedWindow('searching', cv2.WINDOW_NORMAL)
                    cv2.resizeWindow('searching', 600, 400)

                    while cap.isOpened():
                        ret, frame = cap.read()
                        if not ret:
                            break
                        qr_codes = decode(frame)
                        for qr_code in qr_codes:
                            data = qr_code.data.decode('utf-8')

                            if data not in first_detection_times:
                                first_detection_times[data] = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                first_detection_times[data] = first_detection_times[data] % (24 * 3600)
                                qr_codes_array.append(data)

                                hour = first_detection_times[data] // 3600
                                first_detection_times[data] %= 3600
                                minutes = first_detection_times[data] // 60
                                first_detection_times[data] %= 60
                                video_time = "%d:%02d:%02d" % (hour, minutes, first_detection_times[data])

                                present_date = datetime.now().strftime('%Y-%m-%d')
                                present_time = datetime.now().strftime('%I-%M %p')
                                print(
                                    f"QR code [{data}] detected at D&T = ({present_date}//{present_time}), In video = ({video_time})in({video_name})")

                                frequency = 1000
                                duration = 500
                                winsound.Beep(frequency, duration)
                                scan(data, video_time, video_name, present_date, present_time)

                                captured_image = './CAPTURED DATA IMAGES/' + str(data) + str(
                                    first_detection_times[data]) + '.jpg'
                                delay = int(1000 / modified_fps)

                            for qr_code in qr_codes:
                                (x, y, w, h) = qr_code.rect
                                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                pts2 = qr_code.rect
                                cv2.putText(frame, data, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                                            (255, 0, 255), 1)

                            cv2.imwrite(captured_image, frame)
                            if cv2.waitKey(delay):
                                break

                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break

                        cv2.imshow('searching', frame)
                        cv2.waitKey(1)

                    code_array = len(qr_codes_array)
                    print("Number Of Detected QR codes:", len(qr_codes_array))
                    cap.release()
                    cv2.destroyAllWindows()

                    if len(qr_codes_array) == 0:
                        print("No QR codes detected in the video.")

                    output = main_frame

                    if len(qr_codes_array) == 0:
                        NODA = Label(output, text="NO DATA DETECTED", font=3, bg='#2c2f33', fg='white')
                        NODA.place(x=400, y=300)

                    elif code_array == len(qr_codes_array):

                        result = Frame(output, bg='white', width=500, height=450, highlightbackground='black',
                                       highlightthickness=2)
                        result.pack(pady=100, padx=20)

                        Video_name = Label(result, text="VIDEO NAME", font=3, bg='white')
                        Video_name.place(x=120, y=120)

                        Video = Label(result, text=video_name, font=3, bg='white')
                        Video.place(x=300, y=120)

                        Upload_date = Label(result, text="UPLOAD DATE", font=3, bg='white')
                        Upload_date.place(x=120, y=190)

                        pres_date = Label(result, text=present_date, font=3, bg='white')
                        pres_date.place(x=300, y=190)

                        Upload_time = Label(result, text="UPLOAD TIME", font=3, bg='white')
                        Upload_time.place(x=120, y=260)

                        pres_time = Label(result, text=present_time, font=3, bg='white')
                        pres_time.place(x=300, y=260)

                        No_of_data = Label(result, text="NO OF DATA", font=3, bg='white')
                        No_of_data.place(x=120, y=330)

                        NOD = Label(result, text=code_array, font=3, width=5, bg='white')
                        NOD.place(x=300, y=330)

                    overall(video_name, len(qr_codes_array), present_date, present_time)

                def overall(video_name, code_array, present_date, present_time):
                    cons = sqlite3.connect('DATABASES/input.db')
                    cons.execute(
                        "INSERT INTO input_summary (VIDEO_NAME, NO_OF_DATA, UPLOADED_DATE, UPLOADED_TIME) VALUES (?,?,?,?)",
                        (video_name, code_array, present_date, present_time))
                    cons.commit()
                    cons.close()

                def scan(data, video_time, video_name, present_date, present_time):
                    conn = sqlite3.connect('DATABASES/input.db')
                    conn.execute(
                        "INSERT INTO input_data (DETECTED_DATA, DETETCTED_TIME, VIDEO_NAME, UPLOADED_DATE, UPLOADED_TIME) VALUES (?,?,?,?,?)",
                        (data, video_time, video_name, present_date, present_time))
                    conn.commit()
                    conn.close()

                def hide_indicators():
                    rec_indicator.config(bg='#c3c3c3')
                    summary_indicator.config(bg='#c3c3c3')
                    data_indicator.config(bg='#c3c3c3')
                    exp_rec_indicator.config(bg='#c3c3c3')
                    exp_sum_indicator.config(bg='#c3c3c3')
                    input_indicator.config(bg='#c3c3c3')
                    download_indicator.config(bg='#c3c3c3')

                def indicate(lb, page):
                    hide_indicators()
                    lb.config(bg='#158aff')
                    delete_pages()
                    page()

                def delete_pages():
                    for frame in main_frame.winfo_children():
                        frame.destroy()

                # OPTION FRAME

                options_frame = tk.Frame(w, bg="#c3c3c3", highlightbackground='black', highlightthickness=2)
                options_frame.pack(side=tk.LEFT)
                options_frame.pack_propagate(False)
                options_frame.configure(width=210, height=1500)

                # BUTTONS
                general = tk.Label(options_frame, text="GENERAL", font=10, bg="#c3c3c3")
                general.place(x=50, y=20)

                rec_btn = tk.Button(options_frame, text="RECORD", font=('Bold', 15), fg='white', bd=0, bg='#4392fa',
                                    width=15,
                                    borderwidth=5, command=lambda: indicate(rec_indicator, record))
                rec_btn.place(x=10, y=50)

                summary_btn = tk.Button(options_frame, text="DISPLAY \n SUMMARY", font=('Bold', 15), fg='white', bd=0,
                                        bg='#4392fa',
                                        width=15, borderwidth=5,
                                        command=lambda: indicate(summary_indicator, display_summary))
                summary_btn.place(x=10, y=110)

                exp_rec_summary_bt = tk.Button(options_frame, text="EXPORT REC\n SUMMARY", font=('Bold', 15),
                                               fg='white', bd=0,
                                               bg='#4392fa',
                                               width=15, borderwidth=5,
                                               command=lambda: indicate(exp_rec_indicator, export_summary))
                exp_rec_summary_bt.place(x=10, y=195)

                options = tk.Label(options_frame, text="OPTIONS", font=15, bg="#c3c3c3")
                options.place(x=50, y=280)

                input_btn = tk.Button(options_frame, text="INPUT \n VIDEO", font=('Bold', 15), fg='white', bd=0,
                                      bg='#4392fa', width=15,
                                      borderwidth=5, command=lambda: indicate(input_indicator, input_video))
                input_btn.place(x=10, y=320)

                data_btn = tk.Button(options_frame, text="EXPORT\nCAPTURED\nDATA", font=('Bold', 15), fg='white', bd=0,
                                     bg='#4392fa',
                                     width=15, borderwidth=5,
                                     command=lambda: indicate(data_indicator, export_captured_data))
                data_btn.place(x=10, y=400)

                exp_input_summary_bt = tk.Button(options_frame, text="EXPORT INPUT\n SUMMARY", font=('Bold', 15),
                                                 fg='white', bd=0,
                                                 bg='#4392fa',
                                                 width=15, borderwidth=5,
                                                 command=lambda: indicate(exp_sum_indicator, export_input_summary))
                exp_input_summary_bt.place(x=10, y=505)

                download_btn = tk.Button(options_frame, text="DOWNLOAD \n CLIP", font=('Bold', 15), fg='white', bd=0,
                                         bg='#4392fa',
                                         width=15, borderwidth=5,
                                         command=lambda: indicate(download_indicator, download_clip))
                download_btn.place(x=10, y=590)

                delete_db = tk.Button(options_frame, text="Delete DB", command=delete_db, bg='red', fg='white')
                delete_db.place(x=60, y=680)

                # INDICATORS

                rec_indicator = tk.Label(options_frame, text='', bg='#c3c3c3')
                rec_indicator.place(x=3, y=50, width=5, height=40)

                summary_indicator = tk.Label(options_frame, text='', bg='#c3c3c3')
                summary_indicator.place(x=3, y=110, width=5, height=60)

                exp_rec_indicator = tk.Label(options_frame, text='', bg='#c3c3c3')
                exp_rec_indicator.place(x=3, y=195, width=5, height=60)

                input_indicator = tk.Label(options_frame, text='', bg='#c3c3c3')
                input_indicator.place(x=3, y=320, width=5, height=60)

                data_indicator = tk.Label(options_frame, text='', bg='#c3c3c3')
                data_indicator.place(x=3, y=400, width=5, height=90)

                exp_sum_indicator = tk.Label(options_frame, text='', bg='#c3c3c3')
                exp_sum_indicator.place(x=3, y=505, width=5, height=60)

                download_indicator = tk.Label(options_frame, text='', bg='#c3c3c3')
                download_indicator.place(x=3, y=590, width=5, height=60)

                # MAIN FRAME

                main_frame = tk.Frame(w, highlightbackground='black', highlightthickness=2)
                main_frame.pack(side=tk.LEFT)
                main_frame.pack_propagate(False)
                main_frame.configure(height=1500, width=7100, bg='#2c2f33')

                w.mainloop()

            else:
                messagebox.showerror('Error', 'Invalid password')

        else:
            messagebox.showerror('Error', 'Invalid username')

    elif username != '' and password != '':
        cursor.execute('SELECT password FROM users WHERE username=?', [username])
        result = cursor.fetchone()
        if result:
            if bcrypt.checkpw(password.encode('utf-8'), result[0]):
                messagebox.showinfo('Success', f'{username} Logged in successfully')

                app.destroy()

                w = Tk()
                w.geometry('1366x768')
                w.configure(bg='#262626')
                w.title('EAN DETECTOR')

                current_time = datetime.now().time()
                present_date = datetime.now().strftime("%d-%m-%Y")

                def record():
                    options = ["6", "5", "4", "3", "2", "1"]
                    selected_option = tk.StringVar()

                    select = ttk.Label(main_frame, text="Select Cameras:-", font=10)
                    select.place(x=250, y=200)

                    combo_box = ttk.Combobox(main_frame, textvariable=selected_option, values=options, font=10, width=4)
                    combo_box.place(x=450, y=200)
                    combo_box.current(0)

                    def scan1(data1, elapsed_time_str1, present_date, present_time, video_name1, username):
                        rec_d1 = sqlite3.connect('./DATABASES/recording.db')
                        rec_d1.execute(
                            "INSERT INTO record1data (DETETCTED_DATA, DETECTED_TIME, DATE ,TIME , VIDEO_NAME, USER_NAME) VALUES (?,?,?,?,?,?)",
                            (data1, elapsed_time_str1, present_date, present_time, video_name1, username))
                        rec_d1.commit()
                        rec_d1.close()

                    def scan2(data2, elapsed_time_str2, present_date, present_time, video_name2, username):
                        rec_d2 = sqlite3.connect('./DATABASES/recording.db')
                        rec_d2.execute(
                            "INSERT INTO record2data (DETETCTED_DATA, DETECTED_TIME, DATE ,TIME , VIDEO_NAME, USER_NAME) VALUES (?,?,?,?,?,?)",
                            (data2, elapsed_time_str2, present_date, present_time, video_name2, username))
                        rec_d2.commit()
                        rec_d2.close()

                    def scan3(data3, elapsed_time_str3, present_date, present_time, video_name3, username):
                        rec_d3 = sqlite3.connect('./DATABASES/recording.db')
                        rec_d3.execute(
                            "INSERT INTO record3data (DETETCTED_DATA, DETECTED_TIME, DATE ,TIME , VIDEO_NAME, USER_NAME) VALUES (?,?,?,?,?,?)",
                            (data3, elapsed_time_str3, present_date, present_time, video_name3, username))
                        rec_d3.commit()
                        rec_d3.close()

                    def scan4(data4, elapsed_time_str4, present_date, present_time, video_name4, username):
                        rec_d4 = sqlite3.connect('./DATABASES/recording.db')
                        rec_d4.execute(
                            "INSERT INTO record4data (DETETCTED_DATA, DETECTED_TIME, DATE ,TIME , VIDEO_NAME, USER_NAME) VALUES (?,?,?,?,?,?)",
                            (data4, elapsed_time_str4, present_date, present_time, video_name4, username))
                        rec_d4.commit()
                        rec_d4.close()

                    def scan5(data5, elapsed_time_str5, present_date, present_time, video_name5, username):
                        rec_d5 = sqlite3.connect('./DATABASES/recording.db')
                        rec_d5.execute(
                            "INSERT INTO record5data (DETETCTED_DATA, DETECTED_TIME, DATE ,TIME , VIDEO_NAME, USER_NAME) VALUES (?,?,?,?,?,?)",
                            (data5, elapsed_time_str5, present_date, present_time, video_name5, username))
                        rec_d5.commit()
                        rec_d5.close()

                    def scan6(data6, elapsed_time_str6, present_date, present_time, video_name6, username):
                        rec_d6 = sqlite3.connect('./DATABASES/recording.db')
                        rec_d6.execute(
                            "INSERT INTO record6data (DETETCTED_DATA, DETECTED_TIME, DATE ,TIME , VIDEO_NAME, USER_NAME) VALUES (?,?,?,?,?,?)",
                            (data6, elapsed_time_str6, present_date, present_time, video_name6, username))
                        rec_d6.commit()
                        rec_d6.close()

                    def dispatch1(camera1, elapsed_time_str1, code_array1, present_date, present_time, username):
                        sum1 = sqlite3.connect('./DATABASES/recording.db')
                        sum1.execute(
                            "INSERT INTO recordsummary (VIDEO_NAME, DURATION, NO_OF_DATA, DATE, TIME, USER_NAME) VALUES (?,?,?,?,?,?)",
                            (camera1, elapsed_time_str1, code_array1, present_date, present_time, username))
                        sum1.commit()
                        sum1.close()

                    def dispatch2(camera2, elapsed_time_str2, code_array2, present_date, present_time, username):
                        sum2 = sqlite3.connect('./DATABASES/recording.db')
                        sum2.execute(
                            "INSERT INTO recordsummary (VIDEO_NAME, DURATION, NO_OF_DATA, DATE, TIME, USER_NAME) VALUES (?,?,?,?,?,?)",
                            (camera2, elapsed_time_str2, code_array2, present_date, present_time, username))
                        sum2.commit()
                        sum2.close()

                    def dispatch3(camera3, elapsed_time_str3, code_array2, present_date, present_time, username):
                        sum3 = sqlite3.connect('./DATABASES/recording.db')
                        sum3.execute(
                            "INSERT INTO recordsummary (VIDEO_NAME, DURATION, NO_OF_DATA, DATE, TIME, USER_NAME) VALUES (?,?,?,?,?,?)",
                            (camera3, elapsed_time_str3, code_array2, present_date, present_time, username))
                        sum3.commit()
                        sum3.close()

                    def dispatch4(camera4, elapsed_time_str4, code_array4, present_date, present_time, username):
                        sum4 = sqlite3.connect('./DATABASES/recording.db')
                        sum4.execute(
                            "INSERT INTO recordsummary (VIDEO_NAME, DURATION, NO_OF_DATA, DATE, TIME, USER_NAME) VALUES (?,?,?,?,?,?)",
                            (camera4, elapsed_time_str4, code_array4, present_date, present_time, username))
                        sum4.commit()
                        sum4.close()

                    def dispatch5(camera5, elapsed_time_str5, code_array5, present_date, present_time, username):
                        sum5 = sqlite3.connect('./DATABASES/recording.db')
                        sum5.execute(
                            "INSERT INTO recordsummary (VIDEO_NAME, DURATION, NO_OF_DATA, DATE, TIME, USER_NAME) VALUES (?,?,?,?,?,?)",
                            (camera5, elapsed_time_str5, code_array5, present_date, present_time, username))
                        sum5.commit()
                        sum5.close()

                    def dispatch6(camera6, elapsed_time_str6, code_array6, present_date, present_time, username):
                        sum6 = sqlite3.connect('./DATABASES/recording.db')
                        sum6.execute(
                            "INSERT INTO recordsummary (VIDEO_NAME, DURATION, NO_OF_DATA, DATE, TIME, USER_NAME) VALUES (?,?,?,?,?,?)",
                            (camera6, elapsed_time_str6, code_array6, present_date, present_time, username))
                        sum6.commit()
                        sum6.close()

                    def reco():
                        selected_value = selected_option.get()

                        if selected_value == "1":
                            def start_recording1():
                                global recording1, start_time1, writer1, current_date, starting_time1, started_time1, elapsed_time_str1, first_detection_times1, camera1, data1, qr_codes_array1, video_name1
                                recording1 = True
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
                                global recording1, writer1, start_time1, elapsed_time_str1, code_array1
                                recording1 = False
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
                                    dispatch1(video_name1, elapsed_time_str1, len(qr_codes_array1), present_date,
                                              present_time, username)
                                    rec1_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record1data WHERE VIDEO_NAME = '{video_name1}'", rec1_data)
                                    df.to_excel(f"./{current_date}/{video_name1}.xlsx", index=False)
                                    rec1_data.close()

                            cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)

                            cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            fourcc1 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

                            def process_frame():
                                global recording1, start_time1, writer1, end_time1, present_date, present_time, elapsed_time_str1, data1
                                # CAM CCTV
                                ret1, frame1 = cap1.read()
                                cv2.putText(frame1, "CAM1", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret1:
                                    if recording1:
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
                                                scan1(data1, elapsed_time_str1, present_date, present_time, video_name1, username)

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

                            def disable_event():
                                pass

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

                        elif selected_value == "2":
                            ################################    CAM1    RECORDING    ##################################
                            def start_recording1():
                                global recording1, start_time1, writer1, current_date, starting_time1, started_time1, elapsed_time_str1, first_detection_times1, qr_codes_array1, data1, camera1, video_name1
                                recording1 = True
                                data1 = ' '
                                start_time1 = None
                                qr_codes_array1 = []
                                live_time1 = datetime.now()
                                first_detection_times1 = {}
                                starting_time1 = current_time.strftime("%I-%M %p")
                                started_time1 = live_time1.strftime("%I:%M %p")
                                start_time1 = None
                                num1.config(text=0)
                                strt1.config(text=0)
                                drn1.config(text=0)
                                camera1 = "CAM1"
                                time_1 = time1.get()
                                video_name1 = f'{camera1}-{time_1}'
                                print("Camera1 Recording")
                                writer1 = cv2.VideoWriter(f"./{current_date}/{video_name1}.mp4", fourcc1, 23.0,
                                                          (640, 480))

                            def stop_recording1():
                                global recording1, writer1, start_time1, elapsed_time_str1, code_array1
                                recording1 = False

                                print("Camera1 Stopped")
                                if writer1 is not None:
                                    writer1.release()

                                elapsed_time1 = datetime.now() - start_time1
                                elapsed_time_str1 = str(elapsed_time1).split(".")[0]
                                dur1 = elapsed_time_str1
                                print("Camera1 stopped")
                                code_array1 = len(qr_codes_array1)
                                print("No Of detected QR codes in camera1:", code_array1)
                                if len(first_detection_times1) == 0:
                                    print("No data in camera1")
                                else:
                                    strt1.config(text=started_time1)
                                    drn1.config(text=dur1)
                                    num1.config(text=code_array1)
                                    dispatch1(video_name1, elapsed_time_str1, len(qr_codes_array1), present_date,
                                              present_time, username)
                                    rec1_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record1data WHERE VIDEO_NAME = '{video_name1}'", rec1_data)
                                    df.to_excel(f"./{current_date}/{video_name1}.xlsx", index=False)
                                    rec1_data.close()

                                    ################################    CAM2    RECORDING    ##################################

                            def start_recording2():
                                global recording2, start_time2, writer2, current_date, starting_time2, qr_codes_array2, data2, started_time2, camera2, first_detection_times2, elapsed_time_str2, video_name2
                                recording2 = True
                                start_time2 = None
                                data2 = ' '
                                qr_codes_array2 = []
                                first_detection_times2 = {}
                                live_time = datetime.now()
                                starting_time2 = current_time.strftime("%I-%M %p")
                                started_time2 = live_time.strftime("%I:%M %p")
                                num2.config(text=0)
                                strt2.config(text=0)
                                drn2.config(text=0)
                                camera2 = "CAM2"
                                time_2 = time2.get()
                                video_name2 = f'{camera2}-{time_2}'

                                print("Camera2 Recording")
                                writer2 = cv2.VideoWriter(f"./{current_date}/{video_name2}.mp4", fourcc1, 23.0,
                                                          (640, 480))

                            def stop_recording2():
                                global recording2, writer2, start_time2, code_array2, elapsed_time_str2
                                recording2 = False

                                if writer2 is not None:
                                    writer2.release()

                                elapsed_time2 = datetime.now() - start_time2
                                elapsed_time_str2 = str(elapsed_time2).split(".")[0]
                                dur2 = elapsed_time_str2
                                print("Camera2 stopped")
                                code_array2 = len(qr_codes_array2)
                                print("No Of detected QR codes in camera2:", code_array2)

                                if len(first_detection_times2) == 0:
                                    print("No data in camera2")

                                else:
                                    strt2.config(text=started_time2)
                                    drn2.config(text=dur2)
                                    num2.config(text=code_array2)

                                    dispatch2(video_name2, elapsed_time_str2, len(qr_codes_array2), present_date,
                                              present_time, username)

                                    rec2_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record2data WHERE VIDEO_NAME = '{video_name2}'", rec2_data)
                                    df.to_excel(f"./{current_date}/{video_name2}.xlsx", index=False)
                                    rec2_data.close()

                            cap1 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
                            cap2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)

                            cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            fourcc1 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time1 = datetime.now().strftime("%H-%M")

                            fourcc2 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time2 = datetime.now().strftime("%H-%M")

                            def process_frame():
                                global recording1, recording2, recording3, start_time1, start_time2, start_time3, writer1, writer2, writer3, end_time1, end_time2, end_time3, data1, data2, code_array1, code_array2, present_date, present_time, elapsed_time_str1, elapsed_time_str2
                                # CAM1
                                ret1, frame1 = cap1.read()
                                cv2.putText(frame1, "CAM1", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret1:
                                    if recording1:
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
                                                    f"QR code {data1} detected for the first time at{elapsed_time_str1} on {present_date}-{present_time} ")
                                                scan1(data1, elapsed_time_str1, present_date, present_time, video_name1, username)

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
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame1, f"NO OF DATA:  {len(qr_codes_array1)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame1, f"LAST DATA:   {data1}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        writer1.write(frame1)
                                    cv2.imshow("Recording Camera cctv", frame1)
                                if not ret1:
                                    blank_frame1 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame1, "CAM1 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera cctv", blank_frame1)

                                # CAM2
                                ret2, frame2 = cap2.read()
                                cv2.putText(frame2, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret2:
                                    if recording2:
                                        qr_codes2 = decode(frame2)
                                        for qr_code2 in qr_codes2:
                                            data2 = qr_code2.data.decode('utf-8')
                                            if data2 not in first_detection_times2:
                                                first_detection_times2[data2] = cap2.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array2.append(data2)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data2} detected for the first time at{elapsed_time_str2} on {present_date}-{present_time} ")
                                                scan2(data2, elapsed_time_str2, present_date, present_time, video_name2, username)

                                            for qr_code2 in qr_codes2:
                                                (x, y, w, h) = qr_code2.rect
                                                cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code2.rect
                                                cv2.putText(frame2, data2, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array2) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time2 is None:
                                            start_time2 = datetime.now()

                                        elapsed_time2 = datetime.now() - start_time2
                                        elapsed_time_str2 = str(elapsed_time2).split(".")[0]
                                        cv2.putText(frame2, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame2, f"START TIME:  {started_time2}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame2, f"DURATION:    {elapsed_time_str2}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame2, f"NO OF DATA:  {len(qr_codes_array2)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame2, f"LAST DATA:   {data2}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        writer2.write(frame2)
                                    cv2.imshow("Recording Camera 2", frame2)

                                if not ret2:
                                    blank_frame2 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame2, "CAM2 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 2", blank_frame2)

                                cv2.waitKey(1)
                                controller.after(1, process_frame)

                            def start():
                                start_recording1()
                                start_recording2()

                            def stop():
                                stop_recording1()
                                stop_recording2()

                            def close_window():
                                cap1.release()
                                cap2.release()
                                cv2.destroyAllWindows()
                                controller.destroy()

                            controller = tk.Tk()
                            controller.geometry("300x500")
                            controller.title("VIDEO CONTROLLER")
                            controller.resizable(0, 0)
                            start = tk.Button(controller, text="START", command=start)
                            start.place(x=80, y=20)
                            stop = tk.Button(controller, text="STOP", command=stop)
                            stop.place(x=180, y=20)
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
                            ####################    CAM2
                            cam2 = tk.Label(controller, text="CAMERA 2", fg='red')
                            cam2.place(x=20, y=240)
                            get_time2 = tk.Label(controller, text='Enter Time')
                            get_time2.place(x=60, y=270)
                            time2 = tk.Entry(controller)
                            time2.place(x=160, y=270)
                            start_button_2 = tk.Button(controller, text="START CAM2", command=start_recording2)
                            start_button_2.place(x=60, y=300)
                            stop_button_2 = tk.Button(controller, text="STOP CAM2", command=stop_recording2)
                            stop_button_2.place(x=160, y=300)
                            ####################    CAM2
                            Start_timing2 = tk.Label(controller, text="START TIME")
                            Start_timing2.place(x=60, y=330)
                            strt2 = tk.Label(controller, text="0:0")
                            strt2.place(x=210, y=330)
                            Duration_time2 = tk.Label(controller, text="DURATION")
                            Duration_time2.place(x=60, y=360)
                            drn2 = tk.Label(controller, text="0:0:0")
                            drn2.place(x=210, y=360)
                            NOD2 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD2.place(x=60, y=390)
                            num2 = tk.Label(controller, text="0")
                            num2.place(x=210, y=390)
                            ######################  CLOSE

                            close_button = tk.Button(controller, text="CLOSE", command=close_window)
                            close_button.place(x=130, y=430)

                            process_frame()
                            controller.mainloop()
                            cap1.release()
                            cap2.release()
                            cv2.destroyAllWindows()

                        elif selected_value == "3":
                            ################################    CAM1    RECORDING    ##################################
                            def start_recording1():
                                global recording1, start_time1, writer1, current_date, starting_time1, started_time1, elapsed_time_str1, first_detection_times1, camera1, data1, qr_codes_array1, video_name2
                                recording1 = True
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
                                global recording1, writer1, start_time1, elapsed_time_str1, code_array1
                                recording1 = False
                                print("Camera1 Stopped")
                                if writer1 is not None:
                                    writer1.release()

                                elapsed_time1 = datetime.now() - start_time1
                                elapsed_time_str1 = str(elapsed_time1).split(".")[0]
                                dur1 = elapsed_time_str1
                                code_array1 = len(qr_codes_array1)
                                print("no in 1 camera", code_array1)

                                if len(first_detection_times1) == 0:
                                    print("no")

                                else:
                                    strt1.config(text=started_time1)
                                    drn1.config(text=dur1)
                                    num1.config(text=code_array1)
                                    dispatch1(video_name1, elapsed_time_str1, len(qr_codes_array1), present_date,
                                              present_time, username)
                                    rec1_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record1data WHERE VIDEO_NAME = '{video_name1}'", rec1_data)
                                    df.to_excel(f"./{current_date}/{video_name1}.xlsx", index=False)
                                    rec1_data.close()

                                    ################################    CAM2    RECORDING    ##################################

                            def start_recording2():
                                global recording2, start_time2, writer2, current_date, starting_time2, qr_codes_array2, data2, started_time2, camera2, first_detection_times2, elapsed_time_str2, video_name2
                                recording2 = True
                                start_time2 = None
                                data2 = ' '
                                qr_codes_array2 = []
                                first_detection_times2 = {}
                                live_time = datetime.now()
                                starting_time2 = current_time.strftime("%I-%M %p")
                                started_time2 = live_time.strftime("%I:%M %p")
                                num2.config(text=0)
                                strt2.config(text=0)
                                drn2.config(text=0)
                                camera2 = "CAM2"
                                time_2 = time2.get()
                                video_name2 = f'{camera2}-{time_2}'

                                print("Camera2 Recording")
                                writer2 = cv2.VideoWriter(f"./{current_date}/{video_name2}.mp4", fourcc1, 23.0,
                                                          (640, 480))

                            def stop_recording2():
                                global recording2, writer2, start_time2, code_array2, elapsed_time_str2
                                recording2 = False

                                if writer2 is not None:
                                    writer2.release()

                                elapsed_time2 = datetime.now() - start_time2
                                elapsed_time_str2 = str(elapsed_time2).split(".")[0]
                                dur2 = elapsed_time_str2
                                print("Camera2 stopped")
                                code_array2 = len(qr_codes_array2)
                                print("No Of detected QR codes in camera2:", code_array2)

                                if len(first_detection_times2) == 0:
                                    print("No data in camera2")

                                else:
                                    strt2.config(text=started_time2)
                                    drn2.config(text=dur2)
                                    num2.config(text=code_array2)

                                    dispatch2(video_name2, elapsed_time_str2, len(qr_codes_array2), present_date,
                                              present_time, username)

                                    rec2_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record2data WHERE VIDEO_NAME = '{video_name2}'", rec2_data)
                                    df.to_excel(f"./{current_date}/{video_name2}.xlsx", index=False)
                                    rec2_data.close()

                            def start_recording3():
                                global recording3, start_time3, writer3, current_date, starting_time3, qr_codes_array3, data3, started_time3, camera3, elapsed_time_str3, first_detection_times3, video_name3
                                recording3 = True
                                start_time3 = None
                                data3 = ' '
                                qr_codes_array3 = []
                                camera3 = "CAM3"
                                time_3 = time3.get()
                                video_name3 = f'{camera3}-{time_3}'
                                live_time = datetime.now()
                                first_detection_times3 = {}
                                starting_time3 = current_time.strftime("%I-%M %p")
                                started_time3 = live_time.strftime("%I:%M %p")
                                start_time3 = None
                                print("Camera3 Recording")
                                writer3 = cv2.VideoWriter(f"./{current_date}/{video_name3}.mp4", fourcc3, 23.0,
                                                          (640, 480))

                            def stop_recording3():
                                global recording3, writer3, start_time3, clip_name3, code_array3, elapsed_time_str3
                                recording3 = False
                                if writer3 is not None:
                                    writer3.release()
                                elapsed_time3 = datetime.now() - start_time3
                                elapsed_time_str3 = str(elapsed_time3).split(".")[0]
                                dur3 = elapsed_time_str3
                                print("Camera3 stopped")
                                code_array3 = len(qr_codes_array3)
                                print("No Of detected QR codes in camera3:", code_array3)

                                if len(first_detection_times3) == 0:
                                    print("No data")
                                else:
                                    strt3.config(text=started_time3)
                                    drn3.config(text=dur3)
                                    num3.config(text=code_array3)
                                    dispatch3(video_name3, elapsed_time_str3, len(qr_codes_array3), present_date,
                                              present_time, username)
                                    rec3_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record3data WHERE VIDEO_NAME = '{video_name3}'", rec3_data)
                                    df.to_excel(f"./{current_date}/{video_name3}.xlsx", index=False)
                                    rec3_data.close()

                            cap1 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
                            cap2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)
                            cap3 = cv2.VideoCapture(3, cv2.CAP_DSHOW)

                            cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap3.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap3.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            fourcc1 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time1 = datetime.now().strftime("%H-%M")

                            fourcc2 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time2 = datetime.now().strftime("%H-%M")

                            fourcc3 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time3 = datetime.now().strftime("%H-%M")

                            def process_frame():
                                global recording1, recording2, recording3, start_time1, start_time2, start_time3, writer1, writer2, writer3, end_time1, end_time2, end_time3, data1, data2, code_array1, code_array2, present_date, present_time, elapsed_time_str1, elapsed_time_str2, elapsed_time_str3, recording1, start_time1, writer1, end_time1, present_date, present_time, elapsed_time_str1, data1
                                # CAM CCTV
                                ret1, frame1 = cap1.read()
                                cv2.putText(frame1, "CAM1", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret1:
                                    if recording1:
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
                                                    f"QR code {data1} detected for the first time at{elapsed_time_str1} on {present_date}-{present_time} ")
                                                scan1(data1, elapsed_time_str1, present_date, present_time, video_name1, username)

                                            for qr_code1 in qr_codes1:
                                                (x, y, w, h) = qr_code1.rect
                                                cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code1.rect
                                                cv2.putText(frame1, data1, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

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
                                    cv2.imshow("Recording Camera cctv", blank_frame1)

                                # CAM2
                                ret2, frame2 = cap2.read()
                                cv2.putText(frame2, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret2:
                                    if recording2:
                                        qr_codes2 = decode(frame2)
                                        for qr_code2 in qr_codes2:
                                            data2 = qr_code2.data.decode('utf-8')
                                            if data2 not in first_detection_times2:
                                                first_detection_times2[data2] = cap2.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array2.append(data2)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data2} detected for the first time at{elapsed_time_str2} on {present_date}-{present_time} ")
                                                scan2(data2, elapsed_time_str2, present_date, present_time, video_name2, username)

                                            for qr_code2 in qr_codes2:
                                                (x, y, w, h) = qr_code2.rect
                                                cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code2.rect
                                                cv2.putText(frame2, data2, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array2) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time2 is None:
                                            start_time2 = datetime.now()

                                        elapsed_time2 = datetime.now() - start_time2
                                        elapsed_time_str2 = str(elapsed_time2).split(".")[0]
                                        cv2.putText(frame2, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame2, f"START TIME:  {started_time2}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame2, f"DURATION:    {elapsed_time_str2}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame2, f"NO OF DATA:  {len(qr_codes_array2)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame2, f"LAST DATA:   {data2}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        writer2.write(frame2)
                                    cv2.imshow("Recording Camera 2", frame2)

                                if not ret2:
                                    blank_frame2 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame2, "CAM2 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 2", blank_frame2)

                                # CAM3
                                ret3, frame3 = cap3.read()
                                cv2.putText(frame3, "CAM3", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret3:
                                    if recording3:
                                        qr_codes3 = decode(frame3)
                                        for qr_code3 in qr_codes3:
                                            data3 = qr_code3.data.decode('utf-8')
                                            if data3 not in first_detection_times3:
                                                first_detection_times3[data3] = cap2.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array3.append(data3)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data3} detected for the first time at{elapsed_time_str3} on {present_date}-{present_time} ")
                                                scan3(data3, elapsed_time_str3, present_date, present_time, video_name3, username)

                                            for qr_code3 in qr_codes3:
                                                (x, y, w, h) = qr_code3.rect
                                                cv2.rectangle(frame3, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code3.rect
                                                cv2.putText(frame3, data3, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array3) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time3 is None:
                                            start_time3 = datetime.now()

                                        elapsed_time3 = datetime.now() - start_time3
                                        elapsed_time_str3 = str(elapsed_time3).split(".")[0]
                                        cv2.putText(frame3, "CAM3", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame3, f"START TIME:  {started_time3}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame3, f"DURATION:    {elapsed_time_str3}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame3, f"NO OF DATA:  {len(qr_codes_array3)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame3, f"LAST DATA:   {data2}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        writer3.write(frame3)
                                    cv2.imshow("Recording Camera 3", frame3)

                                if not ret3:
                                    blank_frame3 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame3, "CAM3 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 3", blank_frame3)

                                cv2.waitKey(1)
                                controller.after(1, process_frame)

                            def start():
                                start_recording1()
                                start_recording2()
                                start_recording3()

                            def stop():
                                stop_recording1()
                                stop_recording2()
                                stop_recording3()

                            def close_window():
                                cap1.release()
                                cap2.release()
                                cap3.release()
                                cv2.destroyAllWindows()
                                controller.destroy()

                            controller = tk.Tk()
                            controller.geometry("300x650")
                            controller.title("VIDEO CONTROLLER")
                            controller.resizable(0, 0)
                            start = tk.Button(controller, text="START", command=start)
                            start.place(x=80, y=20)
                            stop = tk.Button(controller, text="STOP", command=stop)
                            stop.place(x=180, y=20)
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
                            ####################    CAM2
                            cam2 = tk.Label(controller, text="CAMERA 2", fg='red')
                            cam2.place(x=20, y=240)
                            get_time2 = tk.Label(controller, text='Enter Time')
                            get_time2.place(x=60, y=270)
                            time2 = tk.Entry(controller)
                            time2.place(x=160, y=270)
                            start_button_2 = tk.Button(controller, text="START CAM2", command=start_recording2)
                            start_button_2.place(x=60, y=300)
                            stop_button_2 = tk.Button(controller, text="STOP CAM2", command=stop_recording2)
                            stop_button_2.place(x=160, y=300)
                            ####################    CAM2
                            Start_timing2 = tk.Label(controller, text="START TIME")
                            Start_timing2.place(x=60, y=330)
                            strt2 = tk.Label(controller, text="0:0")
                            strt2.place(x=210, y=330)
                            Duration_time2 = tk.Label(controller, text="DURATION")
                            Duration_time2.place(x=60, y=360)
                            drn2 = tk.Label(controller, text="0:0:0")
                            drn2.place(x=210, y=360)
                            NOD2 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD2.place(x=60, y=390)
                            num2 = tk.Label(controller, text="0")
                            num2.place(x=210, y=390)
                            ####################    CAM3
                            cam3 = tk.Label(controller, text="CAMERA 3", fg='violet')
                            cam3.place(x=20, y=420)
                            get_time3 = tk.Label(controller, text='Enter Time')
                            get_time3.place(x=60, y=450)
                            time3 = tk.Entry(controller)
                            time3.place(x=160, y=450)
                            start_button_3 = tk.Button(controller, text="START CAM3", command=start_recording3)
                            start_button_3.place(x=60, y=480)
                            stop_button_3 = tk.Button(controller, text="STOP CAM3", command=stop_recording3)
                            stop_button_3.place(x=160, y=480)
                            ####################    CAM3
                            Start_timing3 = tk.Label(controller, text="START TIME")
                            Start_timing3.place(x=60, y=510)
                            strt3 = tk.Label(controller, text="0:0")
                            strt3.place(x=210, y=510)
                            Duration_time3 = tk.Label(controller, text="DURATION")
                            Duration_time3.place(x=60, y=540)
                            drn3 = tk.Label(controller, text="0:0:0")
                            drn3.place(x=210, y=540)
                            NOD3 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD3.place(x=60, y=570)
                            num3 = tk.Label(controller, text="0")
                            num3.place(x=210, y=570)
                            ######################  CLOSE

                            close_button = tk.Button(controller, text="CLOSE", command=close_window)
                            close_button.place(x=130, y=600)

                            process_frame()
                            controller.mainloop()
                            cap1.release()
                            cap2.release()
                            cap3.release()
                            cv2.destroyAllWindows()

                        elif selected_value == "4":

                            ################################    CAM1    RECORDING    ##################################
                            def start_recording1():
                                global recording1, start_time1, writer1, current_date, starting_time1, started_time1, elapsed_time_str1, first_detection_times1, camera1, data1, qr_codes_array1, video_name1
                                recording1 = True
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
                                global recording1, writer1, start_time1, elapsed_time_str1, code_array1
                                recording1 = False
                                print("Camera1 Stopped")
                                if writer1 is not None:
                                    writer1.release()

                                elapsed_time1 = datetime.now() - start_time1
                                elapsed_time_str1 = str(elapsed_time1).split(".")[0]
                                dur1 = elapsed_time_str1
                                code_array1 = len(qr_codes_array1)
                                print("no in 1 camera", code_array1)

                                if len(first_detection_times1) == 0:
                                    print("no")

                                else:
                                    strt1.config(text=started_time1)
                                    drn1.config(text=dur1)
                                    num1.config(text=code_array1)
                                    dispatch1(video_name1, elapsed_time_str1, len(qr_codes_array1), present_date,
                                              present_time, username)
                                    rec1_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record1data WHERE VIDEO_NAME = '{video_name1}'", rec1_data)
                                    df.to_excel(f"./{current_date}/{video_name1}.xlsx", index=False)
                                    rec1_data.close()

                            def start_recording2():
                                global recording2, start_time2, writer2, current_date, starting_time2, qr_codes_array2, data2, started_time2, camera2, first_detection_times2, elapsed_time_str2, video_name2
                                recording2 = True
                                start_time2 = None
                                data2 = ' '
                                qr_codes_array2 = []
                                first_detection_times2 = {}
                                live_time = datetime.now()
                                starting_time2 = current_time.strftime("%I-%M %p")
                                started_time2 = live_time.strftime("%I:%M %p")
                                num2.config(text=0)
                                strt2.config(text=0)
                                drn2.config(text=0)
                                camera2 = "CAM2"
                                time_2 = time2.get()
                                video_name2 = f'{camera2}-{time_2}'

                                print("Camera2 Recording")
                                writer2 = cv2.VideoWriter(f"./{current_date}/{video_name2}.mp4", fourcc1, 23.0,
                                                          (640, 480))

                            def stop_recording2():
                                global recording2, writer2, start_time2, code_array2, elapsed_time_str2
                                recording2 = False

                                if writer2 is not None:
                                    writer2.release()

                                elapsed_time2 = datetime.now() - start_time2
                                elapsed_time_str2 = str(elapsed_time2).split(".")[0]
                                dur2 = elapsed_time_str2
                                print("Camera2 stopped")
                                code_array2 = len(qr_codes_array2)
                                print("No Of detected QR codes in camera2:", code_array2)

                                if len(first_detection_times2) == 0:
                                    print("No data in camera2")

                                else:
                                    strt2.config(text=started_time2)
                                    drn2.config(text=dur2)
                                    num2.config(text=code_array2)

                                    dispatch2(video_name2, elapsed_time_str2, len(qr_codes_array2), present_date,
                                              present_time, username)

                                    rec2_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record2data WHERE VIDEO_NAME = '{video_name2}'", rec2_data)
                                    df.to_excel(f"./{current_date}/{video_name2}.xlsx", index=False)
                                    rec2_data.close()

                                    ################################    CAM3    RECORDING    ##################################

                            def start_recording3():
                                global recording3, start_time3, writer3, current_date, starting_time3, qr_codes_array3, data3, started_time3, camera3, elapsed_time_str3, first_detection_times3, video_name3
                                recording3 = True
                                start_time3 = None
                                data3 = ' '
                                qr_codes_array3 = []
                                camera3 = "CAM3"
                                time_3 = time3.get()
                                video_name3 = f'{camera3}-{time_3}'
                                live_time = datetime.now()
                                first_detection_times3 = {}
                                starting_time3 = current_time.strftime("%I-%M %p")
                                started_time3 = live_time.strftime("%I:%M %p")
                                start_time3 = None
                                print("Camera3 Recording")
                                writer3 = cv2.VideoWriter(f"./{current_date}/{video_name3}.mp4", fourcc3, 23.0,
                                                          (640, 480))

                            def stop_recording3():
                                global recording3, writer3, start_time3, clip_name3, code_array3, elapsed_time_str3
                                recording3 = False
                                if writer3 is not None:
                                    writer3.release()
                                elapsed_time3 = datetime.now() - start_time3
                                elapsed_time_str3 = str(elapsed_time3).split(".")[0]
                                dur3 = elapsed_time_str3
                                print("Camera3 stopped")
                                code_array3 = len(qr_codes_array3)
                                print("No Of detected QR codes in camera3:", code_array3)

                                if len(first_detection_times3) == 0:
                                    print("No data")
                                else:
                                    strt3.config(text=started_time3)
                                    drn3.config(text=dur3)
                                    num3.config(text=code_array3)
                                    dispatch3(video_name3, elapsed_time_str3, len(qr_codes_array3), present_date,
                                              present_time, username)
                                    rec3_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record3data WHERE VIDEO_NAME = '{video_name3}'", rec3_data)
                                    df.to_excel(f"./{current_date}/{video_name3}.xlsx", index=False)
                                    rec3_data.close()

                                    ################################    CAM4    RECORDING    ##################################

                            def start_recording4():
                                global recording4, start_time4, writer4, current_datz, starting_time4, qr_codes_array4, data4, started_time4, camera4, first_detection_times4, elapsed_time_str4, video_name4
                                recording4 = True
                                start_time4 = None
                                data4 = ' '
                                qr_codes_array4 = []
                                first_detection_times4 = {}
                                live_time = datetime.now()
                                starting_time4 = current_time.strftime("%I-%M %p")
                                started_time4 = live_time.strftime("%I:%M %p")
                                num4.config(text=0)
                                strt4.config(text=0)
                                drn4.config(text=0)
                                camera4 = "CAM4"
                                time_4 = time4.get()
                                video_name4 = f'{camera4}-{time_4}'
                                print("Camera4 Recording")
                                writer4 = cv2.VideoWriter(f"./{current_date}/{video_name4}.mp4", fourcc4, 23.0,
                                                          (640, 480))

                            def stop_recording4():
                                global recording4, writer4, start_time4, code_array4, elapsed_time_str4
                                recording4 = False
                                if writer4 is not None:
                                    writer4.release()
                                elapsed_time4 = datetime.now() - start_time4
                                elapsed_time_str4 = str(elapsed_time4).split(".")[0]
                                dur4 = elapsed_time_str4
                                print("Camera4 stopped")
                                code_array4 = len(qr_codes_array4)
                                print("No Of detected QR codes in camera4:", code_array4)
                                if len(first_detection_times4) == 0:
                                    print("No data in camera4")
                                else:
                                    strt4.config(text=started_time4)
                                    drn4.config(text=dur4)
                                    num4.config(text=code_array4)
                                    dispatch4(video_name4, elapsed_time_str4, len(qr_codes_array4), present_date,
                                              present_time, username)
                                    rec4_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record4data WHERE VIDEO_NAME = '{video_name4}'", rec4_data)
                                    df.to_excel(f"./{current_date}/{video_name4}.xlsx", index=False)
                                    rec4_data.close()

                            cap1 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
                            cap2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)
                            cap3 = cv2.VideoCapture(3, cv2.CAP_DSHOW)
                            cap4 = cv2.VideoCapture(4, cv2.CAP_DSHOW)

                            cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap3.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap3.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap4.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap4.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            fourcc1 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time1 = datetime.now().strftime("%H-%M")
                            fourcc2 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time2 = datetime.now().strftime("%H-%M")
                            fourcc3 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time3 = datetime.now().strftime("%H-%M")
                            fourcc4 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time4 = datetime.now().strftime("%H-%M")

                            def process_frame():
                                global recording1, recording2, recording3, start_time1, start_time2, start_time3, start_time4, writer1, writer2, writer3, writer4, end_time1, end_time2, end_time3, data1, data2, data3, data4, code_array1, code_array2, present_date, present_time, elapsed_time_str1, elapsed_time_str2, elapsed_time_str3, elapsed_time_str4
                                # CAM CCTV
                                ret1, frame1 = cap1.read()
                                cv2.putText(frame1, "CAM1", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret1:
                                    if recording1:
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
                                                    f"QR code {data1} detected for the first time at{elapsed_time_str1} on {present_date}-{present_time} ")
                                                scan1(data1, elapsed_time_str1, present_date, present_time, video_name1, username)

                                            for qr_code1 in qr_codes1:
                                                (x, y, w, h) = qr_code1.rect
                                                cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code1.rect
                                                cv2.putText(frame1, data1, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

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
                                    cv2.imshow("Recording Camera cctv", blank_frame1)

                                # CAM2
                                ret2, frame2 = cap2.read()
                                cv2.putText(frame2, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret2:
                                    if recording2:
                                        qr_codes2 = decode(frame2)
                                        for qr_code2 in qr_codes2:
                                            data2 = qr_code2.data.decode('utf-8')
                                            if data2 not in first_detection_times2:
                                                first_detection_times2[data2] = cap2.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array2.append(data2)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data2} detected for the first time at{elapsed_time_str2} on {present_date}-{present_time} ")
                                                scan2(data2, elapsed_time_str2, present_date, present_time, video_name2, username)

                                            for qr_code2 in qr_codes2:
                                                (x, y, w, h) = qr_code2.rect
                                                cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code2.rect
                                                cv2.putText(frame2, data2, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array2) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time2 is None:
                                            start_time2 = datetime.now()

                                        elapsed_time2 = datetime.now() - start_time2
                                        elapsed_time_str2 = str(elapsed_time2).split(".")[0]
                                        cv2.putText(frame2, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame2, f"START TIME:  {started_time2}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame2, f"DURATION:    {elapsed_time_str2}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame2, f"NO OF DATA:  {len(qr_codes_array2)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame2, f"LAST DATA:   {data2}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        writer2.write(frame2)
                                    cv2.imshow("Recording Camera 2", frame2)

                                if not ret2:
                                    blank_frame2 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame2, "CAM2 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 2", blank_frame2)

                                # CAM3
                                ret3, frame3 = cap3.read()
                                cv2.putText(frame3, "CAM3", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret3:
                                    if recording3:
                                        qr_codes3 = decode(frame3)
                                        for qr_code3 in qr_codes3:
                                            data3 = qr_code3.data.decode('utf-8')
                                            if data3 not in first_detection_times3:
                                                first_detection_times3[data3] = cap2.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array3.append(data3)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data3} detected for the first time at{elapsed_time_str3} on {present_date}-{present_time} ")
                                                scan3(data3, elapsed_time_str3, present_date, present_time, video_name3, username)

                                            for qr_code3 in qr_codes3:
                                                (x, y, w, h) = qr_code3.rect
                                                cv2.rectangle(frame3, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code3.rect
                                                cv2.putText(frame3, data3, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array3) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time3 is None:
                                            start_time3 = datetime.now()

                                        elapsed_time3 = datetime.now() - start_time3
                                        elapsed_time_str3 = str(elapsed_time3).split(".")[0]
                                        cv2.putText(frame3, "CAM3", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame3, f"START TIME:  {started_time3}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame3, f"DURATION:    {elapsed_time_str3}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame3, f"NO OF DATA:  {len(qr_codes_array3)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame3, f"LAST DATA:   {data3}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        writer3.write(frame3)
                                    cv2.imshow("Recording Camera 3", frame3)

                                if not ret3:
                                    blank_frame3 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame3, "CAM3 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 3", blank_frame3)

                                # CAM4
                                ret4, frame4 = cap4.read()
                                cv2.putText(frame4, "CAM4", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret4:
                                    if recording4:
                                        qr_codes4 = decode(frame4)
                                        for qr_code4 in qr_codes4:
                                            data4 = qr_code4.data.decode('utf-8')
                                            if data4 not in first_detection_times4:
                                                first_detection_times4[data4] = cap2.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array4.append(data4)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data4} detected for the first time at{elapsed_time_str4} on {present_date}-{present_time} ")
                                                scan4(data4, elapsed_time_str4, present_date, present_time, video_name4, username)

                                            for qr_code4 in qr_codes4:
                                                (x, y, w, h) = qr_code4.rect
                                                cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code4.rect
                                                cv2.putText(frame4, data4, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array4) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time4 is None:
                                            start_time4 = datetime.now()

                                        elapsed_time4 = datetime.now() - start_time4
                                        elapsed_time_str4 = str(elapsed_time4).split(".")[0]
                                        cv2.putText(frame4, "CAM4", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame4, f"START TIME:  {started_time4}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame4, f"DURATION:    {elapsed_time_str4}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame4, f"NO OF DATA:  {len(qr_codes_array4)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame4, f"LAST DATA:   {data4}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255),
                                                    1)
                                        writer4.write(frame4)
                                    cv2.imshow("Recording Camera 4", frame4)

                                if not ret4:
                                    blank_frame4 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame4, "CAM4 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 4", blank_frame4)

                                cv2.waitKey(1)
                                controller.after(1, process_frame)

                            def start():
                                start_recording1()
                                start_recording2()
                                start_recording3()
                                start_recording4()

                            def stop():
                                stop_recording1()
                                stop_recording2()
                                stop_recording3()
                                stop_recording4()

                            def close_window():
                                cap1.release()
                                cap2.release()
                                cap3.release()
                                cap4.release()
                                cv2.destroyAllWindows()
                                controller.destroy()

                            controller = tk.Tk()
                            controller.geometry("600x700")
                            controller.title("VIDEO CONTROLLER")
                            controller.resizable(0, 0)
                            start = tk.Button(controller, text="START", command=start)
                            start.place(x=80, y=20)
                            stop = tk.Button(controller, text="STOP", command=stop)
                            stop.place(x=180, y=20)
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
                            ####################    CAM2
                            cam2 = tk.Label(controller, text="CAMERA 2", fg='red')
                            cam2.place(x=20, y=240)
                            get_time2 = tk.Label(controller, text='Enter Time')
                            get_time2.place(x=60, y=270)
                            time2 = tk.Entry(controller)
                            time2.place(x=160, y=270)
                            start_button_2 = tk.Button(controller, text="START CAM2", command=start_recording2)
                            start_button_2.place(x=60, y=300)
                            stop_button_2 = tk.Button(controller, text="STOP CAM2", command=stop_recording2)
                            stop_button_2.place(x=160, y=300)
                            ####################    CAM2
                            Start_timing2 = tk.Label(controller, text="START TIME")
                            Start_timing2.place(x=60, y=330)
                            strt2 = tk.Label(controller, text="0:0")
                            strt2.place(x=210, y=330)
                            Duration_time2 = tk.Label(controller, text="DURATION")
                            Duration_time2.place(x=60, y=360)
                            drn2 = tk.Label(controller, text="0:0:0")
                            drn2.place(x=210, y=360)
                            NOD2 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD2.place(x=60, y=390)
                            num2 = tk.Label(controller, text="0")
                            num2.place(x=210, y=390)
                            ####################    CAM3
                            cam3 = tk.Label(controller, text="CAMERA 3", fg='violet')
                            cam3.place(x=20, y=420)
                            get_time3 = tk.Label(controller, text='Enter Time')
                            get_time3.place(x=60, y=450)
                            time3 = tk.Entry(controller)
                            time3.place(x=160, y=450)
                            start_button_3 = tk.Button(controller, text="START CAM3", command=start_recording3)
                            start_button_3.place(x=60, y=480)
                            stop_button_3 = tk.Button(controller, text="STOP CAM3", command=stop_recording3)
                            stop_button_3.place(x=160, y=480)
                            ####################    CAM3
                            Start_timing3 = tk.Label(controller, text="START TIME")
                            Start_timing3.place(x=60, y=510)
                            strt3 = tk.Label(controller, text="0:0")
                            strt3.place(x=210, y=510)
                            Duration_time3 = tk.Label(controller, text="DURATION")
                            Duration_time3.place(x=60, y=540)
                            drn3 = tk.Label(controller, text="0:0:0")
                            drn3.place(x=210, y=540)
                            NOD3 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD3.place(x=60, y=570)
                            num3 = tk.Label(controller, text="0")
                            num3.place(x=210, y=570)
                            ####################    CAM4
                            cam4 = tk.Label(controller, text="CAMERA 4", fg='skyblue')
                            cam4.place(x=320, y=60)
                            get_time4 = tk.Label(controller, text='Enter Time')
                            get_time4.place(x=360, y=90)
                            time4 = tk.Entry(controller)
                            time4.place(x=460, y=90)
                            start_button_4 = tk.Button(controller, text="START CAM4", command=start_recording4)
                            start_button_4.place(x=360, y=120)
                            stop_button_4 = tk.Button(controller, text="STOP CAM4", command=stop_recording4)
                            stop_button_4.place(x=460, y=120)
                            ####################    CAM4
                            Start_timing4 = tk.Label(controller, text="START TIME")
                            Start_timing4.place(x=360, y=150)
                            strt4 = tk.Label(controller, text="0:0")
                            strt4.place(x=510, y=150)
                            Duration_time4 = tk.Label(controller, text="DURATION")
                            Duration_time4.place(x=360, y=180)
                            drn4 = tk.Label(controller, text="0:0:0")
                            drn4.place(x=510, y=180)
                            NOD4 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD4.place(x=360, y=210)
                            num4 = tk.Label(controller, text="0")
                            num4.place(x=510, y=210)
                            ######################  CLOSE

                            close_button = tk.Button(controller, text="CLOSE", command=close_window)
                            close_button.place(x=130, y=640)

                            process_frame()
                            controller.mainloop()
                            cap1.release()
                            cap2.release()
                            cap3.release()
                            cap4.release()
                            cv2.destroyAllWindows()

                        elif selected_value == "5":

                            ################################    CAM1    RECORDING    ##################################
                            def start_recording1():
                                global recording1, start_time1, writer1, current_date, starting_time1, started_time1, elapsed_time_str1, first_detection_times1, camera1, data1, qr_codes_array1, video_name1
                                recording1 = True
                                data1 = ' '
                                start_time1 = None
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
                                global recording1, writer1, start_time1, elapsed_time_str1, code_array1
                                recording1 = False
                                print("Camera1 Stopped")
                                if writer1 is not None:
                                    writer1.release()

                                elapsed_time1 = datetime.now() - start_time1
                                elapsed_time_str1 = str(elapsed_time1).split(".")[0]
                                dur1 = elapsed_time_str1
                                code_array1 = len(qr_codes_array1)
                                print("no in 1 camera", code_array1)

                                if len(first_detection_times1) == 0:
                                    print("no")

                                else:
                                    strt1.config(text=started_time1)
                                    drn1.config(text=dur1)
                                    num1.config(text=code_array1)
                                    dispatch1(video_name1, elapsed_time_str1, len(qr_codes_array1), present_date,
                                              present_time, username)
                                    rec1_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record1data WHERE VIDEO_NAME = '{video_name1}'", rec1_data)
                                    df.to_excel(f"./{current_date}/{video_name1}.xlsx", index=False)
                                    rec1_data.close()

                            def start_recording2():
                                global recording2, start_time2, writer2, current_date, starting_time2, qr_codes_array2, data2, started_time2, camera2, first_detection_times2, elapsed_time_str2, video_name2
                                recording2 = True
                                start_time2 = None
                                data2 = ' '
                                qr_codes_array2 = []
                                first_detection_times2 = {}
                                live_time = datetime.now()
                                starting_time2 = current_time.strftime("%I-%M %p")
                                started_time2 = live_time.strftime("%I:%M %p")
                                num2.config(text=0)
                                strt2.config(text=0)
                                drn2.config(text=0)
                                camera2 = "CAM2"
                                time_2 = time2.get()
                                video_name2 = f'{camera2}-{time_2}'

                                print("Camera2 Recording")
                                writer2 = cv2.VideoWriter(f"./{current_date}/{video_name2}.mp4", fourcc1, 23.0,
                                                          (640, 480))

                            def stop_recording2():
                                global recording2, writer2, start_time2, code_array2, elapsed_time_str2
                                recording2 = False

                                if writer2 is not None:
                                    writer2.release()

                                elapsed_time2 = datetime.now() - start_time2
                                elapsed_time_str2 = str(elapsed_time2).split(".")[0]
                                dur2 = elapsed_time_str2
                                print("Camera2 stopped")
                                code_array2 = len(qr_codes_array2)
                                print("No Of detected QR codes in camera2:", code_array2)

                                if len(first_detection_times2) == 0:
                                    print("No data in camera2")

                                else:
                                    strt2.config(text=started_time2)
                                    drn2.config(text=dur2)
                                    num2.config(text=code_array2)

                                    dispatch2(video_name2, elapsed_time_str2, len(qr_codes_array2), present_date,
                                              present_time, username)

                                    rec2_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record2data WHERE VIDEO_NAME = '{video_name2}'", rec2_data)
                                    df.to_excel(f"./{current_date}/{video_name2}.xlsx", index=False)
                                    rec2_data.close()

                                    ################################    CAM3    RECORDING    ##################################

                            def start_recording3():
                                global recording3, start_time3, writer3, current_date, starting_time3, qr_codes_array3, data3, started_time3, camera3, elapsed_time_str3, first_detection_times3, video_name3
                                recording3 = True
                                start_time3 = None
                                data3 = ' '
                                qr_codes_array3 = []
                                camera3 = "CAM3"
                                time_3 = time3.get()
                                video_name3 = f'{camera3}-{time_3}'
                                live_time = datetime.now()
                                first_detection_times3 = {}
                                starting_time3 = current_time.strftime("%I-%M %p")
                                started_time3 = live_time.strftime("%I:%M %p")
                                start_time3 = None
                                print("Camera3 Recording")
                                writer3 = cv2.VideoWriter(f"./{current_date}/{camera3}-{starting_time}.mp4", fourcc3,
                                                          23.0, (640, 480))

                            def stop_recording3():
                                global recording3, writer3, start_time3, clip_name3, code_array3, elapsed_time_str3
                                recording3 = False
                                if writer3 is not None:
                                    writer3.release()
                                elapsed_time3 = datetime.now() - start_time3
                                elapsed_time_str3 = str(elapsed_time3).split(".")[0]
                                dur3 = elapsed_time_str3
                                print("Camera3 stopped")
                                code_array3 = len(qr_codes_array3)
                                print("No Of detected QR codes in camera3:", code_array3)

                                if len(first_detection_times3) == 0:
                                    print("No data")
                                else:
                                    strt3.config(text=started_time3)
                                    drn3.config(text=dur3)
                                    num3.config(text=code_array3)
                                    dispatch3(video_name3, elapsed_time_str3, len(qr_codes_array3), present_date,
                                              present_time, username)
                                    rec3_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record3data WHERE VIDEO_NAME = '{video_name3}'", rec3_data)
                                    df.to_excel(f"./{current_date}/{video_name3}.xlsx", index=False)
                                    rec3_data.close()

                                    ################################    CAM4    RECORDING    ##################################

                            def start_recording4():
                                global recording4, start_time4, writer4, current_data, starting_time4, qr_codes_array4, data4, started_time4, camera4, first_detection_times4, elapsed_time_str4, video_name4
                                recording4 = True
                                start_time4 = None
                                data4 = ' '
                                qr_codes_array4 = []
                                first_detection_times4 = {}
                                live_time = datetime.now()
                                starting_time4 = current_time.strftime("%I-%M %p")
                                started_time4 = live_time.strftime("%I:%M %p")
                                num4.config(text=0)
                                strt4.config(text=0)
                                drn4.config(text=0)
                                camera4 = "CAM4"
                                time_4 = time4.get()
                                video_name4 = f'{camera4}-{time_4}'
                                print("Camera4 Recording")
                                writer4 = cv2.VideoWriter(f"./{current_date}/{camera4}-{starting_time}.mp4", fourcc4,
                                                          23.0,
                                                          (640, 480))

                            def stop_recording4():
                                global recording4, writer4, start_time4, code_array4, elapsed_time_str4
                                recording4 = False
                                if writer4 is not None:
                                    writer4.release()
                                elapsed_time4 = datetime.now() - start_time4
                                elapsed_time_str4 = str(elapsed_time4).split(".")[0]
                                dur4 = elapsed_time_str4
                                print("Camera4 stopped")
                                code_array4 = len(qr_codes_array4)
                                print("No Of detected QR codes in camera4:", code_array4)
                                if len(first_detection_times4) == 0:
                                    print("No data in camera4")
                                else:
                                    strt4.config(text=started_time4)
                                    drn4.config(text=dur4)
                                    num4.config(text=code_array4)
                                    dispatch4(video_name4, elapsed_time_str4, len(qr_codes_array4), present_date,
                                              present_time, username)
                                    rec4_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record4data WHERE VIDEO_NAME = '{video_name4}'", rec4_data)
                                    df.to_excel(f"./{current_date}/{video_name4}.xlsx", index=False)
                                    rec4_data.close()

                            def start_recording5():
                                global recording5, start_time5, writer5, current_data, starting_time5, qr_codes_array5, data5, started_time5, camera5, first_detection_times5, elapsed_time_str5, video_name5
                                recording5 = True
                                start_time5 = None
                                data5 = ' '
                                qr_codes_array5 = []
                                first_detection_times5 = {}
                                live_time = datetime.now()
                                starting_time5 = current_time.strftime("%I-%M %p")
                                started_time5 = live_time.strftime("%I:%M %p")
                                num5.config(text=0)
                                strt5.config(text=0)
                                drn5.config(text=0)
                                camera5 = "CAM5"
                                time_5 = time5.get()
                                video_name5 = f'{camera5}-{time_5}'
                                print("Camera5 Recording")
                                writer5 = cv2.VideoWriter(f"./{current_date}/{camera5}-{starting_time}.mp4", fourcc5,
                                                          23.0,
                                                          (1280, 720))

                            def stop_recording5():
                                global recording5, writer5, start_time5, code_array5, elapsed_time_str5
                                recording5 = False
                                if writer5 is not None:
                                    writer5.release()
                                elapsed_time5 = datetime.now() - start_time5
                                elapsed_time_str5 = str(elapsed_time5).split(".")[0]
                                dur5 = elapsed_time_str5
                                print("Camera5 stopped")
                                code_array5 = len(qr_codes_array5)
                                print("No Of detected QR codes in camera5:", code_array5)
                                if len(first_detection_times5) == 0:
                                    print("No data in camera5")
                                else:
                                    strt5.config(text=started_time5)
                                    drn5.config(text=dur5)
                                    num5.config(text=code_array5)
                                    dispatch5(video_name5, elapsed_time_str5, len(qr_codes_array5), present_date,
                                              present_time, username)
                                    rec5_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record5data WHERE VIDEO_NAME = '{video_name5}'", rec5_data)
                                    df.to_excel(f"./{current_date}/{video_name5}.xlsx", index=False)
                                    rec5_data.close()

                            cap1 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
                            cap2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)
                            cap3 = cv2.VideoCapture(3, cv2.CAP_DSHOW)
                            cap4 = cv2.VideoCapture(4, cv2.CAP_DSHOW)
                            cap5 = cv2.VideoCapture(5, cv2.CAP_DSHOW)

                            cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap3.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap3.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap4.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap4.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap5.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap5.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            fourcc1 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time1 = datetime.now().strftime("%H-%M")
                            fourcc2 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time2 = datetime.now().strftime("%H-%M")
                            fourcc3 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time3 = datetime.now().strftime("%H-%M")
                            fourcc4 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time4 = datetime.now().strftime("%H-%M")
                            fourcc5 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time5 = datetime.now().strftime("%H-%M")

                            def process_frame():
                                global recording1, recording2, recording3, recording4, recording5, start_time1, start_time2, start_time3, start_time4, start_time5, writer1, writer2, writer3, writer4, writer5, end_time1, end_time2, end_time3, data1, data2, data3, data4, data5, code_array1, code_array2, present_date, present_time, elapsed_time_str1, elapsed_time_str2, elapsed_time_str3, elapsed_time_str4, elapsed_time_str5
                                # CAM CCTV
                                ret1, frame1 = cap1.read()
                                cv2.putText(frame1, "CAM1", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret1:
                                    if recording1:
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
                                                    f"QR code {data1} detected for the first time at{elapsed_time_str1} on {present_date}-{present_time} ")
                                                scan1(data1, elapsed_time_str1, present_date, present_time, video_name1, username)

                                            for qr_code1 in qr_codes1:
                                                (x, y, w, h) = qr_code1.rect
                                                cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code1.rect
                                                cv2.putText(frame1, data1, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array1) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time1 is None:
                                            start_time1 = datetime.now()

                                        elapsed_time1 = datetime.now() - start_time1
                                        elapsed_time_str1 = str(elapsed_time1).split(".")[0]
                                        cv2.putText(frame1, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
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
                                    cv2.imshow("Recording Camera cctv", blank_frame1)

                                # CAM2
                                ret2, frame2 = cap2.read()
                                cv2.putText(frame2, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret2:
                                    if recording2:
                                        qr_codes2 = decode(frame2)
                                        for qr_code2 in qr_codes2:
                                            data2 = qr_code2.data.decode('utf-8')
                                            if data2 not in first_detection_times2:
                                                first_detection_times2[data2] = cap2.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array2.append(data2)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data2} detected for the first time at{elapsed_time_str2} on {present_date}-{present_time} ")
                                                scan2(data2, elapsed_time_str2, present_date, present_time, video_name2, username)

                                            for qr_code2 in qr_codes2:
                                                (x, y, w, h) = qr_code2.rect
                                                cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code2.rect
                                                cv2.putText(frame2, data2, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array2) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time2 is None:
                                            start_time2 = datetime.now()

                                        elapsed_time2 = datetime.now() - start_time2
                                        elapsed_time_str2 = str(elapsed_time2).split(".")[0]
                                        cv2.putText(frame2, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame2, f"START TIME:  {started_time2}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame2, f"DURATION:    {elapsed_time_str2}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame2, f"NO OF DATA:  {len(qr_codes_array2)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame2, f"LAST DATA:   {data2}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255),
                                                    1)
                                        writer2.write(frame2)
                                    cv2.imshow("Recording Camera 2", frame2)

                                if not ret2:
                                    blank_frame2 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame2, "CAM2 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 2", blank_frame2)

                                # CAM3
                                ret3, frame3 = cap3.read()
                                cv2.putText(frame3, "CAM3", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret3:
                                    if recording3:
                                        qr_codes3 = decode(frame3)
                                        for qr_code3 in qr_codes3:
                                            data3 = qr_code3.data.decode('utf-8')
                                            if data3 not in first_detection_times3:
                                                first_detection_times3[data3] = cap3.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array3.append(data3)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data3} detected for the first time at{elapsed_time_str3} on {present_date}-{present_time} ")
                                                scan3(data3, elapsed_time_str3, present_date, present_time, video_name3, username)

                                            for qr_code3 in qr_codes3:
                                                (x, y, w, h) = qr_code3.rect
                                                cv2.rectangle(frame3, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code3.rect
                                                cv2.putText(frame3, data3, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array3) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time3 is None:
                                            start_time3 = datetime.now()

                                        elapsed_time3 = datetime.now() - start_time3
                                        elapsed_time_str3 = str(elapsed_time3).split(".")[0]
                                        cv2.putText(frame3, "CAM3", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame3, f"START TIME:  {started_time3}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame3, f"DURATION:    {elapsed_time_str3}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame3, f"NO OF DATA:  {len(qr_codes_array3)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame3, f"LAST DATA:   {data3}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255),
                                                    1)
                                        writer3.write(frame3)
                                    cv2.imshow("Recording Camera 3", frame3)

                                if not ret3:
                                    blank_frame3 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame3, "CAM3 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 3", blank_frame3)

                                # CAM4
                                ret4, frame4 = cap4.read()
                                cv2.putText(frame4, "CAM4", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret4:
                                    if recording4:
                                        qr_codes4 = decode(frame4)
                                        for qr_code4 in qr_codes4:
                                            data4 = qr_code4.data.decode('utf-8')
                                            if data4 not in first_detection_times4:
                                                first_detection_times4[data4] = cap4.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array4.append(data4)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data4} detected for the first time at{elapsed_time_str4} on {present_date}-{present_time} ")
                                                scan4(data4, elapsed_time_str4, present_date, present_time, video_name4, username)

                                            for qr_code4 in qr_codes4:
                                                (x, y, w, h) = qr_code4.rect
                                                cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code4.rect
                                                cv2.putText(frame4, data4, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array4) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time4 is None:
                                            start_time4 = datetime.now()

                                        elapsed_time4 = datetime.now() - start_time4
                                        elapsed_time_str4 = str(elapsed_time4).split(".")[0]
                                        cv2.putText(frame4, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame4, f"START TIME:  {started_time4}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame4, f"DURATION:    {elapsed_time_str4}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame4, f"NO OF DATA:  {len(qr_codes_array4)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame4, f"LAST DATA:   {data4}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255),
                                                    1)
                                        writer4.write(frame4)
                                    cv2.imshow("Recording Camera 4", frame4)

                                if not ret4:
                                    blank_frame4 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame4, "CAM4 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 4", blank_frame4)
                                # CAM5
                                ret5, frame5 = cap5.read()
                                cv2.putText(frame5, "CAM5", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret5:
                                    if recording5:
                                        qr_codes5 = decode(frame5)
                                        for qr_code5 in qr_codes5:
                                            data5 = qr_code5.data.decode('utf-8')
                                            if data5 not in first_detection_times5:
                                                first_detection_times5[data5] = cap5.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array5.append(data5)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data5} detected for the first time at{elapsed_time_str5} on {present_date}-{present_time} ")
                                                scan5(data5, elapsed_time_str5, present_date, present_time, video_name5, username)

                                            for qr_code5 in qr_codes5:
                                                (x, y, w, h) = qr_code5.rect
                                                cv2.rectangle(frame5, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code5.rect
                                                cv2.putText(frame5, data5, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array5) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time5 is None:
                                            start_time5 = datetime.now()

                                        elapsed_time5 = datetime.now() - start_time5
                                        elapsed_time_str5 = str(elapsed_time5).split(".")[0]
                                        cv2.putText(frame5, "CAM5", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame5, f"START TIME:  {started_time5}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame5, f"DURATION:    {elapsed_time_str5}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame5, f"NO OF DATA:  {len(qr_codes_array5)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame5, f"LAST DATA:   {data5}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255),
                                                    1)
                                        writer5.write(frame5)
                                    cv2.imshow("Recording Camera 5", frame5)

                                if not ret5:
                                    blank_frame5 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame5, "CAM5 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 5", blank_frame5)

                                cv2.waitKey(1)
                                controller.after(1, process_frame)

                            def start():
                                start_recording1()
                                start_recording2()
                                start_recording3()
                                start_recording4()
                                start_recording5()

                            def stop():
                                stop_recording1()
                                stop_recording2()
                                stop_recording3()
                                stop_recording4()
                                stop_recording5()

                            def close_window():
                                cap1.release()
                                cap2.release()
                                cap3.release()
                                cap4.release()
                                cap5.release()
                                cv2.destroyAllWindows()
                                controller.destroy()

                            controller = tk.Tk()
                            controller.geometry("600x700")
                            controller.title("VIDEO CONTROLLER")
                            controller.resizable(0, 0)
                            start = tk.Button(controller, text="START", command=start)
                            start.place(x=80, y=20)
                            stop = tk.Button(controller, text="STOP", command=stop)
                            stop.place(x=180, y=20)
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
                            ####################    CAM2
                            cam2 = tk.Label(controller, text="CAMERA 2", fg='red')
                            cam2.place(x=20, y=240)
                            get_time2 = tk.Label(controller, text='Enter Time')
                            get_time2.place(x=60, y=270)
                            time2 = tk.Entry(controller)
                            time2.place(x=160, y=270)
                            start_button_2 = tk.Button(controller, text="START CAM2", command=start_recording2)
                            start_button_2.place(x=60, y=300)
                            stop_button_2 = tk.Button(controller, text="STOP CAM2", command=stop_recording2)
                            stop_button_2.place(x=160, y=300)
                            ####################    CAM2
                            Start_timing2 = tk.Label(controller, text="START TIME")
                            Start_timing2.place(x=60, y=330)
                            strt2 = tk.Label(controller, text="0:0")
                            strt2.place(x=210, y=330)
                            Duration_time2 = tk.Label(controller, text="DURATION")
                            Duration_time2.place(x=60, y=360)
                            drn2 = tk.Label(controller, text="0:0:0")
                            drn2.place(x=210, y=360)
                            NOD2 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD2.place(x=60, y=390)
                            num2 = tk.Label(controller, text="0")
                            num2.place(x=210, y=390)
                            ####################    CAM3
                            cam3 = tk.Label(controller, text="CAMERA 3", fg='violet')
                            cam3.place(x=20, y=420)
                            get_time3 = tk.Label(controller, text='Enter Time')
                            get_time3.place(x=60, y=450)
                            time3 = tk.Entry(controller)
                            time3.place(x=160, y=450)
                            start_button_3 = tk.Button(controller, text="START CAM3", command=start_recording3)
                            start_button_3.place(x=60, y=480)
                            stop_button_3 = tk.Button(controller, text="STOP CAM3", command=stop_recording3)
                            stop_button_3.place(x=160, y=480)
                            ####################    CAM3
                            Start_timing3 = tk.Label(controller, text="START TIME")
                            Start_timing3.place(x=60, y=510)
                            strt3 = tk.Label(controller, text="0:0")
                            strt3.place(x=210, y=510)
                            Duration_time3 = tk.Label(controller, text="DURATION")
                            Duration_time3.place(x=60, y=540)
                            drn3 = tk.Label(controller, text="0:0:0")
                            drn3.place(x=210, y=540)
                            NOD3 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD3.place(x=60, y=570)
                            num3 = tk.Label(controller, text="0")
                            num3.place(x=210, y=570)
                            ####################    CAM4
                            cam4 = tk.Label(controller, text="CAMERA 4", fg='skyblue')
                            cam4.place(x=320, y=60)
                            get_time4 = tk.Label(controller, text='Enter Time')
                            get_time4.place(x=360, y=90)
                            time4 = tk.Entry(controller)
                            time4.place(x=460, y=90)
                            start_button_4 = tk.Button(controller, text="START CAM4", command=start_recording4)
                            start_button_4.place(x=360, y=120)
                            stop_button_4 = tk.Button(controller, text="STOP CAM4", command=stop_recording4)
                            stop_button_4.place(x=460, y=120)
                            ####################    CAM4
                            Start_timing4 = tk.Label(controller, text="START TIME")
                            Start_timing4.place(x=360, y=150)
                            strt4 = tk.Label(controller, text="0:0")
                            strt4.place(x=510, y=150)
                            Duration_time4 = tk.Label(controller, text="DURATION")
                            Duration_time4.place(x=360, y=180)
                            drn4 = tk.Label(controller, text="0:0:0")
                            drn4.place(x=510, y=180)
                            NOD4 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD4.place(x=360, y=210)
                            num4 = tk.Label(controller, text="0")
                            num4.place(x=510, y=210)
                            ####################    CAM5
                            cam5 = tk.Label(controller, text="CAMERA 5", fg='black')
                            cam5.place(x=320, y=240)
                            get_time5 = tk.Label(controller, text='Enter Time')
                            get_time5.place(x=360, y=270)
                            time5 = tk.Entry(controller)
                            time5.place(x=460, y=270)
                            start_button_5 = tk.Button(controller, text="START CAM5", command=start_recording5)
                            start_button_5.place(x=360, y=300)
                            stop_button_5 = tk.Button(controller, text="STOP CAM5", command=stop_recording5)
                            stop_button_5.place(x=460, y=300)
                            ####################    CAM5
                            Start_timing5 = tk.Label(controller, text="START TIME")
                            Start_timing5.place(x=360, y=330)
                            strt5 = tk.Label(controller, text="0:0")
                            strt5.place(x=510, y=330)
                            Duration_time5 = tk.Label(controller, text="DURATION")
                            Duration_time5.place(x=360, y=360)
                            drn5 = tk.Label(controller, text="0:0:0")
                            drn5.place(x=510, y=360)
                            NOD5 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD5.place(x=360, y=390)
                            num5 = tk.Label(controller, text="0")
                            num5.place(x=510, y=390)

                            ######################  CLOSE

                            close_button = tk.Button(controller, text="CLOSE", command=close_window)
                            close_button.place(x=130, y=640)

                            process_frame()
                            controller.mainloop()
                            cap1.release()
                            cap2.release()
                            cap3.release()
                            cap4.release()
                            cv2.destroyAllWindows()

                        elif selected_value == "6":

                            ################################    CAM1    RECORDING    ##################################
                            def start_recording1():
                                global recording1, start_time1, writer1, current_date, starting_time1, started_time1, elapsed_time_str1, first_detection_times1, camera1, data1, qr_codes_array1, video_name1
                                recording1 = True
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
                                writer1 = cv2.VideoWriter(f"./{current_date}/{camera1}-{starting_time}.mp4", fourcc1,
                                                          23.0, (640, 480))

                            def stop_recording1():
                                global recording1, writer1, start_time1, elapsed_time_str1, code_array1
                                recording1 = False
                                print("Camera1 Stopped")
                                if writer1 is not None:
                                    writer1.release()

                                elapsed_time1 = datetime.now() - start_time1
                                elapsed_time_str1 = str(elapsed_time1).split(".")[0]
                                dur1 = elapsed_time_str1
                                code_array1 = len(qr_codes_array1)
                                print("no in 1 camera", code_array1)

                                if len(first_detection_times1) == 0:
                                    print("no")

                                else:
                                    strt1.config(text=started_time1)
                                    drn1.config(text=dur1)
                                    num1.config(text=code_array1)
                                    dispatch1(video_name1, elapsed_time_str1, len(qr_codes_array1), present_date,
                                              present_time, username)
                                    rec1_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record1data WHERE VIDEO_NAME = '{video_name1}'", rec1_data)
                                    df.to_excel(f"./{current_date}/{video_name1}.xlsx", index=False)
                                    rec1_data.close()

                            def start_recording2():
                                global recording2, start_time2, writer2, current_date, starting_time2, qr_codes_array2, data2, started_time2, camera2, first_detection_times2, elapsed_time_str2, video_name2
                                recording2 = True
                                start_time2 = None
                                data2 = ' '
                                qr_codes_array2 = []
                                first_detection_times2 = {}
                                live_time = datetime.now()
                                starting_time2 = current_time.strftime("%I-%M %p")
                                started_time2 = live_time.strftime("%I:%M %p")
                                num2.config(text=0)
                                strt2.config(text=0)
                                drn2.config(text=0)
                                camera2 = "CAM2"
                                time_2 = time2.get()
                                video_name2 = f'{camera2}-{time_2}'

                                print("Camera2 Recording")
                                writer2 = cv2.VideoWriter(f"./{current_date}/{camera2}-{starting_time}.mp4", fourcc2,
                                                          23.0, (640, 480))

                            def stop_recording2():
                                global recording2, writer2, start_time2, code_array2, elapsed_time_str2
                                recording2 = False

                                if writer2 is not None:
                                    writer2.release()

                                elapsed_time2 = datetime.now() - start_time2
                                elapsed_time_str2 = str(elapsed_time2).split(".")[0]
                                dur2 = elapsed_time_str2
                                print("Camera2 stopped")
                                code_array2 = len(qr_codes_array2)
                                print("No Of detected QR codes in camera2:", code_array2)

                                if len(first_detection_times2) == 0:
                                    print("No data in camera2")

                                else:
                                    strt2.config(text=started_time2)
                                    drn2.config(text=dur2)
                                    num2.config(text=code_array2)

                                    dispatch2(video_name2, elapsed_time_str2, len(qr_codes_array2), present_date,
                                              present_time, username)

                                    rec2_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record2data WHERE VIDEO_NAME = '{video_name2}'", rec2_data)
                                    df.to_excel(f"./{current_date}/{video_name2}.xlsx", index=False)
                                    rec2_data.close()

                                    ################################    CAM3    RECORDING    ##################################

                            def start_recording3():
                                global recording3, start_time3, writer3, current_date, starting_time3, qr_codes_array3, data3, started_time3, camera3, elapsed_time_str3, first_detection_times3, video_name3
                                recording3 = True
                                start_time3 = None
                                data3 = ' '
                                qr_codes_array3 = []
                                camera3 = "CAM3"
                                time_3 = time3.get()
                                video_name3 = f'{camera3}-{time_3}'
                                live_time = datetime.now()
                                first_detection_times3 = {}
                                starting_time3 = current_time.strftime("%I-%M %p")
                                started_time3 = live_time.strftime("%I:%M %p")
                                start_time3 = None
                                print("Camera3 Recording")
                                writer3 = cv2.VideoWriter(f"./{current_date}/{camera3}-{starting_time}.mp4", fourcc3,
                                                          23.0, (640, 480))

                            def stop_recording3():
                                global recording3, writer3, start_time3, clip_name3, code_array3, elapsed_time_str3
                                recording3 = False
                                if writer3 is not None:
                                    writer3.release()
                                elapsed_time3 = datetime.now() - start_time3
                                elapsed_time_str3 = str(elapsed_time3).split(".")[0]
                                dur3 = elapsed_time_str3
                                print("Camera3 stopped")
                                code_array3 = len(qr_codes_array3)
                                print("No Of detected QR codes in camera3:", code_array3)

                                if len(first_detection_times3) == 0:
                                    print("No data")
                                else:
                                    strt3.config(text=started_time3)
                                    drn3.config(text=dur3)
                                    num3.config(text=code_array3)
                                    dispatch3(video_name3, elapsed_time_str3, len(qr_codes_array3), present_date,
                                              present_time, username)
                                    rec3_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record3data WHERE VIDEO_NAME = '{video_name3}'", rec3_data)
                                    df.to_excel(f"./{current_date}/{video_name3}.xlsx", index=False)
                                    rec3_data.close()

                                    ################################    CAM4    RECORDING    ##################################

                            def start_recording4():
                                global recording4, start_time4, writer4, current_data, starting_time4, qr_codes_array4, data4, started_time4, camera4, first_detection_times4, elapsed_time_str4, video_name4
                                recording4 = True
                                start_time4 = None
                                data4 = ' '
                                qr_codes_array4 = []
                                first_detection_times4 = {}
                                live_time = datetime.now()
                                starting_time4 = current_time.strftime("%I-%M %p")
                                started_time4 = live_time.strftime("%I:%M %p")
                                num4.config(text=0)
                                strt4.config(text=0)
                                drn4.config(text=0)
                                camera4 = "CAM4"
                                time_4 = time4.get()
                                video_name4 = f'{camera4}-{time_4}'
                                print("Camera4 Recording")
                                writer4 = cv2.VideoWriter(f"./{current_date}/{camera4}-{starting_time}.mp4", fourcc4,
                                                          23.0,
                                                          (640, 480))

                            def stop_recording4():
                                global recording4, writer4, start_time4, code_array4, elapsed_time_str4
                                recording4 = False
                                if writer4 is not None:
                                    writer4.release()
                                elapsed_time4 = datetime.now() - start_time4
                                elapsed_time_str4 = str(elapsed_time4).split(".")[0]
                                dur4 = elapsed_time_str4
                                print("Camera4 stopped")
                                code_array4 = len(qr_codes_array4)
                                print("No Of detected QR codes in camera4:", code_array4)
                                if len(first_detection_times4) == 0:
                                    print("No data in camera4")
                                else:
                                    strt4.config(text=started_time4)
                                    drn4.config(text=dur4)
                                    num4.config(text=code_array4)
                                    dispatch4(video_name4, elapsed_time_str4, len(qr_codes_array4), present_date,
                                              present_time, username)
                                    rec4_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record4data WHERE VIDEO_NAME = '{video_name4}'", rec4_data)
                                    df.to_excel(f"./{current_date}/{video_name4}.xlsx", index=False)
                                    rec4_data.close()

                            def start_recording5():
                                global recording5, start_time5, writer5, current_data, starting_time5, qr_codes_array5, data5, started_time5, camera5, first_detection_times5, elapsed_time_str5, video_name5
                                recording5 = True
                                start_time5 = None
                                data5 = ' '
                                qr_codes_array5 = []
                                first_detection_times5 = {}
                                live_time = datetime.now()
                                starting_time5 = current_time.strftime("%I-%M %p")
                                started_time5 = live_time.strftime("%I:%M %p")
                                num5.config(text=0)
                                strt5.config(text=0)
                                drn5.config(text=0)
                                camera5 = "CAM5"
                                time_5 = time5.get()
                                video_name5 = f'{camera5}-{time_5}'
                                print("Camera5 Recording")
                                writer5 = cv2.VideoWriter(f"./{current_date}/{camera5}-{starting_time}.mp4", fourcc5,
                                                          23.0,
                                                          (640, 480))

                            def stop_recording5():
                                global recording5, writer5, start_time5, code_array5, elapsed_time_str5
                                recording5 = False
                                if writer5 is not None:
                                    writer5.release()
                                elapsed_time5 = datetime.now() - start_time5
                                elapsed_time_str5 = str(elapsed_time5).split(".")[0]
                                dur5 = elapsed_time_str5
                                print("Camera5 stopped")
                                code_array5 = len(qr_codes_array5)
                                print("No Of detected QR codes in camera5:", code_array5)
                                if len(first_detection_times5) == 0:
                                    print("No data in camera5")
                                else:
                                    strt5.config(text=started_time5)
                                    drn5.config(text=dur5)
                                    num5.config(text=code_array5)
                                    dispatch5(video_name5, elapsed_time_str5, len(qr_codes_array5), present_date,
                                              present_time, username)
                                    rec5_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record5data WHERE VIDEO_NAME = '{video_name5}'", rec5_data)
                                    df.to_excel(f"./{current_date}/{video_name5}.xlsx", index=False)
                                    rec5_data.close()

                            def start_recording6():
                                global recording6, start_time6, writer6, current_data, starting_time6, qr_codes_array6, data6, started_time6, camera6, first_detection_times6, elapsed_time_str6, video_name6
                                recording6 = True
                                start_time6 = None
                                data6 = ' '
                                qr_codes_array6 = []
                                first_detection_times6 = {}
                                live_time = datetime.now()
                                starting_time6 = current_time.strftime("%I-%M %p")
                                started_time6 = live_time.strftime("%I:%M %p")
                                num6.config(text=0)
                                strt6.config(text=0)
                                drn6.config(text=0)
                                camera6 = "CAM6"
                                time_6 = time6.get()
                                video_name6 = f'{camera6}-{time_6}'
                                print("Camera6 Recording")
                                writer6 = cv2.VideoWriter(f"./{current_date}/{camera6}-{starting_time}.mp4", fourcc6,
                                                          23.0,
                                                          (640, 480))

                            def stop_recording6():
                                global recording6, writer6, start_time6, code_array6, elapsed_time_str6
                                recording6 = False
                                if writer6 is not None:
                                    writer6.release()
                                elapsed_time6 = datetime.now() - start_time6
                                elapsed_time_str6 = str(elapsed_time6).split(".")[0]
                                dur6 = elapsed_time_str6
                                print("Camera6 stopped")
                                code_array6 = len(qr_codes_array6)
                                print("No Of detected QR codes in camera6:", code_array6)
                                if len(first_detection_times6) == 0:
                                    print("No data in camera6")
                                else:
                                    strt6.config(text=started_time6)
                                    drn6.config(text=dur6)
                                    num6.config(text=code_array6)
                                    dispatch6(video_name6, elapsed_time_str6, len(qr_codes_array6), present_date,
                                              present_time, username)
                                    rec6_data = sqlite3.connect('./DATABASES/recording.db')
                                    df = pd.read_sql_query(
                                        f"SELECT * from record6data WHERE VIDEO_NAME = '{video_name6}'", rec6_data)
                                    df.to_excel(f"./{current_date}/{video_name6}.xlsx", index=False)
                                    rec6_data.close()

                            cap1 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
                            cap2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)
                            cap3 = cv2.VideoCapture(3, cv2.CAP_DSHOW)
                            cap4 = cv2.VideoCapture(4, cv2.CAP_DSHOW)
                            cap5 = cv2.VideoCapture(5, cv2.CAP_DSHOW)
                            cap6 = cv2.VideoCapture(6, cv2.CAP_DSHOW)

                            cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap3.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap3.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap4.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap4.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap5.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap5.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            cap6.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap6.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                            fourcc1 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time1 = datetime.now().strftime("%H-%M")
                            fourcc2 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time2 = datetime.now().strftime("%H-%M")
                            fourcc3 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time3 = datetime.now().strftime("%H-%M")
                            fourcc4 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time4 = datetime.now().strftime("%H-%M")
                            fourcc5 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time5 = datetime.now().strftime("%H-%M")
                            fourcc6 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            starting_time6 = datetime.now().strftime("%H-%M")

                            def process_frame():
                                global recording1, recording2, recording3, recording4, recording5, recording6, start_time1, start_time2, start_time3, start_time4, start_time5, start_time6, writer1, writer2, writer3, writer4, writer5, writer6, end_time1, end_time2, end_time3, data1, data2, data3, data4, data5, data6, code_array1, code_array2, present_date, present_time, elapsed_time_str1, elapsed_time_str2, elapsed_time_str3, elapsed_time_str4, elapsed_time_str5, elapsed_time_str6
                                # CAM CCTV
                                ret1, frame1 = cap1.read()
                                cv2.putText(frame1, "CAM1", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret1:
                                    if recording1:
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
                                                    f"QR code {data1} detected for the first time at{elapsed_time_str1} on {present_date}-{present_time} ")
                                                scan1(data1, elapsed_time_str1, present_date, present_time, video_name1, username)

                                            for qr_code1 in qr_codes1:
                                                (x, y, w, h) = qr_code1.rect
                                                cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code1.rect
                                                cv2.putText(frame1, data1, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array1) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time1 is None:
                                            start_time1 = datetime.now()

                                        elapsed_time1 = datetime.now() - start_time1
                                        elapsed_time_str1 = str(elapsed_time1).split(".")[0]
                                        cv2.putText(frame1, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
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
                                    cv2.imshow("Recording Camera cctv", blank_frame1)

                                # CAM2
                                ret2, frame2 = cap2.read()
                                cv2.putText(frame2, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret2:
                                    if recording2:
                                        qr_codes2 = decode(frame2)
                                        for qr_code2 in qr_codes2:
                                            data2 = qr_code2.data.decode('utf-8')
                                            if data2 not in first_detection_times2:
                                                first_detection_times2[data2] = cap2.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array2.append(data2)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data2} detected for the first time at{elapsed_time_str2} on {present_date}-{present_time} ")
                                                scan2(data2, elapsed_time_str2, present_date, present_time, video_name2, username)

                                            for qr_code2 in qr_codes2:
                                                (x, y, w, h) = qr_code2.rect
                                                cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code2.rect
                                                cv2.putText(frame2, data2, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array2) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time2 is None:
                                            start_time2 = datetime.now()

                                        elapsed_time2 = datetime.now() - start_time2
                                        elapsed_time_str2 = str(elapsed_time2).split(".")[0]
                                        cv2.putText(frame2, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame2, f"START TIME:  {started_time2}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame2, f"DURATION:    {elapsed_time_str2}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame2, f"NO OF DATA:  {len(qr_codes_array2)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame2, f"LAST DATA:   {data2}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255),
                                                    1)
                                        writer2.write(frame2)
                                    cv2.imshow("Recording Camera 2", frame2)

                                if not ret2:
                                    blank_frame2 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame2, "CAM2 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 2", blank_frame2)

                                # CAM3
                                ret3, frame3 = cap3.read()
                                cv2.putText(frame3, "CAM3", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret3:
                                    if recording3:
                                        qr_codes3 = decode(frame3)
                                        for qr_code3 in qr_codes3:
                                            data3 = qr_code3.data.decode('utf-8')
                                            if data3 not in first_detection_times3:
                                                first_detection_times3[data3] = cap3.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array3.append(data3)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data3} detected for the first time at{elapsed_time_str3} on {present_date}-{present_time} ")
                                                scan3(data3, elapsed_time_str3, present_date, present_time, video_name3, username)

                                            for qr_code3 in qr_codes3:
                                                (x, y, w, h) = qr_code3.rect
                                                cv2.rectangle(frame3, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code3.rect
                                                cv2.putText(frame3, data3, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array3) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time3 is None:
                                            start_time3 = datetime.now()

                                        elapsed_time3 = datetime.now() - start_time3
                                        elapsed_time_str3 = str(elapsed_time3).split(".")[0]
                                        cv2.putText(frame3, "CAM3", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame3, f"START TIME:  {started_time3}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame3, f"DURATION:    {elapsed_time_str3}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame3, f"NO OF DATA:  {len(qr_codes_array3)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame3, f"LAST DATA:   {data3}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255),
                                                    1)
                                        writer3.write(frame3)
                                    cv2.imshow("Recording Camera 3", frame3)

                                if not ret3:
                                    blank_frame3 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame3, "CAM3 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 3", blank_frame3)

                                # CAM4
                                ret4, frame4 = cap4.read()
                                cv2.putText(frame4, "CAM4", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret4:
                                    if recording4:
                                        qr_codes4 = decode(frame4)
                                        for qr_code4 in qr_codes4:
                                            data4 = qr_code4.data.decode('utf-8')
                                            if data4 not in first_detection_times4:
                                                first_detection_times4[data4] = cap4.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array4.append(data4)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data4} detected for the first time at{elapsed_time_str4} on {present_date}-{present_time} ")
                                                scan4(data4, elapsed_time_str4, present_date, present_time, video_name4, username)

                                            for qr_code4 in qr_codes4:
                                                (x, y, w, h) = qr_code4.rect
                                                cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code4.rect
                                                cv2.putText(frame4, data4, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array4) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time4 is None:
                                            start_time4 = datetime.now()

                                        elapsed_time4 = datetime.now() - start_time4
                                        elapsed_time_str4 = str(elapsed_time4).split(".")[0]
                                        cv2.putText(frame4, "CAM2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame4, f"START TIME:  {started_time4}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame4, f"DURATION:    {elapsed_time_str4}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame4, f"NO OF DATA:  {len(qr_codes_array4)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame4, f"LAST DATA:   {data4}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255),
                                                    1)
                                        writer4.write(frame4)
                                    cv2.imshow("Recording Camera 4", frame4)

                                if not ret4:
                                    blank_frame4 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame4, "CAM4 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 4", blank_frame4)
                                # CAM5
                                ret5, frame5 = cap5.read()
                                cv2.putText(frame5, "CAM5", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret5:
                                    if recording5:
                                        qr_codes5 = decode(frame5)
                                        for qr_code5 in qr_codes5:
                                            data5 = qr_code5.data.decode('utf-8')
                                            if data5 not in first_detection_times5:
                                                first_detection_times5[data5] = cap5.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array5.append(data5)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)
                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')

                                                print(
                                                    f"QR code {data5} detected for the first time at{elapsed_time_str5} on {present_date}-{present_time} ")
                                                scan5(data5, elapsed_time_str5, present_date, present_time, video_name5, username)

                                            for qr_code5 in qr_codes5:
                                                (x, y, w, h) = qr_code5.rect
                                                cv2.rectangle(frame5, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code5.rect
                                                cv2.putText(frame5, data5, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array5) == 0:
                                                print("No QR codes detected!!!!!")

                                        if start_time5 is None:
                                            start_time5 = datetime.now()

                                        elapsed_time5 = datetime.now() - start_time5
                                        elapsed_time_str5 = str(elapsed_time5).split(".")[0]
                                        cv2.putText(frame5, "CAM5", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame5, f"START TIME:  {started_time5}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame5, f"DURATION:    {elapsed_time_str5}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame5, f"NO OF DATA:  {len(qr_codes_array5)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame5, f"LAST DATA:   {data5}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255),
                                                    1)
                                        writer5.write(frame5)
                                    cv2.imshow("Recording Camera 5", frame5)

                                if not ret5:
                                    blank_frame5 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame5, "CAM5 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 5", blank_frame5)

                                # CAM6
                                ret6, frame6 = cap6.read()
                                cv2.putText(frame6, "CAM6", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                if ret6:
                                    if recording6:
                                        qr_codes6 = decode(frame6)
                                        for qr_code6 in qr_codes6:
                                            data6 = qr_code6.data.decode('utf-8')
                                            if data6 not in first_detection_times6:
                                                first_detection_times6[data6] = cap6.get(cv2.CAP_PROP_POS_MSEC) / 1000
                                                qr_codes_array6.append(data6)

                                                frequency = 1000
                                                duration = 500
                                                winsound.Beep(frequency, duration)

                                                present_date = datetime.now().strftime('%Y-%m-%d')
                                                present_time = datetime.now().strftime('%I:%M %p')
                                                print(
                                                    f"QR code {data6} detected for the first time at{elapsed_time_str6} on {present_date}-{present_time} ")
                                                scan6(data6, elapsed_time_str6, present_date, present_time, video_name6, username)

                                            for qr_code6 in qr_codes6:
                                                (x, y, w, h) = qr_code6.rect
                                                cv2.rectangle(frame6, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                pts2 = qr_code6.rect
                                                cv2.putText(frame6, data6, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                                            0.9,
                                                            (255, 0, 255), 1)

                                            if len(qr_codes_array6) == 0:
                                                print("No QR codes detected!!!!!")
                                        if start_time6 is None:
                                            start_time6 = datetime.now()
                                        elapsed_time6 = datetime.now() - start_time6
                                        elapsed_time_str6 = str(elapsed_time6).split(".")[0]
                                        cv2.putText(frame6, "CAM5", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame6, f"START TIME:  {started_time6}", (10, 60),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame6, f"DURATION:    {elapsed_time_str6}", (10, 90),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5,
                                                    (0, 0, 255), 1)
                                        cv2.putText(frame6, f"NO OF DATA:  {len(qr_codes_array6)}", (10, 120),
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, (0, 0, 255), 1)
                                        cv2.putText(frame6, f"LAST DATA:   {data6}", (10, 150),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255),
                                                    1)
                                        writer6.write(frame6)
                                    cv2.imshow("Recording Camera 6", frame6)
                                if not ret6:
                                    blank_frame6 = np.zeros((480, 640, 3), dtype=np.uint8)
                                    cv2.putText(blank_frame6, "CAM6 DISCONNECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5, (0, 0, 255),
                                                1)
                                    cv2.imshow("Recording Camera 6", blank_frame6)

                                cv2.waitKey(1)
                                controller.after(1, process_frame)

                            def start():
                                start_recording1()
                                start_recording2()
                                start_recording3()
                                start_recording4()
                                start_recording5()
                                start_recording6()

                            def stop():
                                stop_recording1()
                                stop_recording2()
                                stop_recording3()
                                stop_recording4()
                                stop_recording5()
                                stop_recording6()

                            def close_window():
                                cap1.release()
                                cap2.release()
                                cap3.release()
                                cap4.release()
                                cap5.release()
                                cap6.release()
                                cv2.destroyAllWindows()
                                controller.destroy()

                            controller = tk.Tk()
                            controller.geometry("600x700")
                            controller.title("VIDEO CONTROLLER")
                            controller.resizable(0, 0)
                            start = tk.Button(controller, text="START", command=start)
                            start.place(x=80, y=20)
                            stop = tk.Button(controller, text="STOP", command=stop)
                            stop.place(x=180, y=20)
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
                            ####################    CAM2
                            cam2 = tk.Label(controller, text="CAMERA 2", fg='red')
                            cam2.place(x=20, y=240)
                            get_time2 = tk.Label(controller, text='Enter Time')
                            get_time2.place(x=60, y=270)
                            time2 = tk.Entry(controller)
                            time2.place(x=160, y=270)
                            start_button_2 = tk.Button(controller, text="START CAM2", command=start_recording2)
                            start_button_2.place(x=60, y=300)
                            stop_button_2 = tk.Button(controller, text="STOP CAM2", command=stop_recording2)
                            stop_button_2.place(x=160, y=300)
                            ####################    CAM2
                            Start_timing2 = tk.Label(controller, text="START TIME")
                            Start_timing2.place(x=60, y=330)
                            strt2 = tk.Label(controller, text="0:0")
                            strt2.place(x=210, y=330)
                            Duration_time2 = tk.Label(controller, text="DURATION")
                            Duration_time2.place(x=60, y=360)
                            drn2 = tk.Label(controller, text="0:0:0")
                            drn2.place(x=210, y=360)
                            NOD2 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD2.place(x=60, y=390)
                            num2 = tk.Label(controller, text="0")
                            num2.place(x=210, y=390)
                            ####################    CAM3
                            cam3 = tk.Label(controller, text="CAMERA 3", fg='violet')
                            cam3.place(x=20, y=420)
                            get_time3 = tk.Label(controller, text='Enter Time')
                            get_time3.place(x=60, y=450)
                            time3 = tk.Entry(controller)
                            time3.place(x=160, y=450)
                            start_button_3 = tk.Button(controller, text="START CAM3", command=start_recording3)
                            start_button_3.place(x=60, y=480)
                            stop_button_3 = tk.Button(controller, text="STOP CAM3", command=stop_recording3)
                            stop_button_3.place(x=160, y=480)
                            ####################    CAM3
                            Start_timing3 = tk.Label(controller, text="START TIME")
                            Start_timing3.place(x=60, y=510)
                            strt3 = tk.Label(controller, text="0:0")
                            strt3.place(x=210, y=510)
                            Duration_time3 = tk.Label(controller, text="DURATION")
                            Duration_time3.place(x=60, y=540)
                            drn3 = tk.Label(controller, text="0:0:0")
                            drn3.place(x=210, y=540)
                            NOD3 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD3.place(x=60, y=570)
                            num3 = tk.Label(controller, text="0")
                            num3.place(x=210, y=570)
                            ####################    CAM4
                            cam4 = tk.Label(controller, text="CAMERA 4", fg='skyblue')
                            cam4.place(x=320, y=60)
                            get_time4 = tk.Label(controller, text='Enter Time')
                            get_time4.place(x=360, y=90)
                            time4 = tk.Entry(controller)
                            time4.place(x=460, y=90)
                            start_button_4 = tk.Button(controller, text="START CAM4", command=start_recording4)
                            start_button_4.place(x=360, y=120)
                            stop_button_4 = tk.Button(controller, text="STOP CAM4", command=stop_recording4)
                            stop_button_4.place(x=460, y=120)
                            ####################    CAM4
                            Start_timing4 = tk.Label(controller, text="START TIME")
                            Start_timing4.place(x=360, y=150)
                            strt4 = tk.Label(controller, text="0:0")
                            strt4.place(x=510, y=150)
                            Duration_time4 = tk.Label(controller, text="DURATION")
                            Duration_time4.place(x=360, y=180)
                            drn4 = tk.Label(controller, text="0:0:0")
                            drn4.place(x=510, y=180)
                            NOD4 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD4.place(x=360, y=210)
                            num4 = tk.Label(controller, text="0")
                            num4.place(x=510, y=210)
                            ####################    CAM5
                            cam5 = tk.Label(controller, text="CAMERA 5", fg='black')
                            cam5.place(x=320, y=240)
                            get_time5 = tk.Label(controller, text='Enter Time')
                            get_time5.place(x=360, y=270)
                            time5 = tk.Entry(controller)
                            time5.place(x=460, y=270)
                            start_button_5 = tk.Button(controller, text="START CAM5", command=start_recording5)
                            start_button_5.place(x=360, y=300)
                            stop_button_5 = tk.Button(controller, text="STOP CAM5", command=stop_recording5)
                            stop_button_5.place(x=460, y=300)
                            ####################    CAM5
                            Start_timing5 = tk.Label(controller, text="START TIME")
                            Start_timing5.place(x=360, y=330)
                            strt5 = tk.Label(controller, text="0:0")
                            strt5.place(x=510, y=330)
                            Duration_time5 = tk.Label(controller, text="DURATION")
                            Duration_time5.place(x=360, y=360)
                            drn5 = tk.Label(controller, text="0:0:0")
                            drn5.place(x=510, y=360)
                            NOD5 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD5.place(x=360, y=390)
                            num5 = tk.Label(controller, text="0")
                            num5.place(x=510, y=390)
                            ####################    CAM6
                            cam6 = tk.Label(controller, text="CAMERA 6", fg='grey')
                            cam6.place(x=320, y=420)
                            get_time6 = tk.Label(controller, text='Enter Time')
                            get_time6.place(x=360, y=450)
                            time6 = tk.Entry(controller)
                            time6.place(x=460, y=450)
                            start_button_6 = tk.Button(controller, text="START CAM6", command=start_recording6)
                            start_button_6.place(x=360, y=480)
                            stop_button_6 = tk.Button(controller, text="STOP CAM6", command=stop_recording6)
                            stop_button_6.place(x=460, y=480)
                            ####################    CAM6
                            Start_timing6 = tk.Label(controller, text="START TIME")
                            Start_timing6.place(x=360, y=510)
                            strt6 = tk.Label(controller, text="0:0")
                            strt6.place(x=510, y=510)
                            Duration_time6 = tk.Label(controller, text="DURATION")
                            Duration_time6.place(x=360, y=540)
                            drn6 = tk.Label(controller, text="0:0:0")
                            drn6.place(x=510, y=540)
                            NOD6 = tk.Label(controller, text="NO OF CAPTURED DATA")
                            NOD6.place(x=360, y=570)
                            num6 = tk.Label(controller, text="0")
                            num6.place(x=510, y=570)
                            ######################  CLOSE
                            close_button = tk.Button(controller, text="CLOSE", command=close_window)
                            close_button.place(x=130, y=640)
                            process_frame()
                            controller.mainloop()
                            cap1.release()
                            cap2.release()
                            cap3.release()
                            cap4.release()
                            cap5.release()
                            cap6.release()
                            cv2.destroyAllWindows()

                    rec = tk.Button(main_frame, text="record", font=10, command=reco)
                    rec.place(x=400, y=250)

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

                        num = num + 1

                    output_frame.update_idletasks()
                    canvas.configure(scrollregion=canvas.bbox("all"))
                    canvas.bind_all("<MouseWheel>",
                                    lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

                def export_summary():
                    conn = sqlite3.connect('DATABASES/recording.db')
                    df = pd.read_sql_query("SELECT * from recordsummary", conn)
                    df.to_excel(f"./SUMMARY DATA EXCEL/{current_date}-RECORDING SUMMARY.xlsx", index=False)
                    conn.close()
                    print("Data exported to Excel successfully.")
                    messagebox.showinfo("Exported", "Overall data exported to Excel successfully.")

                def open_file_dialog():
                    file_path = filedialog.askopenfilename()
                    print("Selected file:", file_path)
                    return file_path

                def hide_indicators():
                    rec_indicator.config(bg='#c3c3c3')
                    summary_indicator.config(bg='#c3c3c3')
                    exp_rec_indicator.config(bg='#c3c3c3')

                def indicate(lb, page):
                    hide_indicators()
                    lb.config(bg='#158aff')
                    delete_pages()
                    page()

                def delete_pages():
                    for frame in main_frame.winfo_children():
                        frame.destroy()

                # OPTION FRAME

                options_frame = tk.Frame(w, bg="#c3c3c3", highlightbackground='black', highlightthickness=2)
                options_frame.pack(side=tk.LEFT)
                options_frame.pack_propagate(False)
                options_frame.configure(width=210, height=1500)

                # BUTTONS
                general = tk.Label(options_frame, text="WELCOME", font=10, bg="#c3c3c3")
                general.place(x=50, y=50)

                u_name = tk.Label(options_frame, text=f'{username}', font=10, bg="#c3c3c3")
                u_name.place(x=80, y=100)

                rec_btn = tk.Button(options_frame, text="RECORD", font=('Bold', 15), fg='white', bd=0, bg='#4392fa',
                                    width=15,
                                    borderwidth=5, command=lambda: indicate(rec_indicator, record))
                rec_btn.place(x=10, y=160)

                summary_btn = tk.Button(options_frame, text="DISPLAY \n SUMMARY", font=('Bold', 15), fg='white', bd=0,
                                        bg='#4392fa',
                                        width=15, borderwidth=5,
                                        command=lambda: indicate(summary_indicator, display_summary))
                summary_btn.place(x=10, y=250)

                exp_rec_summary_bt = tk.Button(options_frame, text="EXPORT REC\n SUMMARY", font=('Bold', 15),
                                               fg='white', bd=0,
                                               bg='#4392fa',
                                               width=15, borderwidth=5,
                                               command=lambda: indicate(exp_rec_indicator, export_summary))
                exp_rec_summary_bt.place(x=10, y=370)

                # INDICATORS

                rec_indicator = tk.Label(options_frame, text='', bg='#c3c3c3')
                rec_indicator.place(x=3, y=160, width=5, height=40)

                summary_indicator = tk.Label(options_frame, text='', bg='#c3c3c3')
                summary_indicator.place(x=3, y=250, width=5, height=60)

                exp_rec_indicator = tk.Label(options_frame, text='', bg='#c3c3c3')
                exp_rec_indicator.place(x=3, y=370, width=5, height=60)

                # MAIN FRAME

                main_frame = tk.Frame(w, highlightbackground='black', highlightthickness=2)
                main_frame.pack(side=tk.LEFT)
                main_frame.pack_propagate(False)
                main_frame.configure(height=1500, width=7100, bg='#2c2f33')

                w.mainloop()

            else:
                messagebox.showerror('Error', 'Invalid password')
        else:
            messagebox.showerror('Error', 'Invalid username')

    else:
        messagebox.showerror('Error', 'Enter all data')

frame1 = Frame(app, bg='#001220',  width=470, height=360)
frame1.place(x=0, y=0)

login_label2 = Label(frame1, font=font1, text='LOGIN', fg='#fff', bg='#001220')
login_label2.place(x=170, y=20)

username_entry2 = Entry(frame1, font=font2, bg='#fff')
username_entry2.place(x=110, y=80)

password_entry2 = Entry(frame1, font=font2, bg='#fff')
password_entry2.place(x=110, y=150)

login_button2 = Button(frame1, command=login_account, font=font2, fg='#fff',bg='#001220', text='LOGIN')
login_button2.place(x=190, y=220)

app.mainloop()
