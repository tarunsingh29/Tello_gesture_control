```markdown
# 🚁 Tello Gesture Control

Control your DJI Tello drone in real-time using hand gestures captured via your computer's webcam or the drone's video stream. This project combines computer vision (MediaPipe), machine learning, and Tello's Python API to provide a seamless, touch-free piloting experience.

## 🚀 Features

* **Dual Control Modes:** Switch between Keyboard and Gesture controls mid-flight.
* **Real-time Gesture Recognition:** Uses Google's MediaPipe framework for fast and accurate hand landmark detection.
* **Flight Telemetry Display:** A Heads-Up Display (HUD) showing battery level, drone connection, and active commands.
* **Safety Features:** Includes hover states and buffering to prevent accidental maneuvers.

## 🛠 Prerequisites & Requirements

Make sure you are using Python 3.7 or higher.

### Dependencies

Install the required Python packages using:

```bash
pip install -r requirements.txt
```

> **Note:** Primary packages used include `djitellopy`, `mediapipe`, `tensorflow`, and `opencv-python`.

## 🔌 Setup & Connection

1. Turn on the Tello drone.
2. Connect your computer to the Tello's Wi-Fi network (e.g., `TELLO-XXXXXX`).
3. Verify connectivity by running the connection test:

```bash
python3 tests/connection_test.py
```

*Expect the response `b'ok'` for commands and the video stream.*

## 🎮 Usage

Run the main script to start the control window:

```bash
python3 main.py
```

### Keyboard Controls

Once the program is running, press the following keys for actions:

* **k** — Toggle Keyboard controls mode
* **g** — Toggle Gesture controls mode
* **Space** — Take off (if landed) or Land (if in flight)
* **w / s** — Move forward / Move back
* **a / d** — Move left / Move right
* **r / f** — Move up / Move down
* **e / q** — Rotate clockwise / Rotate counter-clockwise
* **Esc** — End program and safely land the drone

### Gesture Controls

Press **g** to switch to gesture mode. Point your hand to the camera based on your trained gestures (e.g., UP pose, LEFT, RIGHT).

## 🤖 Model Training (Adding Custom Gestures)

If you want to add or train your own gestures:

1. Launch the logger by running `main.py` and pressing "n" to log key points.
2. Assign a class ID (keys 0–9) to capture points, which updates `model/keypoint_classifier/keypoint.csv`.
3. Retrain the model by opening `Keypoint_model_training.ipynb` in Jupyter Notebook or Google Colab, updating the class count, and running all cells. Export the new `.tflite` model.

## 🤝 Contributing

Contributions are welcome! If you find any bugs or want to introduce new features, please fork the repository and submit a pull request.
```