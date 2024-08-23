import cv2
from landmarker import FaceDetector
import streamlit as st

cap = cv2.VideoCapture(0)
pose_detector = FaceDetector()
run = st.toggle("RUN")

IMAGE = st.empty()
while run:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pose_detector.detect(frame)
    result = pose_detector.result
    answer = ""
    try:
        landmarks = result.face_landmarks[0]
        ydiff = landmarks[468].y - landmarks[473].y
        ythresh = 0.07
        if abs(ydiff) >= ythresh:
            answer = "left" if ydiff > 0 else "right"
    except:
        pass
    
    cv2.putText(frame, answer, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 2)
    IMAGE.image(frame)

if not run:
    cap.release()