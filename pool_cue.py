import cv2 as cv
import numpy as np
import pool_util

def get_cue(table):
   table_blur = cv.medianBlur(table,5)
   #filter out table hue
   table_hsv = cv.cvtColor(table_blur, cv.COLOR_BGR2HSV)
   mid_hue = pool_util.avg_hue(table_hsv, 40)
   err = 30.01
   lower_hue = np.array([mid_hue - err, 25, 25])
   upper_hue = np.array([mid_hue + err, 255, 255])
   mask = cv.inRange(table_hsv, lower_hue, upper_hue)
   mask = cv.bitwise_not(mask)
   table_masked = cv.bitwise_and(table_hsv,table_hsv,mask = mask)
   table_filted_edge = cv.Canny(table_masked, 60, 180)
   hough_lines = cv.HoughLinesP(table_filted_edge, 1, np.pi/180, 90, 0,50, 10)
   if type(hough_lines) == type(None):
      return (0,0),(0,0),None
   #calculate the average slope
   total_x, total_y = 0,0
   for line in hough_lines:
      total_x += line[0][2] - line[0][0]
      total_y += line[0][3] - line[0][1]
   if total_x == 0:
      if total_y > 0:
         avg_deg = 90
      else:
         avg_deg = -90
   else:
      avg_deg = int(np.arctan(total_y/total_x)*180//np.pi)

   #get the start and end point
   min_pt, max_pt = (999,0), (0,0)
   for line in hough_lines:
      x = line[0][2] - line[0][0]
      y = line[0][3] - line[0][1]
      if x == 0:
         if y > 0:
            deg = 90
         else:
            deg = -90
      else:
         deg = int(np.arctan(y/x)*180/np.pi)
      if deg <= avg_deg+2 and deg >= avg_deg-2:
         if line[0][0] < line[0][2]:
            if line[0][0] < min_pt[0]:
               min_pt = (line[0][0], line[0][1])
            if line[0][2] > max_pt[0]:
               max_pt = (line[0][2], line[0][3])
         else:
            if line[0][2] < min_pt[0]:
               min_pt = (line[0][2], line[0][3])
            if line[0][0] > max_pt[0]:
               max_pt = (line[0][0], line[0][1])

   #find the head of cue
   height, width, _ = table.shape
   min_d = min(min_pt[0], min_pt[1], abs(min_pt[0]-width), abs(min_pt[1]-height))
   max_d = min(max_pt[0], max_pt[1], abs(max_pt[0]-width), abs(max_pt[1]-height))
   if min_d < max_d:
      head = max_pt
      if total_x != 0:
         end = (min_pt[0], max_pt[1]-(max_pt[0]-min_pt[0])*(total_y/total_x))
      else:
         end = (max_pt[0], max_pt[1]-150*(sign(max_pt[1]-min_pt[1])))
   else:
      head = min_pt
      if total_x != 0:
         end = (max_pt[0], min_pt[1]+(max_pt[0]-min_pt[0])*(total_y/total_x))
      else:
         end = (min_pt[0], min_pt[1]-150*(sign(min_pt[1]-max_pt[1])))
   head = int(head[0]//1), int(head[1]//1)
   end = int(end[0]//1), int(end[1]//1)
   return head, end, avg_deg

def sign(num):
   if num >=0:
      return 1
   else: return -1