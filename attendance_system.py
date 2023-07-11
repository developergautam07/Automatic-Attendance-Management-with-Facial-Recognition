import face_recognition
import cv2
import numpy as np
import csv
import os
from datetime import datetime
import tkinter as tk
from PIL import Image, ImageTk

video_capture = cv2.VideoCapture(0)
 
gautam_image = face_recognition.load_image_file("img/photo.jpg")
gautam_encoding = face_recognition.face_encodings(gautam_image)[0]

ratan_tata_image = face_recognition.load_image_file("img/tata.jpeg")
ratan_tata_encoding = face_recognition.face_encodings(ratan_tata_image)[0]

sadmona_image = face_recognition.load_image_file("img/mona.jpeg")
sadmona_encoding = face_recognition.face_encodings(sadmona_image)[0]

tesla_image = face_recognition.load_image_file("img/tesla.jpeg")
tesla_encoding = face_recognition.face_encodings(tesla_image)[0]
 
known_face_encoding = [
gautam_encoding,
ratan_tata_encoding,
sadmona_encoding,
tesla_encoding
]

known_faces_names = [
"gautam",
"ratan tata",
"mona",
"nikola tesla"
]
 
students = known_faces_names.copy()
 
face_locations = []
face_encodings = []
face_names = [] 
 
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
 
f = open(current_date+'.csv','w+',newline = '')
lnwriter = csv.writer(f)

# Create a tkinter window
window = tk.Tk()
window.title("Face Recognition Attendance System")

# Create a label to display the video feed
video_label = tk.Label(window)
video_label.pack()

# Create a text widget to display the attendance information
attendance_text = tk.Text(window, height=10, width=30)
attendance_text.pack()

# Create a variable to control whether the face recognition attendance system is running
running = False

# Function to update the video feed and attendance information
def update():
    # Capture a frame from the video
    _, frame = video_capture.read()
    
    # Process the frame if the face recognition attendance system is running
    if running:
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
            name = ""
            face_distance = face_recognition.face_distance(known_face_encoding, face_encoding)
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                name = known_faces_names[best_match_index]
            face_names.append(name)
            if name in known_faces_names:
                font = cv2.FONT_HERSHEY_SIMPLEX
                bottomLeftCornerOfText = (10, 100)
                fontScale = 1.5
                fontColor = (255, 0, 0)
                thickness = 3
                lineType = 2
                cv2.putText(frame, name + ' Present',
                            bottomLeftCornerOfText,
                            font,
                            fontScale,
                            fontColor,
                            thickness,
                            lineType)
                if name in students:
                    students.remove(name)
                    current_time = now.strftime("%H:%M:%S")
                    lnwriter.writerow([name, current_time])
                    # Update the attendance information in the text widget
                    attendance_text.insert(tk.END, f"{name} - {current_time}\n")
    
    # Convert the frame to an image and resize it
    image = Image.fromarray(frame)
    image = image.resize((640, 480), Image.LANCZOS)
    
    # Convert the image to a PhotoImage and display it in the label
    photo = ImageTk.PhotoImage(image)
    video_label.config(image=photo)
    video_label.image = photo
    
    # Call this function again after 15 milliseconds
    window.after(15, update)

# Function to start the face recognition attendance system when the button is clicked
def start():
    global running
    running = True

# Create a button to start the face recognition attendance system
start_button = tk.Button(window, text="Take Attendance", command=start)
start_button.pack()

# Start updating the video feed and attendance information
update()

# Run the tkinter main loop
window.mainloop()
