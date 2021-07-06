import cv2
import mediapipe as mp
import numpy as np

mp_selfie_segmentation = mp.solutions.selfie_segmentation
selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation()

capture = cv2.VideoCapture(0)
bg_img = None
while True:
    success, img = capture.read()
    if not success:
        continue

    RGB_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = selfie_segmentation.process(RGB_image)

    condition = np.stack(
        (results.segmentation_mask,) * 3, axis=-1) > 0.1

    if bg_img is None:
        bg_img = np.zeros(img.shape, dtype=np.uint8)
        bg_img[:] = (192, 192, 192)
    output_img = np.where(condition, img, bg_img)

    cv2.imshow("Camera", output_img)
    if cv2.waitKey(1) & 0xFF == 27:
        break
capture.release()
