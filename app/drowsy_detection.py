import cv2
import dlib
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
    return (A + B) / (2.0 * C)

# ----------------- LOAD MODELS -----------------
print("Loading models...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
print("Models loaded successfully!")

# Eye landmark indexes
LEFT_EYE  = list(range(36, 42))
RIGHT_EYE = list(range(42, 48))

# ----------------- CAMERA -----------------
print("Connecting to camera stream...")
cap = cv2.VideoCapture("http://10.188.69.227:5000/video")

if not cap.isOpened():
    print("ERROR: Could not connect to camera stream!")
    exit()

print("Camera connected!")

EAR_THRESHOLD   = 0.22
EAR_CONSEC_FRAMES = 17
counter  = 0
alarm_on = False
ear = 0.0  # Initialize ear variable

# ----------------- MAIN LOOP -----------------
print("Starting detection...")
frame_count = 0

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame, retrying...")
            continue

        frame_count += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray, 0)

        # Reset ear if no faces detected
        face_detected = False

        for face in faces:
            face_detected = True
            landmarks = predictor(gray, face)
            shape = np.array([[landmarks.part(i).x, landmarks.part(i).y]
                              for i in range(68)])

            leftEye  = shape[36:42]
            rightEye = shape[42:48]

            leftEAR  = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0

            # Draw eye points
            for (ex, ey) in np.concatenate((leftEye, rightEye), axis=0):
                cv2.circle(frame, (int(ex), int(ey)), 2, (0, 255, 0), -1)

            cv2.putText(frame, f"EAR: {ear:.2f}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # --------- DROWSINESS DETECTION ----------
            if ear < EAR_THRESHOLD:
                counter += 1
                cv2.putText(frame, f"Counter: {counter}", (20, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                if counter >= EAR_CONSEC_FRAMES:
                    if not alarm_on:
                        pygame.mixer.music.play(-1)
                        alarm_on = True
                    cv2.putText(frame, "DROWSINESS ALERT!",
                                (20, 100), cv2.FONT_HERSHEY_SIMPLEX,
                                0.9, (0, 0, 255), 3)
            else:
                counter  = 0
                alarm_on = False
                pygame.mixer.music.stop()

        if not face_detected:
            counter = 0
            ear = 0.0
            alarm_on = False
            pygame.mixer.music.stop()
            cv2.putText(frame, "No face detected", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Print status to terminal
        if frame_count % 10 == 0:  # Print every 10 frames to reduce spam
            print(f"Frame {frame_count:5d} | EAR: {ear:.2f} | Counter: {counter:2d} | Alarm: {alarm_on}")

except KeyboardInterrupt:
    print("\n✓ Detection stopped by user")
finally:
    pygame.mixer.music.stop()
    cap.release()
    print("✓ Resources released")