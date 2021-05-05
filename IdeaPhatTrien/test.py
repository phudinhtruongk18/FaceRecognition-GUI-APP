# import cv2
#
# face_cascade = cv2.CascadeClassifier('../Model/data/haarcascade_frontalface_default.xml')
#
# cap = cv2.VideoCapture("../Model/data/video/BeEm.mp4")
# while True:
#     bruuh, frame = cap.read()
#     gray = cv2.cvtColor(cv2.UMat(frame), cv2.COLOR_BGR2GRAY)
#     if frame is None:
#         break
#     faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#     cv2.imshow("image", frame)
#     cv2.imshow("image3", gray)
#     if cv2.waitKey(20) & 0xFF == ord('q'):
#         break
import numpy as np

faces = [(2,2,2,2),(2,2,2,2)]
list_users = ["phu","phu","phu","phu","phu","phu","phu","phu","phu","phu","phu","phu","phu","phu","phu"]
arrayConfidence = np.zeros((len(faces), len(list_users)), dtype=np.int16)
# arrayConfidence[0]
arrayConfidence[0][0] = 1
arrayConfidence[0][3] = 5
arrayConfidence[1][0] = 8
arrayConfidence[1][3] = 7
print(arrayConfidence[0].argmin())
