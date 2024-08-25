import cv2
import streamlit as st
from time import time, sleep
from math import inf
from landmarker import FaceLandmarkDetector
from game_utils import Player, NUM_QUESTIONS, DELAY, TIME_LIMIT
from styles import CSS

THRESH = 0.055  # head tilt threshold

cap = cv2.VideoCapture(0)
face_detector = FaceLandmarkDetector()

st.markdown(CSS, unsafe_allow_html=True)  # custom css
# sidebar
st.logo("hho_logo.png")
st.sidebar.markdown(
"""
<h1 style="text-align:center;">HHO Presents</h1>
<h1 style="text-align:center;color:gold;font-family:'Prata';">VASISTA 2K24</h1>
""", unsafe_allow_html=True)
st.sidebar.image("krishna.gif")
st.sidebar.markdown("""
<p>You will be shown two math expressions.<br>
You must choose the one which has greater value by tilting your head to the left or right.<br>
If you tilt correctly, you will score a point.<br>
GOOD LUCK!</p>
""", unsafe_allow_html=True)

# run = st.toggle("RUN")
col1, col2, col3 = st.columns(3)
with col1:
    score_container = st.empty()
with col2:
    timer_container = st.empty()
with col3:
    qno_container = st.empty()
    
st.divider()
    
col1, col2 = st.columns(2)
with col1:
    left_question_container = st.empty()
with col2:
    right_question_container = st.empty()
image_container = st.empty()
again_btn = st.empty()

run = image_container.button("PLAY!")

# 3 2 1 timer
if run:
    image_container.markdown("<h1 style='text-align:center'>3</h1>", unsafe_allow_html=True)
    sleep(1)
    image_container.markdown("<h1 style='text-align:center'>2</h1>", unsafe_allow_html=True)
    sleep(1)
    image_container.markdown("<h1 style='text-align:center'>1</h1>", unsafe_allow_html=True)
    sleep(1)
    image_container.empty()

player = Player()
qidx = 0
head_position = "center"
answered_time = float('inf')
end_time = time() + TIME_LIMIT
lexp = player.expressions[qidx].left  # left expression text
rexp = player.expressions[qidx].right  # right expression text

while run:
    secs_left = int(end_time - time())
    if secs_left <= 0:
        timer_container.subheader(":red[Time's Up!]")
        image_container.empty()
        break
    timer_container.header(secs_left)  # timer
    qno_container.subheader(f"Q: {qidx + 1} / {NUM_QUESTIONS}") # question number
    
    if time() - answered_time > DELAY: # show next question after delay
        qidx += 1
        if qidx == NUM_QUESTIONS:
            break
        lexp = player.expressions[qidx].left
        rexp = player.expressions[qidx].right
        answered_time = float('inf')
        
    left_question_container.title(lexp)
    right_question_container.title(rexp)
    
    # reading frames
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # getting landmarks
    face_detector.detect(frame)
    result = face_detector.result
    
    # Tilt detection
    try:
        assert answered_time == inf
        next_head_position = "center"
        landmarks = result.face_landmarks[0]
        ydiff = landmarks[468].y - landmarks[473].y
        ythresh = THRESH
        #check if head is tilted
        if abs(ydiff) >= ythresh:
            next_head_position = "left" if ydiff > 0 else "right"
    except:
        pass
    
    # check answer only if previous head position is center
    if answered_time == inf and next_head_position != 'center' and head_position == "center":
        rexp = round(player.expressions[qidx].right_val, 2)
        lexp = round(player.expressions[qidx].left_val, 2)
        if next_head_position == player.expressions[qidx].answer: # right answer
            if next_head_position == "right":
                rexp = f":green[{rexp}]"
            else:
                lexp = f":green[{lexp}]"
            player.score += 1
        else:
            if next_head_position == "right":
                rexp = f":red[{rexp}]"
            else:
                lexp = f":red[{lexp}]"
        answered_time = time()
    
    # cv2.putText(frame, answer_status, (10, 70), cv2.FONT_HERSHEY_TRIPLEX, 3, (255, 0, 0), 2)
    head_position = next_head_position    
    image_container.image(frame, width=590)
    score_container.subheader(f"Score: :blue[{player.score}]")

cap.release()
left_question_container.empty()
right_question_container.empty()
if run:
    if player.score == 0:
        image_container.header("Better luck next time")
    elif player.score == NUM_QUESTIONS:
        image_container.header("Well Played !")
    else:
        image_container.empty()
    again_btn.button("RESTART")
if player.score == NUM_QUESTIONS:
    st.balloons()