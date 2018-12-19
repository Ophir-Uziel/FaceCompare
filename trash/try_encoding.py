import face_recognition
import cv2

img = cv2.imread('IlhamAnas.jpg')
a = face_recognition.face_encodings(img)

print(a[0])