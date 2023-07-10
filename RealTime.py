import cv2
import time



cap = cv2.VideoCapture(1)

pTime = 0
cTime = 0
while True:
    success, img = cap.read()
    cv2.imshow('Image',img)
    cv2.waitKey(1)





