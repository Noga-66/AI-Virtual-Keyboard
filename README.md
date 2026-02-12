#🎮 NEON TYPE

Gesture-Controlled Virtual Keyboard using Computer Vision

A real-time, interactive virtual keyboard powered by hand tracking and gesture recognition.
Designed with a futuristic neon gaming UI and immersive visual feedback effects.
_______________________________________________________________________________________________


#📌 Overview

Neon Type is a real-time virtual keyboard that allows users to type using hand gestures captured through a webcam.

The system detects the user's hand, tracks key landmarks, and triggers key presses using a pinch gesture (index finger + thumb).
The project focuses on:

Real-time computer vision

Gesture-based interaction

Interactive UI design

Visual feedback effects

Human-computer interaction (HCI)

This project demonstrates applied AI in user interface control without physical input devices.
_________________________________________________________________________________________________________________

#✨ Key Features

🖐 Hand Tracking

Real-time hand detection using MediaPipe (via CVZone)

Tracks 21 hand landmarks

Single-hand optimized for performance

👆 Gesture-Based Click Detection

Pinch detection based on Euclidean distance between:

Index fingertip

Thumb fingertip

Debounce logic to prevent multiple unintended clicks

🎮 Futuristic Neon UI

Custom-drawn virtual keyboard

Dynamic hover glow effect

Animated click feedback

Neon-themed visual system

🌊 Animated Wave Text Rendering

Sine-wave motion applied per character

Real-time animated text display

Smooth and dynamic typing experience

💥 Shockwave Click Effect

Expanding circular animation on click

Time-based radius growth

✨ Finger Trail Effect

Motion trail visualization

Alpha-blended fading effect

🔊 Audio Feedback

Click sound integration via pygame

🔠 Functional Keys

Shift / Caps toggle

Delete

Space

Save typed text to file
__________________________________________________________________________________________________________


#🧠 Technical Architecture

1️⃣ Input Layer

Webcam stream via OpenCV

Frame flipping for mirror interaction

Frame darkening for UI contrast

2️⃣ Detection Layer

HandDetector from CVZone

Landmark extraction

Distance computation using NumPy

3️⃣ Interaction Logic

Hover detection using bounding box hit-testing

Click detection via distance threshold

Debounce timing system

4️⃣ Rendering Engine

Custom UI drawing using OpenCV primitives:

Rectangles

Circles

Alpha blending

Animated text rendering using sine functions

Overlay-based glow system
_________________________________________________________________________________________________________________________________
#🛠 Tech Stack

Technology	Purpose
Python	Core language
OpenCV	Image processing & rendering
CVZone	Simplified hand tracking
MediaPipe	Hand landmark model
NumPy	Mathematical operations
Pygame	Audio feedback
⚙️ Installation
git clone https://github.com/your-username/Neon-Type-Virtual-Keyboard.git
cd Neon-Type-Virtual-Keyboard
pip install -r requirements.txt
python neon_type.py
______________________________________________________________________________________________________________________________
📂 Project Structure

Neon-Type-Virtual-Keyboard/
│
├── neon_type.py
├── click.wav
├── requirements.txt
├── README.md
└── assets/
    └── demo.gif
___________________________________________________________________________________________________________________________
#🎯 How It Works

Webcam captures frame
HandDetector extracts landmarks
Index & thumb distance is calculated
If distance < threshold → click event triggered
Corresponding key is appended to text buffer
Visual & audio feedback executed
______________________________________________________________________________________________________________________________
#📊 Performance Considerations

Optimized for 720p resolution
Single-hand detection for efficiency
Time-based debounce for input stability
Lightweight UI rendering (no external GUI frameworks)
______________________________________________________________________________________________________________________________
#🚀 Future Improvements

🔤 AI-powered word prediction (language model integration)

🌍 Multi-language support (including Arabic)

🎤 Text-to-Speech output

🧠 Custom-trained gesture classifier

🖥 Fullscreen immersive mode

🎨 Theme switching system

📱 Port to touchless kiosk systems
________________________________________________________________________________________________________________________________
#🎥 Demo

<img width="1876" height="1025" alt="Screenshot 2025-12-22 000028" src="https://github.com/user-attachments/assets/9bfcb4c0-d4fc-4b8c-b60a-5bbd7af1644e" />

__________________________________________________________________________________________________________________________________
#💡 Use Cases

Touchless interfaces

Accessibility systems

Smart kiosks

Interactive installations

AI + HCI academic demonstrations
_______________________________________________________________________________________________________________________________
#👩🏻‍💻 Author

Nada Hossam
AI & Computer Vision Engineer

Passionate about building intelligent real-time interactive systems that merge AI with creative user experience.





