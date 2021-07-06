import cv2
import mediapipe as mp

capture = cv2.VideoCapture(0)

mp_face_mesh = mp.solutions.face_mesh
mp_draw = mp.solutions.drawing_utils
face_mesh = mp_face_mesh.FaceMesh()

while True:
    success, img = capture.read()

    if not success:
        continue

    RGB_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    result = face_mesh.process(RGB_image).multi_face_landmarks

    if result:
        for face in result:
            mp_draw.draw_landmarks(img, face, mp_face_mesh.FACE_CONNECTIONS, mp_draw.DrawingSpec(thickness=1, circle_radius=1), mp_draw.DrawingSpec(thickness=1, circle_radius=1))

    cv2.imshow("Camera", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

capture.release()
