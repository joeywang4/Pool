import pool_size
import pool_ball
import pool_util
import pool_set_bound
import pool_cue
import time
import cv2 as cv
import numpy as np
import argparse
from operator import itemgetter

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--camera", required=False, type = int, help="Specify camera if there are multiple ones.")
args = vars(ap.parse_args())
if type(args["camera"]) == type(None):
   cam = 0
else:
   cam = args["camera"]

#use cv.VideoCapture(1) if webcam is not the default camera
cap = cv.VideoCapture(cam)
Img, Table, old_Table, refPt, old_balls, BallsNum = None, None, None, None, None, None
stableTableDiff = None
lower_hue, upper_hue = None, None
next = True

def Next_command():
   command = input("> ")
   if command == 'help':
      show_help()
   elif command == 'a':
      get_frame()
   elif command == 'b':
      get_table(False)
   elif command == 'c':
      get_table(True)
   elif command == 'd':
      show_table()
   elif command == 'e':
      ball_detect()
   elif command == 'f':
      cue_detect()
   elif command == 'g':
      ball_cue_detect()
   elif command == 'h':
      smooth_detect()
   elif command == 'q':
      return False
   else:
      print('Error command! Use "help" to show commands.')
   
   return True   

def get_frame():
   global Img
   global Table
   global old_Table
   Img = cap.read()[1]
   old_Table = Table
   if type(refPt) != type(None):
      Table = pool_util.get_table(refPt, Img)

def get_table(click):
   global refPt
   global Table
   global lower_hue
   global upper_hue
   if type(Img) == type(None):
      print('Error, Please get frame first!')
      return False
   if click:
      refPt = pool_set_bound.set_bound(Img)
   else:
      refPt = pool_size.get_boundary(Img)
   Table = pool_util.get_table(refPt, Img)
   
   #calculate table hue
   table_blur = cv.medianBlur(Table,5)
   table_hsv = cv.cvtColor(table_blur, cv.COLOR_BGR2HSV)
   mid_hue = pool_util.avg_hue(table_hsv, 50)
   err = 10.01
   lower_hue = np.array([mid_hue - err, 50, 50])
   upper_hue = np.array([mid_hue + err, 255, 255])
   calculateStableTableDiff()
   return True

def calculateStableTableDiff():
   global stableTableDiff
   global Table
   global old_Table
   tableSum = 0.0
   time.sleep(1)
   for i in range(10):
      get_frame()
      tableSum += diff_table(old_Table, Table)
   stableTableDiff = tableSum/10

def show_table():
   if type(Table) == type(None):
      print('Error, Please set boundary first!')
      return False
   print('Press "q" to exit...')
   while True:
      get_frame()
      cv.imshow('table', Table)
      tmp = cv.waitKey(1) & 0xFF
      if tmp == ord('q'):
         break
   cv.destroyAllWindows()

def ball_detect():
   global lower_hue
   global upper_hue
   if type(Table) == type(None):
      print('Error, Please set boundary first!')
      return False
   print('Press "q" to exit...')
   while True:
      get_frame()
      balls = pool_ball.get_ball(Table,lower_hue,upper_hue)
      table = Table.copy()
      if type(balls) != type(None):
         pool_util.draw_ball(balls, table)
      cv.imshow('table', table)
      tmp = cv.waitKey(1) & 0xFF
      if tmp == ord('q'):
         break   
   cv.destroyAllWindows()

def cue_detect():
   if type(Table) == type(None):
      print('Error, Please set boundary first!')
      return False
   print('Press "q" to exit...')
   while True:
      get_frame()
      head, end, _ = pool_cue.get_cue(Table)
      table = Table.copy()
      if head != end:
         pool_util.draw_cue(table, head, end)
      cv.imshow('table', table)
      tmp = cv.waitKey(1) & 0xFF
      if tmp == ord('q'):
         break
   cv.destroyAllWindows()

def ball_cue_detect():
   global lower_hue
   global upper_hue
   if type(Table) == type(None):
      print('Error, Please set boundary first!')
      return False
   print('Press "q" to exit...')
   while True:
      get_frame()
      head, end, _ = pool_cue.get_cue(Table)
      balls = pool_ball.get_ball(Table,lower_hue,upper_hue)
      table = Table.copy()
      if head != end:
         pool_util.draw_cue(table, head, end)
      if type(balls) != type(None):
         pool_util.draw_ball(balls, table)
      cv.imshow('table', table)
      tmp = cv.waitKey(1) & 0xFF
      if tmp == ord('q'):
         break
   cv.destroyAllWindows()

def smooth_detect():
   global lower_hue
   global upper_hue
   global Table
   global old_Table
   global stableTableDiff
   if type(Table) == type(None):
      print('Error, Please set boundary first!')
      return False
   print('Press "q" to exit...')
   global old_balls
   while True:
      get_frame()
      if diff_table(old_Table, Table)<stableTableDiff:
         continue
      head, end, _ = pool_cue.get_cue(Table)
      balls = pool_ball.get_ball(Table,lower_hue,upper_hue)
      table = Table.copy()
      if head != end:
         pool_util.draw_cue(table, head, end)
      if type(balls) != type(None):
         if type(old_balls) != type(None):
            check_diff(balls)
            BallsNum = len(balls[0])
            pool_util.draw_ball(old_balls, table)
         else:
            balls = np.array(sorted(balls[0], key=pool_ball.posOrder))
            balls = np.array([balls])
            old_balls = balls
            BallsNum = len(balls[0])
            pool_util.draw_ball(balls, table)
      cv.imshow('table', table)
      tmp = cv.waitKey(1) & 0xFF
      if tmp == ord('q'):
         break
   cv.destroyAllWindows()

'''
return True if exists difference
'''
def check_diff(balls):
   global old_balls
   balls = np.array(sorted(balls[0], key=pool_ball.posOrder))
   balls = np.array([balls])
   if len(old_balls[0]) != len(balls[0]):
      old_balls = balls
      return True
   for i in range(len(balls[0])):
      if not(abs(balls[0][i][0] - old_balls[0][i][0]) <= 5
         and abs(balls[0][i][1] - old_balls[0][i][1]) <= 5):
         old_balls = balls
         return True
   return False

def diff_table(img1, img2):
   diff = cv.absdiff(Table,old_Table)
   #for i in range(3):
     # idx = diff[:,:,i] < 10
     # diff[idx] = 0
   return np.sum(np.sum(diff))

def show_help():
   print('a. get next frame')
   print('b. set boundary (auto)')
   print('c. set boundary (click)')
   print('d. show table')
   print('e. start ball detection')
   print('f. start cue detection')
   print('g. start ball and cue detection')
   print('h. ball and cue detection v2')
   print('q. quit')

#----------------------------
#The main program begins here
#----------------------------
while next:
   next = Next_command()