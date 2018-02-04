import pool_util
import cv2 as cv
import numpy as np

'''
Find the balls by doing Hough transform
Input type: table img (table part only)
Output type: numpy array ( [[x,y,r], ... ] )
'''
def get_ball(table):   
   #blurring the image
   table_blur = cv.medianBlur(table,5)

   #filter out table hue
   table_hsv = cv.cvtColor(table_blur, cv.COLOR_BGR2HSV)
   mid_hue = pool_util.avg_hue(table_hsv, 40)
   err = 10.01
   lower_hue = np.array([mid_hue - err, 50, 50])
   upper_hue = np.array([mid_hue + err, 255, 255])
   mask = cv.inRange(table_hsv, lower_hue, upper_hue)
   mask = cv.bitwise_not(mask)
   table_masked = cv.bitwise_and(table_hsv,table_hsv,mask = mask)
   
   #change to gray scale and find circles
   table_gray = cv.split(table_masked)[2]
   circles = cv.HoughCircles(table_gray,cv.HOUGH_GRADIENT,1,20,
                               param1=30,param2=20,minRadius=0,maxRadius=50)
   circles = np.uint16(np.around(circles))
   return circles