# AI Virtual Keyboard

A **hand gesture-based virtual keyboard** using Python, OpenCV, and MediaPipe. Type text in real-time using hand movements and finger gestures.

---

## Features

- Detects a single hand and tracks finger tips.
- Virtual keyboard interaction:
- Click keys by bringing index finger and thumb together.
- Support for letters, Space, Delete, Shift, and Save keys.
- Word prediction for faster typing.
- Save typed text to a file.
- Visual feedback with hover and click effects.
- Sound effects for key clicks.

---


## Usage

- Hover your index finger over a key to highlight it.
- Bring thumb and index finger together to select a key.
- Shift toggles capitalization.
- Save writes the current text to typed_text.txt.


---

## Requirements

- Python 3.8+
- OpenCV
- NumPy
- MediaPipe
- Playsound

Install dependencies via pip:

```bash
pip install opencv-python numpy mediapipe playsound


## How to Run

```bash
python virtual_keyboard.py


