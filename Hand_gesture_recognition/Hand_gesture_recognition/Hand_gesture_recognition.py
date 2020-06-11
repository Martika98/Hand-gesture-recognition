import numpy as np
import cv2
import math

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
image = cv2.imread("image.jpg")
height, width, _ = image.shape
f = cv2.resize(image, (int(height * 0.4), int(width * 0.4)))
frame = cv2.fastNlMeansDenoisingColored(f,None,10,10,7,21)
image2 = np.zeros(frame.shape)

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
lower_skin = np.array([0,20,70])
upper_skin = np.array([20,255,255])
mask = cv2.inRange(hsv, lower_skin, upper_skin)
kernel = np.ones((2,2), np.uint8)
mask = cv2.GaussianBlur(mask, (3,3), 100)
#mask = cv2.medianBlur(mask, 1)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
#mask = cv2.dilate(mask, kernel, iterations = 4)
contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #wyszukiwania konturów na obrazie po progowaniu
#cv2.drawContours(image2, contours, -1, (0,255,0), 3)
cnt = max(contours, key = lambda x: cv2.contourArea(x))

#for cnt in contours:
approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
cv2.drawContours(image2, [approx], -1, (255,0 ,0), 3)
print (len(approx))

cv2.imshow('image', image2)
cv2.waitKey(0)
cv2.destroyAllWindows