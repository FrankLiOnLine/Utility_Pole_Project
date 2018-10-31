import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('pole.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

gray = cv2.GaussianBlur(gray,(3,3),0)
edges = cv2.Canny(gray,1,700, apertureSize=3)
plt.subplot(121),plt.imshow(edges,'gray')
plt.xticks([]),plt.yticks([])

lines = cv2.HoughLinesP(edges,1,np.pi/180,200,minLineLength=200,maxLineGap=10)
lines1 = lines[:,0,:]
for x1,y1,x2,y2 in lines1[:]: 
    cv2.line(img,(x1,y1),(x2,y2),(255,0,0),1)

plt.subplot(122),plt.imshow(img,)
plt.xticks([]),plt.yticks([])
plt.show()