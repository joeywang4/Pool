import Ball
import json
import numpy as np

WIDTH = 1000
HEIGHT = 500
RADIUS = 12
CORNER_WIDTH = 20
balls = []  
ballList = [] 
lineList = []

def calc_run():
    calc_read()

    head = np.array([310,110])
    end = np.array([330,110])


    cue = Ball.Ball(-1, head, head-end)
    print('Tline21')
    calc_motion(cue)
    print('Tline23')

    calc_write()

def calc_read():
    global WIDTH, HEIGHT, RADIUS, CORNER_WIDTH, balls
    Ball.Ball.width = WIDTH 
    Ball.Ball.height = HEIGHT
    Ball.Ball.radius = RADIUS
    Ball.Ball.corner_width = CORNER_WIDTH
    for id in range(balls.shape[0]):
        ballList.append(Ball.Ball(id, balls[id][:2]))
        lineList.append({'id': id, 'lines': list(balls[id][:2])})

def calc_motion(ball):
    if len(lineList[ball.id]['lines']) == 4:
        return
    id = calc_check_collision(ball) 
    print('id',id,'ball',ballList[id].position)
    #collide
    if id != -1:
        ball.collide(ballList[id])
        lineList[ball.id]['lines'].append(ball.position)
        lineList[id]['lines'].append(ballList[id].position)

        calc_motion(ball)
        calc_motion(ballList[id])

    #bounce
    else:
        ball.bounce()

        lineList[ball.id]['lines'].append(ball.position)

        calc_motion(ball)

def calc_write():
    print(lineList)
    #json.dumps(lineList)

def calc_check_collision(ball):
    global balls
    nearest = -1, 10000
    for id in range(balls.shape[0]):
        if id == ball.id:
            continue
        #if more than one ball collides, need to compare distance of projection
        distance = ball.check_collision(ballList[id])
        if distance != -1 and distance < nearest[1]:
            nearest = id, distance
    return nearest[0]

def init(calBalls, wid, hig):
  global WIDTH, HEIGHT, RADIUS, CORNER_WIDTH, balls    
  WIDTH = wid
  HEIGHT = hig
  RADIUS = 13
  CORNER_WIDTH = 20
  balls = calBalls
  print('w',wid,'h',hig)
  calc_run()
