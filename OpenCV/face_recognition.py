import cv2 as cv
import numpy as np
import os

face_detect = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")
face_recognizer = cv.face.LBPHFaceRecognizer_create()


def train_recognizer():
    features = []
    labels = []
    for person in people:
        person_path = os.path.join(DIR, person)
        label = people.index(person)

        for img in os.listdir(person_path):
            img_path = os.path.join(person_path, img)
            img_array = cv.imread(img_path)
            gray = cv.cvtColor(img_array, cv.COLOR_BGR2GRAY)

            faces_rect = face_detect.detectMultiScale(gray, 1.1, 4)

            for (x, y, w, h) in faces_rect:
                faces_roi = gray[y:y + h, x:x + w]
                features.append(faces_roi)
                labels.append(label)

    features = np.array(features, dtype="object")
    labels = np.array(labels)

    face_recognizer.train(features, labels)

    face_recognizer.save("Face_data/face_trained.yml")

    if not os.path.exists(os.path.join(os.getcwd(), "Face_data")):
        os.mkdir(os.path.join(os.getcwd(), "Face_data"))

    np.save("Face_data/labels.npy", labels)


DIR = os.path.join(os.getcwd(), "Faces")
people = []
for i in os.listdir("Faces"):
    people.append(i)

print("Checking faces data...")
img_dir = []
for person in people:
    person_path = os.path.join(DIR, person)
    person_dir = []
    for img in os.listdir(person_path):
        img_path = os.path.join(person_path, img)
        person_dir.append(img_path)
    img_dir.append(person_dir)
img_dir = np.array(img_dir, dtype="object")
if not os.path.exists(os.path.join(os.getcwd(), "Face_data")):
    os.mkdir(os.path.join(os.getcwd(), "Face_data"))

if os.path.exists("Face_data/img_dir.npy"):
    if np.array_equal(np.load("Face_data/img_dir.npy", allow_pickle=True), img_dir):
        print("Face data already analized...")
    else:
        np.save("Face_data/img_dir.npy", img_dir)
        print("Analizing faces...")
        train_recognizer()
else:
    np.save("Face_data/img_dir.npy", img_dir)
    print("Analizing faces...")
    train_recognizer()


labels = np.load("Face_data/labels.npy", allow_pickle=True)

face_recognizer.read("Face_data/face_trained.yml")

print("Openning webcam...")
camera_capture = cv.VideoCapture(0)

close_count = 0
while True:
    camera_isTrue, camera_frame = camera_capture.read()
    gray = cv.cvtColor(camera_frame, cv.COLOR_BGR2GRAY)
    face_rect = face_detect.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in face_rect:
        face_roi = gray[y:y + h, x:x + w]

        label, confidence = face_recognizer.predict(face_roi)
        cv.putText(camera_frame, f"{people[label]}: {round(confidence * 10) / 10}%", (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv.rectangle(camera_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if cv.waitKey(50) & 0xFF == ord("q"):
        break
    if cv.getWindowProperty("Camera", cv.WND_PROP_VISIBLE) == 0:
        close_count += 1
        if close_count > 1:
            break

    cv.imshow("Camera", camera_frame)

camera_capture.release()
cv.destroyAllWindows()
