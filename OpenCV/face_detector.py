import cv2 as cv

face_detect = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")

capture = cv.VideoCapture(0)

while True:
    isTrue, frame = capture.read()

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    faces = face_detect.detectMultiScale(gray, 1.1, 10)

    for x, y, w, h in faces:
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    cv.imshow("Face detector", frame)

    if cv.waitKey(20) & 0xFF == ord("q"):
        break
    if cv.getWindowProperty("Face detector", cv.WND_PROP_VISIBLE) == 0:
        break

capture.release()
cv.destroyAllWindows()
