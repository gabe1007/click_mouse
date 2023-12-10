import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)

# Mediapipe functions for hand detection and drawing
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

# Code to give a little bit of color
green_color = (0, 255, 0)  # green em BGR
landmark_drawing_spec = mp.solutions.drawing_utils.DrawingSpec(color=green_color, thickness=1, circle_radius=3)

# get the size of the screen
screen_width, screen_height = pyautogui.size()

# define the variables that will be used to make detections
thumb_y = 0
thumb_x = 0

while True:

    # Processing part
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Flip the screen in th y axis so that the finger moves to the right direction
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks  # Get the hand landmarks

    # If our image detects a hand
    if hands:
        for hand in hands:
            # Draw the landmarks o the frame
            drawing_utils.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS,
                                         landmark_drawing_spec, landmark_drawing_spec)
            # Get the hand landmarks
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                # Get the position of the landmark on the screen
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                # 4 = thumb landmark
                if id == 4:
                    # Draw a circle around the thumb landmark
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    # Adjust the reach of the detection, by doing this the mouse will move through the whole screen
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y

                # 8 = index landmark
                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y
                    print('outside', abs(thumb_y - index_y))

                    # If the difference between the y position of both fingers is less than 40 we have a click
                    if abs(thumb_y - index_y) < 40:
                        pyautogui.click()
                        pyautogui.sleep(1)

                    # If the difference between the y position of both fingers is less than 100 the mouse moves
                    elif abs(thumb_y - index_y) < 100:
                        pyautogui.moveTo(thumb_x, thumb_y)

    cv2.imshow('Virtual Mouse', frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
