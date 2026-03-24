import cv2
import numpy as np
from scipy.spatial import distance as dist
import pygame

# ----------------- ALARM -----------------
pygame.mixer.init()
pygame.mixer.music.load("alarm.wav")

# ----------------- EAR FUNCTION -----------------
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Eye landmark indexes (68 landmark model)
LEFT_EYE = list(range(36, 42))
RIGHT_EYE = list(range(42, 48))

# ----------------- FACE + LANDMARK MODEL -----------------
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

facemark = cv2.face.createFacemarkLBF()
facemark.loadModel("lbfmodel.yaml")

# ----------------- CAMERA -----------------
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

EAR_THRESHOLD = 0.22
EAR_CONSEC_FRAMES = 17

counter = 0
alarm_on = False

# ----------------- LOOP -----------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)

        _, landmarks = facemark.fit(gray, np.array([[(x,y,w,h)]]))

        if len(landmarks) > 0:
            shape = landmarks[0][0]

            # extract eye coordinates
            leftEye = shape[36:42]
            rightEye = shape[42:48]

            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

            ear = (leftEAR + rightEAR) / 2.0

            # draw eye points
            for (ex,ey) in np.concatenate((leftEye,rightEye),axis=0):
                cv2.circle(frame,(int(ex),int(ey)),2,(0,255,0),-1)

            cv2.putText(frame, f"EAR: {ear:.2f}", (20,40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

            # --------- DROWSINESS DETECTION ----------
            if ear < EAR_THRESHOLD:
                counter += 1
                cv2.putText(frame, f"Counter: {counter}", (20,70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
                if counter >= EAR_CONSEC_FRAMES:
                    if not alarm_on:
                        pygame.mixer.music.play(-1)
                        alarm_on = True

                    cv2.putText(frame, "DROWSINESS ALERT!",
                                (20,80), cv2.FONT_HERSHEY_SIMPLEX,
                                0.9, (0,0,255), 3)
            else:
                counter = 0
                alarm_on = False
                pygame.mixer.music.stop()

    cv2.imshow("Driver Monitor", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()