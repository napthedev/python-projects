import cv2
import mediapipe as mp

capture = cv2.VideoCapture(0)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils


while True:
    success, img = capture.read()
    if not success:
        continue

    RGB_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    result = pose.process(RGB_image).pose_landmarks

    if result:
        mp_draw.draw_landmarks(img, result, mp_pose.POSE_CONNECTIONS)

    cv2.imshow("Camera", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

capture.release()
