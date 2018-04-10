import cv2 as cv
import numpy as np
import pool_util

#read the image and get inner boundary
name = '/home/joey/py/opencv/camera/table.png'
table = cv.imread(name)

#filt out the table and opening
table_hsv = cv.cvtColor(table, cv.COLOR_BGR2HSV)
mid_hue = pool_util.avg_hue(table_hsv, 40)
err = 10.01
lower_hue = np.array([mid_hue - err, 50, 50])
upper_hue = np.array([mid_hue + err, 255, 255])
mask = cv.inRange(table_hsv, lower_hue, upper_hue)
mask = cv.bitwise_not(mask)
table_masked = cv.bitwise_and(table_hsv,table_hsv,mask = mask)
rect = cv.getStructuringElement(cv.MORPH_RECT, (10, 10))
table_filted_open = cv.morphologyEx(table_hsv, cv.MORPH_OPEN, rect)
cv.imshow('filt', table_masked)

#canny and find contours
table_edge = cv.Canny(table_filted_open, 70, 210)
img_contours = cv.findContours(table_edge, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[1]

#approx poly
img_contours_poly = []
circles_tmp = []
circles = []
index = 0
for index in range(len(img_contours)):
   img_contours_poly.append(cv.approxPolyDP(img_contours[index], 3, True))
   circles_tmp.append(cv.minEnclosingCircle(img_contours_poly[index]))
for circle in circles_tmp:
   if circle[1] > 3.0:
      circles.append((round(circle[0][0]),round(circle[0][1]//1)))
for circle in circles:
   cv.drawMarker(table, circle, (100,0,255))
cv.imshow('ha', table)
cv.imshow('haha', table_edge)
cv.imwrite('output.png', table)
cv.waitKey(0)