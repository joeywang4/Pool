import pool_util
import cv2 as cv
import numpy as np

'''
Find the balls by doing Hough transform
Input type: table img (table part only)
Output type: numpy array ( [[x,y,r], ... ] )
'''
def get_ball(table,lower_hue,upper_hue):   
   #blurring the image
   table_blur = cv.medianBlur(table,5)

   #filter out table hue
   table_hsv = cv.cvtColor(table_blur, cv.COLOR_BGR2HSV)
   mask = cv.inRange(table_hsv, lower_hue, upper_hue)
   mask = cv.bitwise_not(mask)
   table_masked = cv.bitwise_and(table_hsv,table_hsv,mask = mask)
   
   #change to gray scale and find circles
   table_gray = cv.split(table_masked)[2]
   circles = cv.HoughCircles(table_gray,cv.HOUGH_GRADIENT,1,20,
                               param1=30,param2=20,minRadius=8,maxRadius=15)
   if type(circles) == type(None):
      return None
   circles = np.int16(np.around(circles))
   return circles

def reget_a_ball(table, index, old_balls):   
   #blurring the image
   x = old_balls[0][index][0]
   y = old_balls[0][index][1]
   crop_table = table[y-72:y+72, x-72:x+72]
   table_blur = cv.medianBlur(crop_table,5)

   #filter out table hue
   table_hsv = cv.cvtColor(table_blur, cv.COLOR_BGR2HSV)
   mid_hue = pool_util.avg_hue(table_hsv, 50)
   err = 10.01
   lower_hue = np.array([mid_hue - err, 50, 50])
   upper_hue = np.array([mid_hue + err, 255, 255])
   mask = cv.inRange(table_hsv, lower_hue, upper_hue)
   mask = cv.bitwise_not(mask)
   table_masked = cv.bitwise_and(table_hsv,table_hsv,mask = mask)
   
   #change to gray scale and find circles
   table_gray = cv.split(table_masked)[2]
   circles = cv.HoughCircles(table_gray,cv.HOUGH_GRADIENT,1,20,
                               param1=30,param2=20,minRadius=8,maxRadius=15)
   if type(circles) == type(None):
      return None
   if len(circles[0])>1:
      return get_ball(table)
   else:
      circles = np.int16(np.around(circles))
      old_balls[0][index][0] = x - 72 -1 + circles[0][i][0]
      old_balls[0][index][1] = y - 72 -1 + circles[0][i][1]
   return old_balls

def posOrder(coordinate):
    return coordinate[0]*coordinate[0]+coordinate[1]*coordinate[1]