import cv2
import mediapipe as mp

capture = cv2.VideoCapture(0)

mp_hand = mp.solutions.hands
hands = mp_hand.Hands()
mp_draw = mp.solutions.drawing_utils

while True:
    success, img = capture.read()
    if not success:
        continue

    RGB_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(RGB_image).multi_hand_landmarks

    if result:
        for hand_landmark in result:
            mp_draw.draw_landmarks(img, hand_landmark, mp_hand.HAND_CONNECTIONS)

    cv2.imshow("Camera", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

capture.release()
