

import cv2
import mediapipe as mp
import time
import numpy as np
from djitellopy import Tello

# ============================================================
# CONFIGURATION
# ============================================================

FRAME_WIDTH = 640
FRAME_HEIGHT = 480

COMMAND_DISTANCE = 30      # movement distance (cm)
COMMAND_DELAY = 2          # seconds between commands

# ============================================================
# TELLO DRONE CLASS
# ============================================================


class DroneController:

    def __init__(self):

        self.tello = Tello()
        self.tello.connect()

        battery = self.tello.get_battery()
        print(f"Drone Connected | Battery: {battery}%")

        self.tello.streamon()
        self.frame_reader = self.tello.get_frame_read()

        self.last_command_time = 0


    def get_frame(self):
        frame = self.frame_reader.frame
        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
        return frame


    def send_command(self, command):

        if time.time() - self.last_command_time < COMMAND_DELAY:
            return

        try:
            if command == "forward":
                self.tello.move_forward(COMMAND_DISTANCE)

            elif command == "back":
                self.tello.move_back(COMMAND_DISTANCE)

            elif command == "left":
                self.tello.move_left(COMMAND_DISTANCE)

            elif command == "right":
                self.tello.move_right(COMMAND_DISTANCE)

            elif command == "up":
                self.tello.move_up(COMMAND_DISTANCE)

            elif command == "down":
                self.tello.move_down(COMMAND_DISTANCE)

            self.last_command_time = time.time()
            print("Command Sent:", command)

        except Exception as e:
            print("Command Error:", e)


    def takeoff(self):
        self.tello.takeoff()

    def land(self):
        self.tello.land()

    def shutdown(self):
        self.tello.streamoff()


# ============================================================
# HAND TRACKING MODULE
# ============================================================

class HandTracker:

    def __init__(self):

        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.drawer = mp.solutions.drawing_utils


    def detect(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        landmarks = None

        if results.multi_hand_landmarks:

            for handLms in results.multi_hand_landmarks:

                self.drawer.draw_landmarks(
                    frame,
                    handLms,
                    self.mp_hands.HAND_CONNECTIONS
                )

                landmarks = handLms.landmark

        return frame, landmarks


# ============================================================
# GESTURE CLASSIFIER
# ============================================================

class GestureClassifier:

    def __init__(self):
        pass


    def finger_states(self, lm):

        fingers = []

        # Thumb
        fingers.append(1 if lm[4].x > lm[3].x else 0)

        # Index
        fingers.append(1 if lm[8].y < lm[6].y else 0)

        # Middle
        fingers.append(1 if lm[12].y < lm[10].y else 0)

        # Ring
        fingers.append(1 if lm[16].y < lm[14].y else 0)

        # Pinky
        fingers.append(1 if lm[20].y < lm[18].y else 0)

        return fingers


    def classify(self, lm):

        fingers = self.finger_states(lm)

        # -------------------------------------------------
        # Gesture Rules
        # -------------------------------------------------

        if fingers == [0,0,0,0,0]:
            return "forward"

        if fingers == [1,1,1,1,1]:
            return "back"

        if fingers == [1,0,0,0,0]:

            if lm[4].x > lm[2].x:
                return "right"
            else:
                return "left"

        if fingers[1] == 1 and fingers[0] == 1:

            if lm[8].y < lm[6].y:
                return "up"
            else:
                return "down"

        return None


# ============================================================
# DISPLAY UTILITIES
# ============================================================

class Display:

    @staticmethod
    def draw_text(frame, text):

        cv2.putText(
            frame,
            text,
            (30,70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.8,
            (0,255,0),
            3
        )

# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    print("\nStarting Gesture Drone System...\n")

    drone = DroneController()
    tracker = HandTracker()
    classifier = GestureClassifier()

    gesture = "None"

    drone_flying = False

    while True:

        frame = drone.get_frame()

        frame, landmarks = tracker.detect(frame)

        gesture = "None"

        # ------------------------------------------------
        # GESTURE CONTROL ONLY AFTER TAKEOFF
        # ------------------------------------------------
        if drone_flying and landmarks:

            gesture = classifier.classify(landmarks)

            if gesture:
                drone.send_command(gesture)

        Display.draw_text(frame, str(gesture))

        cv2.imshow("Gesture Drone Control", frame)

        key = cv2.waitKey(1) & 0xFF

        # -----------------------------
        # TAKEOFF
        # -----------------------------
        if key == ord('t'):
            print("Takeoff")
            drone.takeoff()
            drone_flying = True

        # -----------------------------
        # LAND
        # -----------------------------
        elif key == ord('l'):
            print("Landing")
            drone.land()

        # -----------------------------
        # EXIT
        # -----------------------------
        elif key == ord('q'):
            if drone_flying:
                drone.land()
            break

    drone.shutdown()
    cv2.destroyAllWindows()


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()