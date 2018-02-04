import cv2 as cv
import numpy as np

'''
Draw the table with yellow lines
Input type: corner points, and file name
Return type: mat
'''
def draw_table(refPt, image):
   drawed = image.copy()
   cv.polylines(drawed, [refPt], True, (100,0,255))
   return drawed

'''
Get the table part of the input image
Input type: file name
Return type: mat
'''
def get_table(refPt, image):
   x,y,w,h = cv.boundingRect(refPt)
   table = image[y:y+h,x:x+w]
   return table

'''
Computes the average hue in middle region
Input type: source image(in hsv type), middle region size(in pixel)
Return type: int
'''
def avg_hue(src, mid_size):
   mid_size = 50   
   height, width, _ = src.shape
   mid_point = [height//2, width//2]
   mid_region = src[mid_point[0]:mid_point[0] + mid_size,
                    mid_point[1]:mid_point[1] + mid_size]
   mid_hue = 0
   for i in mid_region:
      for j in i:
         mid_hue += j[0]
   mid_hue //= (mid_size**2)
   return mid_hue

'''
Show the detected balls
Input type: balls (numpy array), and image of the table
Return type: None
'''
def draw_ball(balls, image):
   table = image.copy()
   for i in balls[0,:]:
      # draw the outer circle
      cv.circle(table,(i[0],i[1]),i[2],(0,255,0),2)
      # draw the center of the circle
      cv.circle(table,(i[0],i[1]),2,(0,0,255),3)
   cv.imshow('detected balls', table)
   cv.waitKey(0)
   cv.destroyAllWindows()