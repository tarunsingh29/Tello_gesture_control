from djitellopy import Tello
import cv2
import mediapipe as mp

# -----------------------------
# CONNECT TO DRONE
# -----------------------------
tello = Tello()
tello.connect()

print("Battery:", tello.get_battery())

tello.streamon()
frame_read = tello.get_frame_read()

# -----------------------------
# MEDIAPIPE SETUP
# -----------------------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# -----------------------------
# FINGER STATE FUNCTION
# -----------------------------
def get_finger_states(lm):

    fingers = []

    # thumb
    if lm[4].x > lm[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # index
    if lm[8].y < lm[6].y:
        fingers.append(1)
    else:
        fingers.append(0)

    # middle
    if lm[12].y < lm[10].y:
        fingers.append(1)
    else:
        fingers.append(0)

    # ring
    if lm[16].y < lm[14].y:
        fingers.append(1)
    else:
        fingers.append(0)

    # pinky
    if lm[20].y < lm[18].y:
        fingers.append(1)
    else:
        fingers.append(0)

    return fingers

# -----------------------------
# MAIN LOOP
# -----------------------------
while True:

    frame = frame_read.frame
    frame = cv2.resize(frame,(640,480))

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

            # -----------------------------
            # GESTURE LOGIC
            # -----------------------------

            # fist
            if fingers == [0,0,0,0,0]:
                gesture = "Forward"

            # open palm
            elif fingers == [1,1,1,1,1]:
                gesture = "Backward"

            # thumb direction
            elif fingers == [1,0,0,0,0]:

                thumb_dx = lm[4].x - lm[2].x

                if thumb_dx > 0.05:
                    gesture = "Right"

                elif thumb_dx < -0.05:
                    gesture = "Left"

            # index + thumb
            elif fingers[0] == 1 and fingers[1] == 1:

                if lm[8].y < lm[6].y:
                    gesture = "Up"

                else:
                    gesture = "Down"

    # -----------------------------
    # DISPLAY GESTURE
    # -----------------------------
    cv2.putText(
        frame,
        gesture,
        (30,80),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (0,255,0),
        3
    )

    cv2.imshow("Drone Gesture Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# -----------------------------
# CLEANUP
# -----------------------------
tello.streamoff()
cv2.destroyAllWindows()