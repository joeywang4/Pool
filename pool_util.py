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
*change the default radius if it doesn't fit
Input type: balls (numpy array), and image of the table
Return type: None
'''
def draw_ball(balls, table, radius = 12):
   for i in balls[0]:
      # draw the outer circle
      cv.circle(table,(i[0],i[1]),radius,(0,255,0),2)
      # draw the center of the circle
      cv.circle(table,(i[0],i[1]),2,(0,0,255),3)

'''
Show the detected cue
Input type: table image, head of the cue and end of the cue
Return type: None
'''
def draw_cue(table, head, end):
   cv.line(table, head, end, (255,0,255), thickness=5)
   cv.drawMarker(table, head, (255,255,0))