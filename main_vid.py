import pool_size
import pool_ball
import pool_util
import pool_set_bound
import pool_cue
import cv2 as cv
import numpy as np

#use cv.VideoCapture(1) if webcam is not the default camera
cap = cv.VideoCapture(0)
Img, Table, refPt = None, None, None
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
      head, end = pool_cue.get_cue(Table)
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
      head, end = pool_cue.get_cue(Table)
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

def show_help():
   print('a. get next frame')
   print('b. set boundary (auto)')
   print('c. set boundary (click)')
   print('d. show table')
   print('e. start ball detection')
   print('f. start cue detection')
   print('g. start ball and cue detection')
   print('q. quit')

#----------------------------
#The main program begins here
#----------------------------
while next:
   next = Next_command()