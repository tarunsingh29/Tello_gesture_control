import cv2
import mediapipe as mp
import time
from djitellopy import Tello

# -----------------------------
# CONNECT TO TELLO DRONE
# -----------------------------
tello = Tello()
tello.connect()
print("Battery:", tello.get_battery())

tello.streamon()
frame_read = tello.get_frame_read()

# -----------------------------
# MEDIAPIPE HAND SETUP
# -----------------------------

import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# -----------------------------
# COMMAND CONTROL SETTINGS
# -----------------------------
command_delay = 2
last_command_time = 0

# -----------------------------
# FINGER STATE FUNCTION
# -----------------------------
def get_finger_states(landmarks):

    fingers = []

    # Thumb
    if landmarks[4].x > landmarks[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Index
    if landmarks[8].y < landmarks[6].y:
        fingers.append(1)
    else:
        fingers.append(0)

    # Middle
    if landmarks[12].y < landmarks[10].y:
        fingers.append(1)
    else:
        fingers.append(0)

    # Ring
    if landmarks[16].y < landmarks[14].y:
        fingers.append(1)
    else:
        fingers.append(0)

    # Pinky
    if landmarks[20].y < landmarks[18].y:
        fingers.append(1)
    else:
        fingers.append(0)

    return fingers

# -----------------------------
# MAIN LOOP
# -----------------------------
while True:

    frame = frame_read.frame
    frame = cv2.resize(frame, (640,480))

    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    gesture = "None"

    if results.multi_hand_landmarks:

        for handLms in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                handLms,
                mp_hands.HAND_CONNECTIONS
            )

            lm = handLms.landmark
            fingers = get_finger_states(lm)

            # -------------------------
            # GESTURE LOGIC
            # -------------------------

            if fingers == [0,0,0,0,0]:
                gesture = "Forward"
                if time.time()-last_command_time > command_delay:
                    tello.move_forward(30)
                    last_command_time = time.time()

            elif fingers == [1,1,1,1,1]:
                gesture = "Back"
                if time.time()-last_command_time > command_delay:
                    tello.move_back(30)
                    last_command_time = time.time()

            elif fingers == [1,0,0,0,0]:
                if lm[4].x > lm[2].x:
                    gesture = "Right"
                    if time.time()-last_command_time > command_delay:
                        tello.move_right(30)
                        last_command_time = time.time()

                else:
                    gesture = "Left"
                    if time.time()-last_command_time > command_delay:
                        tello.move_left(30)
                        last_command_time = time.time()

            elif fingers[1] == 1 and fingers[0] == 1:

                if lm[8].y < lm[6].y:
                    gesture = "Up"
                    if time.time()-last_command_time > command_delay:
                        tello.move_up(30)
                        last_command_time = time.time()

                else:
                    gesture = "Down"
                    if time.time()-last_command_time > command_delay:
                        tello.move_down(30)
                        last_command_time = time.time()

    cv2.putText(frame, gesture,
                (30,80),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (0,255,0),
                3)

    cv2.imshow("Gesture Drone Control", frame)

    key = cv2.waitKey(1)

    # -----------------------------
    # KEYBOARD SAFETY CONTROLS
    # -----------------------------
    if key == ord('t'):
        tello.takeoff()

    if key == ord('l'):
        tello.land()

    if key == ord('q'):
        tello.land()
        break

# -----------------------------
# CLEANUP
# -----------------------------
tello.streamoff()
cv2.destroyAllWindows()