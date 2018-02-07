import pool_size
import pool_set_bound
import pool_ball
import pool_util
import pool_cue
import cv2 as cv
import numpy as np
from operator import itemgetter

Img, Table, refPt, old_balls, cap = None, None, None, None, None

#use cv.VideoCapture(1) if webcam is not the default camera
def init(cam):
   global Img
   global Table
   global refPt
   global cap

   if type(cam) != type(0):
      print('Initiation fail!')
      return False
   cap = cv.VideoCapture(cam)

   #drop the first five images
   for _ in range(5):
      Img = cap.read()[1]
   
   done = False
   while not done:
      Img = cap.read()[1]
      refPt = pool_size.get_boundary(Img)
      Table = pool_util.get_table(refPt, Img)
      if type(Table) != type(None):
         cv.imshow('table', Table)
         print('Press any key to continue...')
         cv.waitKey(0)
         cv.destroyAllWindows()
         result = input("Is the table correct?(y/n)")
         if result.lower() == 'y':
            done = True
         elif result.lower() == 'n':
            result = input("Type 'y' to try again or type 'n' to set boundary manually.(y/n)")
            if result.lower() == 'n':
               cv.destroyAllWindows()
               refPt = pool_set_bound.set_bound(Img)
               Table = pool_util.get_table(refPt, Img)
               done = True
            elif result.lower() != 'y':
               print('Error input!')
         else:
            print('Error input!')
   print('Initiation succeed...')

def get_frame():
   global refPt
   global Img
   global Table
   global cap
   if type(refPt) != type(np.array(0)):
      print('Not initialize yet...')
      return False
   Img = cap.read()[1]
   Table = pool_util.get_table(refPt, Img)

def detect():
   if type(Table) == type(None):
      print('Error, Please initialize first!')
      return False
   print('Detection begin...')
   global old_balls
   while True:
      get_frame()
      head, end, deg = pool_cue.get_cue(Table)
      balls = pool_ball.get_ball(Table)
      if type(balls) != type(None):
         if type(old_balls) != type(None):
            check_diff(balls)
         else:
            balls = np.array(sorted(balls[0], key=itemgetter(0,1)))
            balls = np.array([balls])
            old_balls = balls
         balls = old_balls[0]
      '''
      ---------------------
      put your code here...
      ---------------------
      '''
      if type(deg) != type(None):
         print(deg)

'''
return True if exists difference
'''
def check_diff(balls):
   global old_balls
   balls = np.array(sorted(balls[0], key=itemgetter(0,1)))
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