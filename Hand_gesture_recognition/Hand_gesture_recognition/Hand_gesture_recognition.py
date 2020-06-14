import numpy as np
import cv2
import math

font = cv2.FONT_HERSHEY_SIMPLEX
l = 0 # ilość deformacji
lo = 0 # ilość punktów pomiędzy palcami ostre kąty
rangle = 0 # ilość kątów prostych
cv2.namedWindow('image', cv2.WINDOW_NORMAL) #okno o zmiennym rozmiarze
image = cv2.imread("image.jpg")
height, width, _ = image.shape
frame = image[50:(height-50), 50:(width-50)]
image2 = np.zeros(frame.shape)

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
lower_skin = np.array([0,20,70]) #wybrany kolor skóry
upper_skin = np.array([20,255,255])
mask = cv2.inRange(hsv, lower_skin, upper_skin) #obszar o kolorze skóry

kernel = np.ones((2,2), np.uint8)
mask = cv2.GaussianBlur(mask, (3,3), 100) #rozmycie 
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel) #operacja zamknięcia maski
contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #wyszukiwanie konturów na obrazie po progowaniu

cnt = max(contours, key = lambda x: cv2.contourArea(x)) #kontur o maksymalnej wielkości
cnt = cv2.approxPolyDP(cnt, 0.00001*cv2.arcLength(cnt, True), True) # wcześniej było 0.00001
cv2.drawContours(image2, cnt, -1, (0,255,0), 3) 
hull = cv2.convexHull(cnt, returnPoints = False)
hull2 = cv2.convexHull(cnt)

lcnt = cv2.arcLength(cnt, 1) # obwód maksymalnego konturu
lhull = cv2.arcLength(hull2, 1) # obwód hull
w = lcnt/lhull #współczynnik obwodów
acnt = cv2.contourArea(cnt) # powierzchnia konturu
ahull = cv2.contourArea(hull2)
aq = acnt/ahull # współczynnik powierzchni
# fin to współrzędna y od punktu w miejscu zgjęcia kciuka (w wielokącie)
fin1 = 0 #punkty sąsiadujace do fin
fin2 = 0
defects = cv2.convexityDefects(cnt, hull) # defekty hull
n = defects.shape[0]
for i in range (n):
    s, e, f, d = defects[i, 0]
    start = tuple(cnt[s][0]) # początek odcinka na którym występuje defekt między hull'em a konturem
    end = tuple(cnt[e][0]) #koniec odcinka
    far = tuple(cnt[f][0]) # najbardziej odległy punkt defektu

    lngratio = d/acnt * 100 # współczynnik pokazujący odległośc między maks defektu a hull

    a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
    b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
    c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
    cosang = (b**2 + c**2 - a**2) / (2*b*c) # cosinus kąta między palcami rąk
    ang = math.acos(cosang) # kąt między palcami dłoni swej

    if( lngratio > 4.0): # odległość jest wystarczająco duża
        cv2.line(image2, start, end, [0,230, 230], 2)
        cv2.circle(image2, far, 5, [0, 0, 255], -1)
        l = l +1
        if (ang < 1.3): # kąt ostry 
            lo = lo + 1
        if (ang > 1.3 and ang < 1.75): # kąt prosty
            rangle = 1
            fin1 = start[1]
            fin2 = end[1]

approx = cv2.approxPolyDP(cnt, 0.0185*cv2.arcLength(cnt, True), True) # przybliżenie konturu wielokątem
cv2.drawContours(image2, [approx], -1, (255,0 ,0), 3)
maxy = 0
miny = height


for app in approx:
    _, y = app[0]
    if maxy < y :
        maxy = y
    if miny > y :
        miny = y





lk = len(approx) # liczba krawędzi w wielokącie 

if lo == 0 and rangle == 0:
    if w > 1.09 and w < 1.38 and lk < 9 and aq < 0.8:
        cv2.putText(image2,'Wskazywanie',(50,100), font, 2, (128,0,255), 5, cv2.LINE_AA)
if lo == 1 or lo == 0:
    if lk > 7 and lk < 10:
        if aq > 0.5 and aq < 0.62:
            if w > 1.27:
                cv2.putText(image2,'Legiunia',(180,100), font, 2, (128,0,255), 5, cv2.LINE_AA)
if lo == 1:
    if l == 2 or l==1:
        if w > 1.21 and w < 1.35:
            if lk == 6 or lk == 7:
                cv2.putText(image2,'Dwa',(50,250), font, 2, (128,0,255), 5, cv2.LINE_AA)
if lo == 2:
    if lk == 9 or lk == 8:
        if l==3 or l == 4 or l==2:
            if w < 1.4 and w > 1.3:
                cv2.putText(image2,'Trzy',(180,250), font, 2, (128,0,255), 5, cv2.LINE_AA)
if lo == 3:
    if lk == 9 or lk == 10 or lk == 11:
        if w > 1.4 and w < 1.6:
            cv2.putText(image2,'Cztery',(50,350), font, 2, (128,0,255), 5, cv2.LINE_AA)
if w > 2.1:
    cv2.putText(image2,'Machanie',(180,350), font, 2, (128,0,255), 5, cv2.LINE_AA)
if lo ==4 and lk > 1.8:
    if aq > 0.59 and aq < 0.78:
        if lk > 8:
            cv2.putText(image2,'Machanie',(180,350), font, 2, (128,0,255), 5, cv2.LINE_AA)
    if aq > 0.78:
            cv2.putText(image2,'Piatka',(50,450), font, 2, (128,0,255), 5, cv2.LINE_AA)
if aq < 0.58 and lk > 11 and w > 1.6:
    cv2.putText(image2,'Machanie',(180,450), font, 2, (128,0,255), 5, cv2.LINE_AA)
if lk ==7 and lo == 1:
    if w > 1.28 and w < 1.4:
        cv2.putText(image2,'Przekazany znak pokoju',(50,550), font, 5, (128,0,255), 3, cv2.LINE_AA)
if rangle == 1 and aq > 0.65 and lo < 2:
    if ((maxy < fin1 +100 and maxy > fin1 - 100) or (maxy < fin2 + 100 and maxy > fin2 - 100)): # jeśli któryś z puntów sąsiadujacych jest najwyższym punktem wielokąta, to bardzoprawdopodobne, ze jest to punkt kciuka w dół
        cv2.putText(image2,'Nie ok',(180,550), font, 2, (128,0,255), 5, cv2.LINE_AA)
    if ((miny < fin1 +100 and miny > fin1 - 100) or (miny < fin2 + 100 and miny > fin2 - 100)): # jeśli któryś z punktów sąsiadujących jest najniżej, to prawdopodobnie jest to kciuk w górę
        cv2.putText(image2, 'OK', (50,650), font, 2, (128,0,255), 5, cv2.LINE_AA)
if lo == 0 and l ==0:
    if aq > 0.8 and w <1.35:
        cv2.putText(image2,'Piesc',(180,650), font, 2, (128,0,255), 5, cv2.LINE_AA)
if l == 1:
    if lo == 0:
        if lk == 6 or lk == 5:
            cv2.putText(image2,'Znak szatana',(50,750), font, 2, (128,0,255), 5, cv2.LINE_AA)


print (lo)
print (lk)
print (l)

print (w)
print (aq)
print (rangle)

print (fin1)
print (fin2)
print (miny)
print (maxy)



cv2.imshow('image', image2)
cv2.waitKey(0)
cv2.destroyAllWindows