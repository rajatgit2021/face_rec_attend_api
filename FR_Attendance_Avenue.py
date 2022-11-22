from html.entities import name2codepoint
import cv2
import numpy as np
import face_recognition
import sqlite3
import requests
import json
import os
from datetime import datetime


path = 'Face_Recognition_Attendance_1/images'
images = []
personName =[]
myList = os.listdir(path)
print(myList)

for cu_img in myList:
    curr_img = cv2.imread(f'{path}/{cu_img}')
    images.append(curr_img)
    personName.append(os.path.splitext(cu_img)[0])
print(personName)

def faceEncoding(images):
    encodeList =[]
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

#print(faceEncoding(images)) #HOG Algorithm used for finding encoding - 128 points to find uniqueness

encodingListKnown = faceEncoding(images)
print("All Encoding completed!!!")

conn = sqlite3.connect("sqlite.db")
print("DB Connection established here")
cursor = conn.cursor()
print("Connected to SQLite")

api_url = "https://Avenue.reliancegeneral.co.in/vmsintegration/Attendance"
headers =  {"Ocp-Apim-Subscription-Key" : "e8f1d1a426954e8da25ab71f6f8813c9"}

def attendance(emp_code):
    qry = f"SELECT * FROM emp_attendance where emp_id = '{emp_code}'"
    print("qry :: "+qry)
    cursor.execute(qry)
    records = cursor.fetchall()
    print("Total rows are:  ", len(records))
    print("Printing each row")
    time_now = datetime.now()
    tStr = time_now.strftime('%H:%M:%S')
    dStr = time_now.strftime('%d/%m/%Y')
    
    if len(records) == 0:
        print("No record with the emp id: "+emp_code)
        requestbody = {"Employee_Code": emp_code,"Login_Date": dStr,"In_Time": tStr,"Log_Flag": "Entry"}
        response = requests.post(api_url, data=json.dumps(requestbody), headers=headers)
        response.json()
        response.status_code

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    #print(ret)
    faces = cv2.resize(frame, (0,0), None, 0.25, 0.25)
    faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)
    
    facesCurrentFrame = face_recognition.face_locations(faces)
    encodeCurrentFrame = face_recognition.face_encodings(faces,facesCurrentFrame)

    for encodeFace, faceLoc in zip(encodeCurrentFrame, facesCurrentFrame):
        matches = face_recognition.compare_faces(encodingListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodingListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            emp_code = personName[matchIndex].upper()
            #print(name)
            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
            cv2.rectangle(frame, (x1, y2-35), (x2,y2), (0,255,0), cv2.FILLED)
            cv2.putText(frame, emp_code, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
            attendance(emp_code)
        
    cv2.imshow("Camera", frame)
    if cv2.waitKey(10) == 13:
        break
    
cap.release()
cv2.destroyAllWindows()