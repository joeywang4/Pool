import cv2 as cv
import numpy as np

width, height = 0,0
refPt = np.array([[0,0],[0,0],[0,0],[0,0]])
#top-left, down-left, down-right, top-right
image = None

def set_bound(img):
   global image
   global refPt
   global width
   global height
   image = img
   height, width = image.shape[:2]
   refPt = np.array([[0,0],[0,height-1],[width-1,height-1],[width-1,0]])
   count = 0
   cv.namedWindow("image")
   cv.setMouseCallback("image", click_and_crop)
   cv.imshow('image', image)
   cv.waitKey(0)
   cv.destroyAllWindows()
   return refPt

def click_and_crop(event, x, y, flags, param):
   # grab references to the global variables
   global refPt
   # if the left mouse button was clicked, record the starting
   # (x, y) coordinates and indicate that cropping is being
   # performed
   if event == cv.EVENT_LBUTTONUP:
      sec = get_sector(x,y)
      refPt[sec] = [x,y]
      drawed = image.copy()
      cv.polylines(drawed, [refPt], True, (255,0,255))
      cv.imshow("image", drawed)

def get_sector(x,y):
   if x < width//2:
      if y < height//2:
         return 0
      else: return 1
   elif y < height//2:
      return 3
   else: return 2