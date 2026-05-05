# 🚁 Tello Gesture Control System

A real-time, vision-based control system for the DJI Tello drone that enables touch-free piloting using hand gestures.  
Built using MediaPipe, TensorFlow, and OpenCV, the system focuses on low-latency inference, control stability, and safety.

---

## 🎯 Key Highlights

- **Real-Time Gesture Control**  
  Hand gestures are processed and mapped to drone commands with minimal delay.

- **Dual Control System**  
  Seamless switching between manual keyboard input and gesture-based control during flight.

- **Safety-First Design**
  - Command buffering to prevent jitter  
  - Neutral gesture triggers hover state  
  - Emergency keyboard override  

- **Live Telemetry HUD**  
  Displays battery status, connection health, and active command state.

---

## 🧠 System Architecture
Camera Input → MediaPipe (Hand Tracking) → Feature Extraction →
TensorFlow Lite Model → Gesture Classification →
Command Mapping → Tello API → Drone Movement


---

## ⚙️ Pipeline Breakdown

- **Hand Detection**  
  MediaPipe extracts 21 keypoints per frame.

- **Feature Engineering**  
  Keypoints are normalized and converted into relative coordinate vectors.

- **Gesture Classification**  
  A lightweight TensorFlow Lite (`.tflite`) model predicts gesture classes.

- **Command Execution**  
  Commands are sent via `djitellopy` to control the drone.

---

## ⚙️ Performance Considerations

- Optimized for real-time CPU inference  
- Temporal smoothing reduces false positives  
- Gesture buffering prevents rapid oscillations  
- Handles unstable Wi-Fi latency from Tello stream  

---

## 🎮 Controls

### Keyboard Mode

| Key | Action |
|-----|--------|
| w / s | Forward / Back |
| a / d | Left / Right |
| r / f | Up / Down |
| q / e | Rotate |
| Space | Takeoff / Land |
| Esc | Exit and Land |

---

### Gesture Mode

- Press `g` to activate  
- Perform predefined gestures (UP, DOWN, LEFT, RIGHT, etc.)  
- Extendable via custom training  

---

## 🤖 Custom Gesture Training

1. Run `main.py`  
2. Press `n` to enable logging mode  
3. Capture gesture samples using keys `0–9`  
4. Data is saved to:  
   `model/keypoint_classifier/keypoint.csv`  
5. Open `Keypoint_model_training.ipynb`  
6. Train and export new `.tflite` model  

---

## ⚠️ Challenges & Limitations

- Sensitive to lighting conditions  
- Gesture misclassification under occlusion  
- Network latency affects responsiveness  
- Limited gesture vocabulary (depends on training data)  

---

## 🚀 Future Improvements

- Add temporal models (LSTM / Transformer)  
- Improve gesture confidence thresholding  
- Multi-hand gesture support  
- Edge deployment on embedded devices  

---

## 🛠 Tech Stack

- Python  
- MediaPipe  
- TensorFlow / TensorFlow Lite  
- OpenCV  
- djitellopy  

---

## 🔌 Setup

1. Turn on the Tello drone  
2. Connect to Wi-Fi (`TELLO-XXXXXX`)  

### Install Dependencies

pip install -r requirements.txt


### Test Connection:

python3 tests/connection_test.py


### ▶️ Run the Project:

python3 main.py

