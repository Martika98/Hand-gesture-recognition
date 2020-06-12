import numpy as np
import cv2
import math

cv2.namedWindow('image', cv2.WINDOW_NORMAL) #okno o zmiennym rozmiarze
image = cv2.imread("image.jpg")
height, width, _ = image.shape
frame = cv2.resize(image, (int(width * 0.4), int(height * 0.4)))
#frame = cv2.fastNlMeansDenoisingColored(f,None,10,10,7,21) usuwanie szumu
image2 = np.zeros(frame.shape)

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
lower_skin = np.array([0,20,70]) #wybrany kolor skóry
upper_skin = np.array([20,255,255])
mask = cv2.inRange(hsv, lower_skin, upper_skin) #obszar o kolorze skóry

kernel = np.ones((2,2), np.uint8)
mask = cv2.GaussianBlur(mask, (3,3), 100) #rozmycie 
#mask = cv2.medianBlur(mask, 1)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel) #operacja zamknięcia maski
#mask = cv2.dilate(mask, kernel, iterations = 4)
contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #wyszukiwanie konturów na obrazie po progowaniu
cv2.drawContours(image2, contours, -1, (0,255,0), 3) 
cnt = max(contours, key = lambda x: cv2.contourArea(x)) #kontur o maksymalnej wielkości
hull = cv2.convexHull(cnt) 
cv2.drawContours(image2, [hull], -1, (0, 0 ,255), 3)

#areahull = cv2.contourArea(hull)
#areacnt = cv2.contour
lcnt = cv2.arcLength(cnt, 1) #obwód maksymalnego konturu
lhull = cv2.arcLength(hull, 1) #obwód hull
w = lcnt/lhull #współczynnik w
acnt = cv2.contourArea(cnt)
ahull = cv2.contourArea(hull)
a = acnt/ahull
approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
cv2.drawContours(image2, [approx], -1, (255,0 ,0), 3)

#rozróżnianie gestów opierać się będzie na porównaniu współczynnika w
#(różnica obwodów hull i cnt chyba jest bardziej wyraźna niż różnica między powierzchniami)
# i ilości krawędzi wielokąta przybliżającego
#co jeśli ręka wychodzi z rogu i program zliczy punkt więcej


print (len(approx))
print (w)
print (a)

cv2.imshow('image', image2)
cv2.waitKey(0)
cv2.destroyAllWindows