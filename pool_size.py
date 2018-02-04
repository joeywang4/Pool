import cv2 as cv
import numpy as np

'''
computes the average hue in middle region
input: source image(in hsv type), middle region size(in pixel)
return type: int
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
Returns the inner boundary of the pool table
Input type: image of the table
Return type: [[top-left point], [bottom-left point], [bottom-right point], [top-right point]]
'''
def get_boundary(image):
   img = image
   img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
   
   #get middle hue
   mid_hue = avg_hue(img_hsv, 50)

   #filter image with specified color
   err = 20.01
   lower_hue = np.array([mid_hue - err, 25, 25])
   upper_hue = np.array([mid_hue + err, 255, 255])
   mask = cv.inRange(img_hsv, lower_hue, upper_hue)
   img_masked = cv.bitwise_and(img,img,mask = mask)
   
   #opening to filter out noise
   rect = cv.getStructuringElement(cv.MORPH_RECT, (15, 15))
   img_filted_open = cv.morphologyEx(img_masked, cv.MORPH_OPEN, rect)
   
   #find contours, approx poly, find rect
   img_edge = cv.Canny(img_filted_open, 30, 90)
   img_contours = cv.findContours(img_edge, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[1]
   #approx poly
   img_contours_poly = []
   rects = []
   index = 0
   for index in range(len(img_contours)):
      rects.append(cv.boundingRect( img_contours[index]))

   #choose max rect
   max_rect = rects[0]
   for rect in rects:
      if max_rect[2]*max_rect[3] < rect[2]*rect[3]:
         max_rect = rect
   #get the inner table (to get the inside boundary)
   shrink = 0
   table = img[max_rect[1]+shrink : max_rect[1]+max_rect[3]-shrink,
               max_rect[0]+shrink : max_rect[0]+max_rect[2]-shrink]
   
   table_gray = cv.cvtColor(table, cv.COLOR_BGR2GRAY)
   table_mid_point = [max_rect[3]//2 - shrink, max_rect[2]//2 - shrink]
   mid_val = table_gray[table_mid_point[0],table_mid_point[1]]
   table_bin = cv.threshold(table_gray, mid_val-30, 255, cv.THRESH_BINARY_INV)[1]
   
   #opening
   rect = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
   table_filted_open = cv.morphologyEx(table_bin, cv.MORPH_OPEN, rect)
   
   #canny
   table_filted_edge = cv.Canny(table_filted_open, 50, 0)
   #hough lines
   hough_lines = cv.HoughLinesP(table_filted_edge, 0.01, np.pi/180, 15, 0,50, 5)
   
   #sort lines
   vert_lines = []
   hori_lines = []
   for hough_line in hough_lines:
      if hough_line[0][0] == hough_line[0][2]:
         vert_lines.append(hough_line[0])
      elif hough_line[0][1] == hough_line[0][3]:
         hori_lines.append(hough_line[0])
   
   #find bound
   upper_bound, lower_bound = 0, 1080
   for line in hori_lines:
      if line[1] < lower_bound:
         lower_bound = line[1]
      if line[1] > upper_bound:
         upper_bound = line[1]
   left_bound, right_bound = 1920, 0
   for line in vert_lines:
      if line[0] < left_bound:
         left_bound = line[0]
      if line[0] > right_bound:
         right_bound = line[0]
   upper_bound += max_rect[1]+shrink
   lower_bound += max_rect[1]+shrink
   left_bound += max_rect[0]+shrink
   right_bound += max_rect[0]+shrink

   return np.array([[left_bound,upper_bound],[left_bound,lower_bound],
                    [right_bound,lower_bound],[right_bound,upper_bound]])