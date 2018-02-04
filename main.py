import pool_size
import pool_ball
import pool_util
import pool_set_bound
import cv2 as cv
import numpy as np

name = '/home/joey/py/opencv/camera/17.png'
Img, Table, refPt = None, None, None
next = True

def Next_command():
   command = input("> ")
   if command == 'help':
      show_help()
   elif command == 'a':
      get_img()
   elif command == 'b':
      get_table(False)
   elif command == 'c':
      get_table(True)
   elif command == 'd':
      show_table()
   elif command == 'e':
      show_balls()
   elif command == 'q':
      return False
   else:
      print('Error command! Use "help" to show commands.')
   
   return True   

def get_img():
   global Img
   Img = cv.imread(name)

def get_table(click):
   global refPt
   global Table
   if click:
      refPt = pool_set_bound.set_bound(Img)
   else:
      refPt = pool_size.get_boundary(Img)
   Table = pool_util.get_table(refPt, Img)
   return True

def show_table():
   cv.imshow('table', Table)
   print('Press any key to continue...')
   cv.waitKey(0)
   cv.destroyAllWindows()

def show_balls():
   balls = pool_ball.get_ball(Table)
   print('Press any key to continue...')
   pool_util.draw_ball(balls, Table)

def show_help():
   print('a. get next frame')
   print('b. set boundary (auto)')
   print('c. set boundary (click)')
   print('d. show table')
   print('e. show balls')
   print('q. quit')

#----------------------------
#The main program begins here
#----------------------------
while next:
   next = Next_command()