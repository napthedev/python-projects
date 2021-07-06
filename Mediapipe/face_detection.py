import cv2
import mediapipe as mp

capture = cv2.VideoCapture(0)

mp_face_detection = mp.solutions.face_detection
mp_draw = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection()

while True:
    success, img = capture.read()

    if not success:
        continue

    RGB_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    result = face_detection.process(img).detections

    if result:
        for face in result:
            mp_draw.draw_detection(img, face)
            cv2.putText(img, str(round(face.score[0] * 1000) / 10) + "%", (
                round(face.location_data.relative_bounding_box.xmin * img.shape[1]),
                round(face.location_data.relative_bounding_box.ymin * img.shape[0] - 5),
            ), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Camera", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

capture.release()
