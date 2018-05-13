import pool_size
import pool_ball
import pool_util
import pool_set_bound
import pool_cue
import traj_calc
import cv2 as cv
import numpy as np
import argparse
from operator import itemgetter

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--camera", required=False, type = int, help="Specify camera if there are multiple ones.")
ap.add_argument("-r", "--refpt", required=False, nargs='+', type = int, help="Specify minx miny maxx maxy ((x0,y0), (x1, y1)) of the table.")
args = vars(ap.parse_args())
if type(args["camera"]) == type(None):
   cam = 1
else:
   cam = args["camera"]

#use cv.VideoCapture(1) if webcam is not the default camera
cap = cv.VideoCapture(cam)
#below is for mac only
cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
Img, Table, refPt, old_balls = None, None, None, None
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
   elif command == 'ball':
      show_balls()
   elif command == 'cue' :
      show_both()
   elif command == 'q':
      return False
   else:
      print('Error command! Use "help" to show commands.')
   
   return True   

def get_frame():
   global Img
   global Table
   Img = cap.read()[1]
   if type(refPt) != type(None):
      Table = pool_util.get_table(refPt, Img)

def get_table(click):
   global refPt
   global Table
   if type(Img) == type(None):
      print('Error, Please get frame first!')
      return False
   if click:
      refPt = pool_set_bound.set_bound(Img)
   else:
      refPt = pool_size.get_boundary(Img)
   Table = pool_util.get_table(refPt, Img)
   print('refPt',refPt)
   return True

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
   if type(Table) == type(None):
      print('Error, Please set boundary first!')
      return False
   print('Press "q" to exit...')
   while True:
      get_frame()
      balls = pool_ball.get_ball(Table)
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
   if type(Table) == type(None):
      print('Error, Please set boundary first!')
      return False
   print('Press "q" to exit...')
   while True:
      get_frame()
      head, end, _ = pool_cue.get_cue(Table)
      balls = pool_ball.get_ball(Table)
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
   if type(Table) == type(None):
      print('Error, Please set boundary first!')
      return False
   print('Press "q" to exit...')
   global old_balls
   while True:
      get_frame()
      head, end, _ = pool_cue.get_cue(Table)
      balls = pool_ball.get_ball(Table)
      table = Table.copy()
      if head != end:
         pool_util.draw_cue(table, head, end)
      if type(balls) != type(None):
         if type(old_balls) != type(None):
            check_diff(balls)
            pool_util.draw_ball(old_balls, table)
         else:
            balls = np.array(sorted(balls[0], key=itemgetter(0,1)))
            balls = np.array([balls])
            old_balls = balls
            pool_util.draw_ball(balls, table)
      cv.imshow('table', table)
      tmp = cv.waitKey(1) & 0xFF
      if tmp == ord('q'):
         break
   cv.destroyAllWindows()

def show_balls():
   if type(Table) == type(None):
      print('Error, Please set boundary first!')
      return False
   balls = pool_ball.get_ball(Table)
   if type(balls) == type(None):
      print('No balls found...')
      return False
   table = Table.copy()
   pool_util.draw_ball(balls, table)
   cv.imshow('table', table)
   print('Press any key to continue...')
   '''
   bound = np.array([refPt[0][0], refPt[0][1], 0])
   balls = np.add(balls,bound)
   '''
   print('balls', balls)
   cv.waitKey(0)
   cv.destroyAllWindows()

def show_both():
   if type(Table) == type(None):
      print('Error, Please set boundary first!')
      return False
   head, end, _ = pool_cue.get_cue(Table)
   balls = pool_ball.get_ball(Table)
   if head == end:
      print('No cue found...')
      return False
   if type(balls) == type(None):
      print('No balls found...')
      return False
   table = Table.copy()
   pool_util.draw_cue(table, head, end)
   pool_util.draw_ball(balls, table)
   print("cue:", head, end)
   print("balls:", balls[0])
   line_list = traj_calc.init(balls[0], np.array([head, end]), refPt[2][0]-refPt[0][0], refPt[0][1]-refPt[2][1])
   print("lines:", line_list)
   pool_util.draw_line(table,line_list)
   cv.imshow('table', table)
   print('Press any key to continue...')
   cv.waitKey(0)
   cv.destroyAllWindows()

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


def show_help():
   print('a. get next frame')
   print('b. set boundary (auto)')
   print('c. set boundary (click)')
   print('d. show table')
   print('e. start ball detection')
   print('f. start cue detection')
   print('g. start ball and cue detection')
   print('h. ball and cue detection v2')
   print('ball. show balls')
   print('cue. show cue')
   print('q. quit')

#----------------------------
#The main program begins here
#----------------------------
if type(args["refpt"]) != type(None):
   get_frame()             #drop the first frame
   pt = tuple(args["refpt"])
   refPt = np.array([ [pt[0], pt[3]], [pt[0], pt[1]], [pt[2], pt[1]], [pt[2], pt[3]] ])
   get_frame()

while next:
   next = Next_command()