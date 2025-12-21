import cv2
import numpy as np
import time
from playsound import playsound
from mediapipe.python.solutions.hands import Hands, HAND_CONNECTIONS
from mediapipe.python.solutions.drawing_utils import draw_landmarks

# ===================== Camera =====================
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# ===================== MediaPipe =====================
hands = Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# ===================== Keyboard Layout =====================
keys = [
    ['Q','W','E','R','T','Y','U','I','O','P'],
    ['A','S','D','F','G','H','J','K','L'],
    ['Z','X','C','V','B','N','M','Space','Del'],
    ['Shift','Save']
]

# ===================== UI Settings =====================
BTN_W, BTN_H = 80, 80
MARGIN = 10
START_X, START_Y = 50, 150

COLORS = {
    "normal": (200, 200, 200),
    "hover": (0, 255, 0),
    "click": (0, 0, 255),
    "text": (0, 0, 0)
}

# ===================== Variables =====================
text = ""
caps = True
last_click = 0

words = ["HELLO", "HI", "HOW", "HOUSE", "HAPPY", "PYTHON", "PROJECT"]

# ===================== Functions =====================
def draw_keyboard(img, hover=None, click=None):
    overlay = img.copy()
    alpha = 0.5  

    y = START_Y
    for row in keys:
        x = START_X
        for key in row:
            w = BTN_W*2 if key in ['Space','Save'] else BTN_W
            color = COLORS["normal"]
            if key == hover: color = COLORS["hover"]
            if key == click: color = COLORS["click"]

            cv2.rectangle(overlay, (x, y), (x+w, y+BTN_H), color, cv2.FILLED)
            cv2.rectangle(overlay, (x, y), (x+w, y+BTN_H), (0,0,0), 2)
            cv2.putText(overlay, key, (x+10, y+50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, COLORS["text"], 2)
            x += w + MARGIN
        y += BTN_H + MARGIN

    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

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

def predict_word(txt):
    for w in words:
        if w.startswith(txt.upper()):
            return w
    return ""

# ===================== Main Loop =====================
while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    hover = click = None

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            draw_landmarks(img, hand, HAND_CONNECTIONS)

            lm = []
            h,w,_ = img.shape
            for id,l in enumerate(hand.landmark):
                lm.append((int(l.x*w), int(l.y*h)))

            index_tip = lm[8]
            thumb_tip = lm[4]

            dist = np.linalg.norm(np.array(index_tip)-np.array(thumb_tip))
            hover = get_key(index_tip)

            if dist < 45 and time.time()-last_click > 0.6:
                click = hover
                if click:
                    playsound("click.wav", block=False)

                    if click == "Space":
                        text += " "
                    elif click == "Del":
                        text = text[:-1]
                    elif click == "Shift":
                        caps = not caps
                    elif click == "Save":
                        with open("typed_text.txt","w") as f:
                            f.write(text)
                    else:
                        text += click if caps else click.lower()

                    last_click = time.time()

    # ===================== UI =====================
    cv2.rectangle(img,(0,0),(1280,120),(50,50,50),cv2.FILLED)
    cv2.putText(img,"TEXT: "+text,(50,80),
                cv2.FONT_HERSHEY_SIMPLEX,1.5,(255,255,255),2)

    prediction = predict_word(text.split(" ")[-1])
    if prediction:
        cv2.putText(img,"Suggestion: "+prediction,(50,120),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2)

    draw_keyboard(img, hover, click)
    cv2.imshow("AI Virtual Keyboard", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



