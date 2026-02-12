import streamlit as st
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import time
import math

# ================= Streamlit Page =================
st.set_page_config(layout="wide")
st.title("🎮 Neon Type Virtual Keyboard Demo (Cloud-Friendly)")

# ================= Sound (Cloud-Safe) =================
def playsound(file):
    pass  # معلق مؤقتًا عشان Streamlit Cloud

# ================= Camera =================
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
detector = HandDetector(detectionCon=0.7, maxHands=1)

# ================= Variables =================
keys = [
    ['Q','W','E','R','T','Y','U','I','O','P'],
    ['A','S','D','F','G','H','J','K','L'],
    ['Z','X','C','V','B','N','M','Space','Del'],
    ['Shift','Save']
]

text = ""
caps = True
last_click = 0
shockwave = None
finger_trail = []

BTN_W, BTN_H, MARGIN = 95, 95, 22
START_X, START_Y = 80, 180

stframe = st.empty()
st.sidebar.header("Typed Text")
text_box = st.sidebar.empty()

# ================= Helpers =================
def get_key(pos):
    y = START_Y
    for row in keys:
        x = START_X
        for key in row:
            w = BTN_W*2 if key in ['Space','Save'] else BTN_W
            if x < pos[0] < x+w and y < pos[1] < y+BTN_H:
                return key
            x += w + MARGIN
        y += BTN_H + MARGIN
    return None

def pulse_value(speed=4, min_v=2, max_v=8):
    t = time.time()
    return int(min_v + (max_v-min_v)*(0.5 + 0.5*math.sin(t*speed)))

def draw_wave_text(img, text, x, y, font, scale, thickness, color, amp=6, speed=6):
    t = time.time()
    offset_x = 0
    for i, ch in enumerate(text):
        (w,_), _ = cv2.getTextSize(ch, font, scale, thickness)
        dy = int(np.sin(t*speed + i*0.5)*amp)
        cv2.putText(img, ch, (x+offset_x, y+dy), font, scale, color, thickness)
        offset_x += w

# ================= Main Loop =================
while True:
    ret, img = cap.read()
    if not ret:
        st.warning("Camera not detected!")
        break

    img = cv2.flip(img, 1)
    img = cv2.addWeighted(img, 0.2, np.zeros_like(img), 0.8, 0)  # Dark effect

    hands, img = detector.findHands(img)

    hover_key = None
    click_key = None

    if hands:
        lm = hands[0]['lmList']
        index_tip = lm[8][:2]
        thumb_tip = lm[4][:2]
        dist = np.linalg.norm(np.array(index_tip)-np.array(thumb_tip))
        hover_key = get_key(index_tip)

        finger_trail.append(tuple(index_tip))
        if len(finger_trail) > 8:
            finger_trail.pop(0)

        if dist < 45 and time.time() - last_click > 0.6:
            click_key = hover_key
            if click_key:
                playsound("click.wav")
                if click_key == "Space": 
                    text += " "
                elif click_key == "Del": 
                    text = text[:-1]
                elif click_key == "Shift": 
                    caps = not caps
                elif click_key == "Save":
                    # زر تحميل النص
                    st.sidebar.download_button(
                        label="Download Text",
                        data=text,
                        file_name="typed_text.txt",
                        mime="text/plain"
                    )
                else: 
                    text += click_key if caps else click_key.lower()
                shockwave = {"pos": tuple(index_tip), "start": time.time()}
            last_click = time.time()

    # Finger trail
    for i, p in enumerate(finger_trail):
        alpha = int(255*(i+1)/len(finger_trail))
        cv2.circle(img, p, 8, (0, alpha, 255), cv2.FILLED)

    # Shockwave
    if shockwave:
        dt = time.time() - shockwave["start"]
        r = int(dt*300)
        if r < 120:
            cv2.circle(img, shockwave["pos"], r, (255,0,120), 2)
        else:
            shockwave = None

    # Draw keyboard
    overlay = img.copy()
    y = START_Y
    for row in keys:
        x = START_X
        for key in row:
            w = BTN_W*2 if key in ['Space','Save'] else BTN_W
            color = (20,20,20)
            if key == hover_key:
                pulse = pulse_value()
                for i in range(pulse):
                    cv2.rectangle(img,(x-i,y-i),(x+w+i,y+BTN_H+i),(0,255,180),1)
                color = (0,255,180)
            cv2.rectangle(overlay,(x,y),(x+w,y+BTN_H),color,-1)
            cv2.rectangle(overlay,(x,y),(x+w,y+BTN_H),(0,255,180),2)
            cv2.putText(overlay,key,(x+20,y+60),cv2.FONT_HERSHEY_SIMPLEX,1.2,(255,255,255),2)
            x += w + MARGIN
        y += BTN_H + MARGIN
    img = cv2.addWeighted(overlay, 0.6, img, 0.4, 0)

    # Wave text
    draw_wave_text(img, text, 50, 100, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 2, (0,255,255), amp=7, speed=7)

    # ================= Update Sidebar =================
    text_box.markdown(
        f"<div style='background-color:black; padding:10px; color:white; height:400px; overflow:auto;'>{text}</div>", 
        unsafe_allow_html=True
    )

    stframe.image(img, channels="BGR")

    # Reduce CPU load
    time.sleep(0.03)


