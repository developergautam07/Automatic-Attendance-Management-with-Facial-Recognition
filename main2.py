import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
from ttkthemes import ThemedStyle
import tkinter.simpledialog as tsd
import cv2
import os
import csv
import datetime
import concurrent.futures
import threading
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time

# FUNCTIONS


def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200, tick)


def contact():
    mess._show(title='Contact us',
               message="Please contact us on: '")


def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if not exists:
        mess._show(title='File Missing',
                   message='haarcascade_frontalface_default.xml is missing. Please contact us for help.')
        window.destroy()


def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel/psd.txt")
    if exists1:
        tf = open("TrainingImageLabel/psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found',
                                'Please enter a new password below', show='*')
        if new_pas is None:
            mess._show(title='No Password Entered',
                       message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel/psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered',
                       message='New password was registered successfully!!')
            return
    op = old.get()
    newp = new.get()
    nnewp = nnew.get()
    if op == key:
        if newp == nnewp:
            txf = open("TrainingImageLabel/psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password',
                   message='Please enter correct old password.')
        return
    mess._show(title='Password Changed',
               message='Password changed successfully!!')
    master.destroy()


def change_pass():
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False, False)
    master.title("Change Password")
    master.configure(background="white")
    lbl4 = tk.Label(master, text='    Enter Old Password',
                    bg='white', font=('times', 12, ' bold '))
    lbl4.place(x=10, y=10)
    global old
    old = tk.Entry(master, width=25, fg="black", relief='solid',
                   font=('times', 12, ' bold '), show='*')
    old.place(x=180, y=10)
    lbl5 = tk.Label(master, text='   Enter New Password',
                    bg='white', font=('times', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black", relief='solid',
                   font=('times', 12, ' bold '), show='*')
    new.place(x=180, y=45)
    lbl6 = tk.Label(master, text='Confirm New Password',
                    bg='white', font=('times', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid',
                    font=('times', 12, ' bold '), show='*')
    nnew.place(x=180, y=80)
    cancel = tk.Button(master, text="Cancel", command=master.destroy, fg="black", bg="red", height=1, width=25,
                       activebackground="white", font=('times', 10, ' bold '))
    cancel.place(x=200, y=120)
    save1 = tk.Button(master, text="Save", command=save_pass, fg="black", bg="#3ece48", height=1, width=25,
                      activebackground="white", font=('times', 10, ' bold '))
    save1.place(x=10, y=120)
    master.mainloop()


def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel/psd.txt")
    if exists1:
        tf = open("TrainingImageLabel/psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found',
                                'Please enter a new password below', show='*')
        if new_pas is None:
            mess._show(title='No Password Entered',
                       message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel/psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered',
                       message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if password == key:
        TrainImages()
    elif password is None:
        pass
    else:
        mess._show(title='Wrong Password',
                   message='You have entered the wrong password')


def clear():
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)


def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("StudentDetails/StudentDetails.csv")
    if exists:
        with open("StudentDetails/StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("StudentDetails/StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = txt.get()
    name = txt2.get()
    if name.isalpha() or (' ' in name):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum = sampleNum + 1
                cv2.imwrite("TrainingImage/" + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w])
                cv2.imshow('Taking Images', img)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Taken for ID: " + Id
        row = [serial, '', Id, '', name]
        with open('StudentDetails/StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        if not name.isalpha():
            res = "Enter Correct name"
            message.configure(text=res)


def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations',
                   message='Please Register someone first!!!')
        return
    recognizer.save("TrainingImageLabel/Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    message.configure(text='Total Registrations till now: ' + str(ID[0]))


def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids


def process_frame(frame, faceCascade, recognizer, df, attendance, present_ids, font):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.2, 5, minSize=(100, 100))
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (225, 0, 0), 2)
        serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
        
        if conf < 50:
            ts = time.time()
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
            ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
            ID = str(ID)
            ID = ID[1:-1]
            bb = str(aa)
            bb = bb[2:-2]
            
            if ID not in present_ids:
                attendance.append([str(ID), '', bb, '', str(date), '', str(timeStamp)])
                present_ids.add(ID)
        else:
            Id = 'Unknown'
            bb = str(Id)
        
        cv2.putText(frame, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
    
    return frame


def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    for k in tv.get_children():
        tv.delete(k)
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
    
    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Set buffer size to 1 frame
    cam.set(cv2.CAP_PROP_FPS, 10)  # Set FPS to 10
    
    df = pd.read_csv("StudentDetails/StudentDetails.csv")
    date = datetime.date.today()
    attendance = []
    present_ids = set()
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    while True:
        ret, frame = cam.read()
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(process_frame, frame, faceCascade, recognizer, df, attendance, present_ids, font)
            frame = future.result()
        
        cv2.imshow('Taking Attendance', frame)
        
        if cv2.waitKey(1) == 13:
            break
    
    cam.release()
    cv2.destroyAllWindows()
    
    for student in attendance:
        tv.insert("", "end", text=student[0], values=(student[0], student[2], date, student[5], student[6]))
        
    csv_file = f"Attendance/Attendance_{date}.csv"
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', '', 'NAME', '', 'DATE', '', 'TIME'])
        writer.writerows(attendance)
    
    mess._show(title='Attendance Successful', message=f'Attendance taken and saved for date: {date}')


# GUI SETUP

window = tk.Tk()
window.geometry("960x540")
window.title("Attendance System")
window.resizable(False, False)

style = ThemedStyle(window)
style.set_theme("arc")

tab_control = ttk.Notebook(window)

tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)

tab_control.add(tab1, text='For new registrations')
tab_control.add(tab2, text='For already registered')

lbl = tk.Label(tab1, text="Enter ID", width=20, height=2, fg="black", bg="#ccc", font=('times', 15, ' bold '))
lbl.place(x=80, y=30)

txt = tk.Entry(tab1, width=20, bg="white", fg="black", font=('times', 23, ' bold '))
txt.place(x=380, y=30)

lbl2 = tk.Label(tab1, text="Enter Name", width=20, height=2, fg="black", bg="#ccc", font=('times', 15, ' bold '))
lbl2.place(x=80, y=110)

txt2 = tk.Entry(tab1, width=20, bg="white", fg="black", font=('times', 23, ' bold '))
txt2.place(x=380, y=110)

clearButton = tk.Button(tab1, text="Clear", command=clear, fg="black", bg="red", width=10, height=1,
                        activebackground="white", font=('times', 15, ' bold '))
clearButton.place(x=700, y=30)

clearButton2 = tk.Button(tab1, text="Clear", command=clear2, fg="black", bg="red", width=10, height=1,
                         activebackground="white", font=('times', 15, ' bold '))
clearButton2.place(x=700, y=110)

takeImg = tk.Button(tab1, text="Take Images", command=TakeImages, fg="black", bg="#3ece48", width=20, height=3,
                    activebackground="white", font=('times', 15, ' bold '))
takeImg.place(x=90, y=200)

trackImg = tk.Button(tab1, text="Save Profile", command=TrainImages, fg="black", bg="#3ece48", width=20, height=3,
                     activebackground="white", font=('times', 15, ' bold '))
trackImg.place(x=390, y=200)

pswd = tk.Button(tab1, text="Change Password", command=change_pass, fg="black", bg="#3ece48", width=20, height=3,
                 activebackground="white", font=('times', 15, ' bold '))
pswd.place(x=690, y=200)

message = tk.Label(tab1, text="", bg="#ccc", fg="black", width=35, height=1, activebackground="white",
                   font=('times', 15, ' bold '))
message.place(x=70, y=380)

message1 = tk.Label(tab1, text="", bg="#ccc", fg="black", width=35, height=1, activebackground="white",
                    font=('times', 15, ' bold '))
message1.place(x=70, y=450)

# Tab 2

lbl3 = tk.Label(tab2, text="Attendance", width=20, height=2, fg="black", bg="#ccc", font=('times', 15, ' bold '))
lbl3.place(x=200, y=30)

lbl4 = tk.Label(tab2, text="Date: ", width=10, height=1, fg="black", bg="#ccc", font=('times', 12, ' bold '))
lbl4.place(x=30, y=100)

date = datetime.date.today()
date_label = tk.Label(tab2, text=str(date), width=12, height=1, fg="black", bg="#ccc", font=('times', 12, ' bold '))
date_label.place(x=110, y=100)

tv = ttk.Treeview(tab2, columns=(1, 2, 3, 4, 5), show="headings", height="15")
tv.place(x=30, y=150)
tv.heading(1, text="ID")
tv.heading(2, text="Name")
tv.heading(3, text="Date")
tv.heading(4, text="In-Time")
tv.heading(5, text="Out-Time")

scroll = ttk.Scrollbar(tab2, orient='vertical', command=tv.yview)
scroll.pack(side='right', fill='y')
tv.configure(yscrollcommand=scroll.set)

attendance_button = tk.Button(tab2, text="Take Attendance", command=TrackImages, fg="black", bg="#3ece48", width=20,
                              height=3, activebackground="white", font=('times', 15, ' bold '))
attendance_button.place(x=200, y=400)

# Add contact button
contact_button = tk.Button(tab2, text="Contact Us", command=contact, fg="black", bg="light blue", width=10, height=1,
                           activebackground="white", font=('times', 12, ' bold '))
contact_button.place(x=810, y=500)

# Clock widget
clock = tk.Label(tab2, font=('times', 15, 'bold'))
clock.place(x=800, y=50)
tick()

tab_control.pack(expand=1, fill='both')

window.mainloop()
