🚁 Tello Gesture Control System

A real-time, vision-based control system for the DJI Tello drone that enables touch-free piloting using hand gestures.
Built using MediaPipe, TensorFlow, and OpenCV, the system focuses on low-latency inference, control stability, and safety.

🎯 Key Highlights
Real-Time Gesture Control
Hand gestures are processed and mapped to drone commands with minimal delay.
Dual Control System
Seamless switching between manual keyboard input and gesture-based control during flight.
Safety-First Design
Command buffering to prevent jitter
Neutral gesture triggers hover state
Emergency keyboard override
Live Telemetry HUD
Displays battery status, connection health, and active command state.
🧠 System Architecture

Camera Input → MediaPipe (Hand Tracking) → Feature Extraction → TensorFlow Lite Model → Gesture Classification → Command Mapping → Tello API → Drone Movement

⚙️ Pipeline Breakdown
Hand Detection:
MediaPipe extracts 21 keypoints per frame.
Feature Engineering:
Keypoints are normalized and converted into relative coordinate vectors.
Gesture Classification:
A lightweight TensorFlow Lite (.tflite) model predicts gesture classes.
Command Execution:
Commands are sent via djitellopy to control the drone.
⚙️ Performance Considerations
Optimized for real-time CPU inference
Temporal smoothing reduces false positives
Gesture buffering prevents rapid oscillations
Handles unstable Wi-Fi latency from Tello stream
🎮 Controls
Keyboard Mode
Key	Action
w / s	Forward / Back
a / d	Left / Right
r / f	Up / Down
q / e	Rotate
Space	Takeoff / Land
Esc	Exit and Land
Gesture Mode
Switch using g
Perform predefined gestures (UP, DOWN, LEFT, RIGHT, etc.)
Easily extendable via custom training
🤖 Custom Gesture Training
Run main.py
Press n to enable logging mode
Capture gesture samples using keys (0–9)
Data is saved to:
model/keypoint_classifier/keypoint.csv
Open Keypoint_model_training.ipynb
Train and export new .tflite model
⚠️ Challenges & Limitations
Sensitive to lighting conditions
Gesture misclassification under occlusion
Network latency affects responsiveness
Limited gesture vocabulary (depends on training data)
🚀 Future Improvements
Add temporal models (LSTM / Transformer)
Improve gesture confidence thresholding
Multi-hand gesture support
Edge deployment on embedded devices
🛠 Tech Stack
Python
MediaPipe
TensorFlow / TensorFlow Lite
OpenCV
djitellopy
🔌 Setup
Turn on the Tello drone
Connect to Wi-Fi (TELLO-XXXXXX)
Install dependencies:
pip install -r requirements.txt
Test connection:
python3 tests/connection_test.py

(Expected output: ok)

▶️ Run the Project
python3 main.py