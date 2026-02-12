import cv2
import numpy as np
import time
import os

# ===================== Sound =====================
try:
    import pygame
    pygame.mixer.init()
    def playsound(file):
        if os.path.exists(file):
            pygame.mixer.Sound(file).play()
except:
    def playsound(file): pass

from cvzone.HandTrackingModule import HandDetector

# ===================== Camera =====================
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.7, maxHands=1)

# ===================== Keyboard Layout =====================
keys = [
    ['Q','W','E','R','T','Y','U','I','O','P'],
    ['A','S','D','F','G','H','J','K','L'],
    ['Z','X','C','V','B','N','M','Space','Del'],
    ['Shift','Save']
]

# ===================== Neon Colors =====================
COLORS = {
    "normal": (20, 20, 20),
    "hover": (0, 255, 180),
    "click": (255, 0, 120),
    "text": (255, 255, 255),
    "background": (5, 5, 20),
    "border": (0, 255, 180),
    "caps_on": (255, 0, 120),
    "caps_off": (120, 120, 120)
}

# ===================== Layout =====================
BTN_W, BTN_H = 95, 95
MARGIN = 22
START_X, START_Y = 80, 180

# ===================== Variables =====================
text = ""
caps = True
last_click = 0
flash_time = 0
shockwave = None
finger_trail = []

words = ["HELLO", "GAMING", "NEON", "CYBER", "PYTHON", "PROJECT"]

# ===================== Helpers =====================
def pulse_value(speed=4, min_v=2, max_v=8):
    t = time.time()
    return int(min_v + (max_v - min_v) * (0.5 + 0.5 * np.sin(t * speed)))

def draw_glow_rect(img, x, y, w, h, color, thickness):
    for i in range(thickness):
        cv2.rectangle(img, (x-i, y-i), (x+w+i, y+h+i), color, 1)

def fit_text_to_width(text, max_width, font, scale, thickness):
    fitted = ""
    for ch in text[::-1]:
        test = ch + fitted
        (w, _), _ = cv2.getTextSize(test, font, scale, thickness)
        if w <= max_width:
            fitted = test
        else:
            break
    return fitted

def draw_wave_text(img, text, x, y, max_width,
                   font, scale, thickness,
                   color, amp=6, speed=6):
    offset_x = 0
    t = time.time()

    for i, ch in enumerate(text):
        (w, _), _ = cv2.getTextSize(ch, font, scale, thickness)
        if offset_x + w > max_width:
            break

        dy = int(np.sin(t * speed + i * 0.5) * amp)

        cv2.putText(img, ch,
                    (x + offset_x, y + dy),
                    font, scale, color, thickness)
        offset_x += w

# ===================== Keyboard =====================
def draw_keyboard(img, hover=None, click=None):
    overlay = img.copy()
    y = START_Y

    for row in keys:
        x = START_X
        for key in row:
            w = BTN_W*2 if key in ['Space','Save'] else BTN_W
            base = COLORS["normal"]

            if key == hover:
                pulse = pulse_value()
                draw_glow_rect(img, x, y, w, BTN_H, COLORS["hover"], pulse)

            if key == click:
                draw_glow_rect(img, x, y, w, BTN_H, COLORS["click"], 10)
                base = COLORS["click"]

            cv2.rectangle(overlay, (x, y), (x+w, y+BTN_H), base, cv2.FILLED)
            cv2.rectangle(overlay, (x, y), (x+w, y+BTN_H), COLORS["border"], 2)

            cv2.putText(overlay, key,
                        (x+18, y+58),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.3, COLORS["text"], 3)

            x += w + MARGIN
        y += BTN_H + MARGIN

    cv2.addWeighted(overlay, 0.4, img, 0.6, 0, img)

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

# ===================== Main Loop =====================
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Dark webcam
    img = cv2.addWeighted(img, 0.25, np.zeros_like(img), 0.75, 0)

    hands, img = detector.findHands(img)
    hover = click = None

    if hands:
        lm = hands[0]['lmList']
        index_tip = lm[8][:2]
        thumb_tip = lm[4][:2]

        dist = np.linalg.norm(np.array(index_tip) - np.array(thumb_tip))
        hover = get_key(index_tip)

        finger_trail.append(index_tip)
        if len(finger_trail) > 8:
            finger_trail.pop(0)

        for i, p in enumerate(finger_trail):
            alpha = int(255 * (i+1) / len(finger_trail))
            cv2.circle(img, p, 8, (0, alpha, 255), cv2.FILLED)

        if dist < 45 and time.time() - last_click > 0.6:
            click = hover
            if click:
                playsound("click.wav")

                if click == "Space": text += " "
                elif click == "Del": text = text[:-1]
                elif click == "Shift": caps = not caps
                elif click == "Save":
                    with open("typed_text.txt", "a") as f:
                        f.write(text + "\n")
                else:
                    text += click if caps else click.lower()

                last_click = time.time()
                flash_time = time.time()
                shockwave = {"pos": index_tip, "start": time.time()}

    # Shockwave
    if shockwave:
        dt = time.time() - shockwave["start"]
        r = int(dt * 300)
        if r < 120:
            cv2.circle(img, shockwave["pos"], r, COLORS["click"], 2)
        else:
            shockwave = None

    # Flash
    if time.time() - flash_time < 0.1:
        flash = img.copy()
        cv2.rectangle(flash, (0,0), (1280,720), (255,255,255), cv2.FILLED)
        cv2.addWeighted(flash, 0.08, img, 0.92, 0, img)

    # ===================== HUD =====================
    cv2.rectangle(img, (0,0), (1280,60), COLORS["background"], cv2.FILLED)
    cap_color = COLORS["caps_on"] if caps else COLORS["caps_off"]
    cv2.circle(img, (25,30), 12, cap_color, cv2.FILLED)

    cv2.putText(img, "NEON TYPE",
                (60,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2, COLORS["hover"], 3)

    # ===================== Text Area + Wave =====================
    cv2.rectangle(img, (0,60), (1280,135), COLORS["background"], cv2.FILLED)

    cursor = "|" if int(time.time()*2) % 2 == 0 else ""
    display = fit_text_to_width(text + cursor, 1180,
                                cv2.FONT_HERSHEY_SIMPLEX, 1.5, 2)

    draw_wave_text(img, display,
                   50, 115, 1180,
                   cv2.FONT_HERSHEY_SIMPLEX,
                   1.5, 2,
                   (255,255,255),
                   amp=7, speed=7)

    draw_keyboard(img, hover, click)
    cv2.imshow("NEON TYPE – Gaming UI", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()




