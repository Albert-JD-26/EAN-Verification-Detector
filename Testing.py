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
from tkcalendar import DateEntry

current_time = datetime.now().time()
present_date = datetime.now().strftime("%d-%m-%Y")

current_date = datetime.now().strftime("%d-%m-%Y")
starting_time = current_time.strftime("%I-%M %p")


try:
    if not os.path.exists('DATABASES'):
        os.makedirs('DATABASES')
except OSError:
    print('Error: Creating directory of DATABASES')

current_date = datetime.now().strftime("%d-%m-%Y")


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

if not os.path.exists('DATABASES/recording.db'):
    conn.execute('''CREATE TABLE record1data(
                    DETETCTED_DATA TEXT NOT NULL, 
                    DETECTED_TIME TIMESTAMP NOT NULL, 
                    VIDEO_NAME TEXT NOT NULL, 
                    DATE DATE NOT NULL, 
                    TIME TIMESTAMP NOT NULL, 
                    USER_NAME NOT NULL);''')

def check_company_name_not_null():
    connection = sqlite3.connect('EAN.db')
    check = connection.cursor()
    check.execute("SELECT * FROM details WHERE company_name IS NOT NULL")
    result = check.fetchall()
    connection.close()
    return len(result) > 0

cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
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

def record():

    camera_list = [f'Camera {i}' for i in range(10) if cv2.VideoCapture(i).read()[0]]
    print(f'Detected cameras: {", ".join(camera_list)}')
    Number_of_camera = len(camera_list)
    print("Total number of cameras:", Number_of_camera)

    def scan1(data1, elapsed_time_str1, present_date, present_time, video_name1, username_entry2):
        rec_d1 = sqlite3.connect('./DATABASES/recording.db')
        rec_d1.execute(
            "INSERT INTO record1data (DETETCTED_DATA, DETECTED_TIME, DATE ,TIME , VIDEO_NAME, USER_NAME) VALUES (?,?,?,?,?,?)",
            (data1, elapsed_time_str1, present_date, present_time, video_name1, username_entry2))
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
            dispatch1(video_name1, elapsed_time_str1, len(qr_codes_array1), present_date, present_time, username_entry2)
            rec1_data = sqlite3.connect('recording.db')
            df = pd.read_sql_query(
                f"SELECT * from cam1data WHERE VIDEO_NAME = '{video_name1}'", rec1_data)
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

    def close_window():
        cap1.release()
        cap2.release()
        cap3.release()
        cap4.release()
        cap5.release()
        cap6.release()
        cv2.destroyAllWindows()
        controller.destroy()

    # Detect the number of camera connected to system #
    if Number_of_camera == 1:
        print("One camera is connected to system")

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

            rec_btn = tk.Button(options_frame, text="RECORD", font=('Bold', 15), fg='white', bd=0, bg='#4392fa', width=15, borderwidth=5, command=record)
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


