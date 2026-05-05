from djitellopy import Tello
import cv2
import mediapipe as mp


try:
    tello = Tello()
    tello.connect()
    print(f"Battery: {tello.get_battery()}%")
    tello.takeoff()
    # tello.move_up(30)
    tello.move_forward(5)
    # tello.rotate_clockwise(90)
    # tello.rotate_counter_clockwise(90)
    # tello.move_forward(50)
    tello.land()
except Exception as e:
    print(f"Error: {e}")
finally:
    try:
        tello.end()
    except:
        pass






