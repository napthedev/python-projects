import cv2
import mediapipe as mp
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

capture = cv2.VideoCapture(0)

mp_hand = mp.solutions.hands
hands = mp_hand.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume_min, volume_max = volume.GetVolumeRange()[0], volume.GetVolumeRange()[1]
volume_distance = volume_max - volume_min
volume.SetMute(0, None)

percent = 0

while True:
    success, img = capture.read()
    if not success:
        continue

    RGB_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(RGB_image).multi_hand_landmarks

    if result:
        hand_landmark = result[0]
        mp_draw.draw_landmarks(img, hand_landmark, mp_hand.HAND_CONNECTIONS)
        x_0 = round(hand_landmark.landmark[0].x * img.shape[1])
        y_0 = round(hand_landmark.landmark[0].y * img.shape[0])
        x_4 = round(hand_landmark.landmark[4].x * img.shape[1])
        y_4 = round(hand_landmark.landmark[4].y * img.shape[0])
        x_8 = round(hand_landmark.landmark[8].x * img.shape[1])
        y_8 = round(hand_landmark.landmark[8].y * img.shape[0])
        cv2.line(img, (x_4, y_4), (x_8, y_8), (255, 0, 0), 5)
        cv2.circle(img, (x_4, y_4), 10, (0, 0, 255), -1)
        cv2.circle(img, (x_8, y_8), 10, (0, 0, 255), -1)
        cv2.circle(img, (round((x_4 + x_8) / 2), round((y_4 + y_8) / 2)), 10, (0, 0, 255), -1)

        max_distanse = round(math.hypot(x_0 - x_8, y_0 - y_8))
        current_distanse = round(math.hypot(x_4 - x_8, y_4 - y_8))
        percent = current_distanse / max_distanse
        if (percent > 1):
            percent = 1
        volume.SetMasterVolumeLevel(round(volume_min + percent * volume_distance), None)

    cv2.rectangle(img, (0, 0), (20, img.shape[0]), (0, 255, 0), 1)
    cv2.rectangle(img, (0, round((1 - percent) * img.shape[1])), (20, img.shape[0]), (0, 255, 0), -1)

    cv2.imshow("Camera", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

capture.release()
