import cv2
import numpy as np

img = cv2.imread('test.png')
rows, cols, asdf = img.shape

a = [[543,285],[1961,285],[543,1603],[1961,1603]]
b = [[300,0],[2249,0],[300,1885],[2249,1885]]   # 왼쪽위점, 오른쪽위점, 왼쪽아래점, 오른쪽아래점

pts1 = np.float32(a)
pts2 = np.float32(b)

img = cv2.circle(img, (a[0][0], a[0][1]), 3, (0,0,255),-1)
img = cv2.circle(img, (a[1][0], a[1][1]), 3, (0,0,255),-1)
img = cv2.circle(img, (a[2][0], a[2][1]), 3, (0,0,255),-1)
img = cv2.circle(img, (a[3][0], a[3][1]), 3, (0,0,255),-1)
#cv2.circle(img, c, 5, (55, 255, 55), -1)

M = cv2.getPerspectiveTransform(pts1, pts2)
dst = cv2.warpPerspective(img, M, (1440, 1080))  # 변환후 크기 (x좌표, y좌표)
imS = cv2.resize(img, (1440, 1080)) 
dsts = cv2.resize(dst, (1000, 967))
cv2.imshow('imgage', imS)
cv2.imshow('dst', dst)
cv2.waitKey(0)