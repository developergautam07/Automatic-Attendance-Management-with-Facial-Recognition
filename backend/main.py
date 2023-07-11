from flask import Flask, jsonify
from flask_cors import CORS
import cv2
from PIL import Image
from io import BytesIO
import base64
import face_recognition
import numpy as np
import csv
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Your face recognition attendance system code goes here

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
s=True

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open(current_date+'.csv','w+',newline = '')
lnwriter = csv.writer(f)

@app.route('/start')
def start():
    # Start the face recognition attendance system
    # ...
    return 'OK'

@app.route('/update')
def update():
    # Capture a frame from the video
    _, frame = video_capture.read()

    # Process the frame using your face recognition code
    small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
    rgb_small_frame = small_frame[:,:,::-1]
    if s:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encoding,face_encoding)
            name=""
            face_distance = face_recognition.face_distance(known_face_encoding,face_encoding)
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                name = known_faces_names[best_match_index]

            face_names.append(name)
            if name in known_faces_names:
                font = cv2.FONT_HERSHEY_SIMPLEX
                bottomLeftCornerOfText = (10,100)
                fontScale              = 1.5
                fontColor              = (255,0,0)
                thickness              = 3
                lineType               = 2

                cv2.putText(frame,name+' Present', 
                    bottomLeftCornerOfText, 
                    font, 
                    fontScale,
                    fontColor,
                    thickness,
                    lineType)

                if name in students:
                    students.remove(name)
                    print(students)
                    current_time = now.strftime("%H-%M-%S")
                    lnwriter.writerow([name,current_time])
    
    # Encode the frame as a JPEG image and convert it to a base64 string
    image = Image.fromarray(frame)
    buffer = BytesIO()
    image.save(buffer, format='JPEG')
    video_src = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    # Get the current attendance information
    attendance=[]
    
    # Return the video frame and attendance information as JSON data
    return jsonify({
        'video_src': f'data:image/jpeg;base64,{video_src}',
        'attendance': attendance,
    })

if __name__ == '__main__':
    app.run()
