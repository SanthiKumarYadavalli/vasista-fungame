import cv2
import streamlit as st
from time import time
from math import inf
from landmarker import FaceLandmarkDetector
from game_utils import Player, NUM_QUESTIONS, DELAY


cap = cv2.VideoCapture(0)
face_detector = FaceLandmarkDetector()

run = st.toggle("RUN")
col1, col2 = st.columns([0.7, 0.3])
with col1:
    score_container = st.empty()
with col2:
    question_status = st.empty()
col1, col2 = st.columns(2)
with col1:
    left_question_container = st.empty()
with col2:
    right_question_container = st.empty()
image_container = st.empty()
again_btn = st.empty()

player = Player("Player")
qidx = 0
head_position = "center"
answered_time = float('inf')
lq = player.expressions[qidx].left
rq = player.expressions[qidx].right

while run:
    question_status.subheader(f"Q: {qidx + 1} / {NUM_QUESTIONS}")
    if time() - answered_time > DELAY:
        qidx += 1
        if qidx == NUM_QUESTIONS:
            break
        lq = player.expressions[qidx].left
        rq = player.expressions[qidx].right
        answered_time = float('inf')
        
    left_question_container.header(lq)
    right_question_container.header(rq)
    
    # reading frames
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # getting landmarks
    face_detector.detect(frame)
    result = face_detector.result
    
    # Tilt detection
    next_head_position = "center"
    try:
        assert answered_time == inf
        landmarks = result.face_landmarks[0]
        ydiff = landmarks[468].y - landmarks[473].y
        ythresh = 0.07
        #check if head is tilted
        if abs(ydiff) >= ythresh:
            next_head_position = "left" if ydiff > 0 else "right"
    except:
        pass
    
    # check answer only if previous head position is center
    if answered_time == inf and next_head_position != 'center' and head_position == "center":
        rq = round(player.expressions[qidx].right_val, 2)
        lq = round(player.expressions[qidx].left_val, 2)
        if next_head_position == player.expressions[qidx].answer: # right answer
            if next_head_position == "right":
                rq = f":green[{rq}]"
            else:
                lq = f":green[{lq}]"
            player.score += 1
        else:
            if next_head_position == "right":
                rq = f":red[{rq}]"
            else:
                lq = f":red[{lq}]"
        answered_time = time()
    
    # cv2.putText(frame, answer_status, (10, 70), cv2.FONT_HERSHEY_TRIPLEX, 3, (255, 0, 0), 2)
    head_position = next_head_position    
    image_container.image(frame, width=590)
    score_container.subheader(f"Score: :blue[{player.score}]")

cap.release()
left_question_container.empty()
right_question_container.empty()
image_container.empty()
if player.score == NUM_QUESTIONS:
    st.balloons()
again_btn.button("AGAIN!")