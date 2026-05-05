import cv2
import mediapipe as mp
import math

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

class GestureClassifier:
    """
    Analyzes spatial relationships between hand landmarks to classify gestures.
    Calculates 2D distances between points to ensure somewhat rotation-invariant detection.
    """
    def __init__(self):
        # We define relevant landmarks based on the MediaPipe documentation
        self.WRIST = 0
        self.THUMB_IP = 3
        self.THUMB_TIP = 4
        self.INDEX_PIP = 6
        self.INDEX_TIP = 8
        self.MIDDLE_PIP = 10
        self.MIDDLE_TIP = 12
        self.RING_PIP = 14
        self.RING_TIP = 16
        self.PINKY_PIP = 18
        self.PINKY_TIP = 20
        self.PINKY_MCP = 17

    def get_distance(self, p1, p2):
        """Euclidean distance calculation between two normalized landmarks"""
        return math.hypot(p1.x - p2.x, p1.y - p2.y)

    def classify_gesture(self, landmarks):
        """
        Takes a list of 21 hand landmarks and classifies the gesture.
        Returns string identifier of the gesture.
        """
        if not landmarks or len(landmarks) < 21:
            return "UNKNOWN"

        # Finger Extension Logic: 
        # For fingers (index, middle, ring, pinky), they are extended if the tip is further 
        # from the wrist than the PIP joint (middle knuckle).
        
        thumb_ext = self.get_distance(landmarks[self.THUMB_TIP], landmarks[self.PINKY_MCP]) > \
                    self.get_distance(landmarks[self.THUMB_IP], landmarks[self.PINKY_MCP])

        index_ext = self.get_distance(landmarks[self.INDEX_TIP], landmarks[self.WRIST]) > \
                    self.get_distance(landmarks[self.INDEX_PIP], landmarks[self.WRIST])

        middle_ext = self.get_distance(landmarks[self.MIDDLE_TIP], landmarks[self.WRIST]) > \
                     self.get_distance(landmarks[self.MIDDLE_PIP], landmarks[self.WRIST])

        ring_ext = self.get_distance(landmarks[self.RING_TIP], landmarks[self.WRIST]) > \
                   self.get_distance(landmarks[self.RING_PIP], landmarks[self.WRIST])

        pinky_ext = self.get_distance(landmarks[self.PINKY_TIP], landmarks[self.WRIST]) > \
                    self.get_distance(landmarks[self.PINKY_PIP], landmarks[self.WRIST])

        extensions = [thumb_ext, index_ext, middle_ext, ring_ext, pinky_ext]
        ext_count = sum(extensions)
        
        # Gesture 1: Open Palm
        if ext_count >= 4: # Allow 1 finger to be slightly misdetected for stability
            return "OPEN_PALM"
            
        # Gesture 2: Closed Fist
        if ext_count == 0:
            return "CLOSED_FIST"
            
        # Thumb pointing (Gesture 3 & 4)
        if extensions == [True, False, False, False, False] or extensions == [True, True, False, False, False]:
            # Wait, if index and thumb are extended, it could be L-shape.
            # We differentiate based on whether Index is extended, but let's strictly check [True, False, False, False, False]
            if extensions == [True, False, False, False, False]:
                # Is thumb pointing left or right?
                # Because the captured frame is flipped via cv2.flip(1), left on screen = left pointing.
                # Smaller X is left side of the screen.
                if landmarks[self.THUMB_TIP].x > landmarks[self.WRIST].x:
                    return "THUMB_RIGHT"
                else:
                    return "THUMB_LEFT"
                
        # L-Shape (Gesture 5 & 6)
        if extensions == [True, True, False, False, False]:
            # Are they pointing up or down?
            # Check if index tip is higher (smaller Y) or lower (larger Y) than the wrist
            if landmarks[self.INDEX_TIP].y < landmarks[self.WRIST].y:
                return "L_SHAPE_UP"
            else:
                return "L_SHAPE_DOWN"
                
        return "UNKNOWN"

classifier = GestureClassifier()

# WEBCAM
cap = cv2.VideoCapture(0)

while True:

    success, frame = cap.read()

    frame = cv2.flip(frame,1)

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

            gesture_code = classifier.classify_gesture(lm)
            
            # Map to display strings
            if gesture_code == "OPEN_PALM":
                gesture = "Backward (Open Palm)"
            elif gesture_code == "CLOSED_FIST":
                gesture = "Forward (Fist)"
            elif gesture_code == "THUMB_RIGHT":
                gesture = "Right"
            elif gesture_code == "THUMB_LEFT":
                gesture = "Left"
            elif gesture_code == "L_SHAPE_UP":
                gesture = "Up"
            elif gesture_code == "L_SHAPE_DOWN":
                gesture = "Down"
            else:
                gesture = "None"

    cv2.putText(
        frame,
        gesture,
        (30,80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.5,
        (0,255,0),
        3
    )

    cv2.imshow("Gesture Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()