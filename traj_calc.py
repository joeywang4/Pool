from Ball import *
import json
import numpy as np

def init_balls(balls):
    global width, height, radius, corner_wid, ballList, lineList
    Ball.width = width 
    Ball.height = height
    Ball.radius = radius
    Ball.corner_wid = corner_wid
    for id in range(len(balls)):
        ballList.append(Ball(id, balls[id][:2]))
        lineList.append({'id': id, 'lines': [list(balls[id][:2])]})

def init_cue(cue):
    global radius, ballList
    head = cue[0] 
    tail = cue[1]
    end = 2*head - tail
    nearest = {'id': -1, 'dist': 1000} 

    for id in range(len(ballList)):
        pos = ballList[id].pos
        if dist_pt_line(pos, head, end) < radius and \
                np.dot(pos-head, end-head) > 0:
            dist = projection(head, end, pos)
            if dist < nearest['dist']:
                nearest['id'] = id 
                nearest['dist'] = dist
    print('first_ball:', nearest['id'], 'dist:', nearest['dist'])
    ballList[nearest['id']].set_heading(head-tail)
    return nearest['id']

def move(ball):
    global ballList, lineList
    if len(lineList[ball.id]['lines']) == 4:
        return
    c_id = check_collision(ball) 
    # collide
    if c_id != -1:
        c_ball = ballList[c_id]
        ball.collide(c_ball)
        print(ball.id, 'colide', c_id, ball.pos.round(), c_ball.pos.round())
        lineList[ball.id]['lines'].append(list(ball.pos.round().astype('int16')))

        move(c_ball)
        move(ball)

    # bounce
    else:
        ball.bounce()
        print(ball.id, 'bounce', ball.pos.round())
        lineList[ball.id]['lines'].append(list(ball.pos.round().astype('int16')))
        move(ball)

def check_collision(ball):
    global ballList, lineList
    nearest = {'id': -1, 'dist': 1000} 
    for id in range(len(ballList)):
        if id == ball.id or len(lineList[id]['lines']) > 1:
            continue
        #if more than one ball collides, need to compare distance of projection
        dist = ball.check_collision(ballList[id])
        if dist != 0 and dist < nearest['dist']:
            nearest['id'] = id 
            nearest['dist'] = dist
    return nearest['id']

def write():
    global lineList
    print(lineList)
    #json.dumps(lineList)

def init(calballs, cue, wid, hig):
    global width, height, radius, corner_wid, ballList, lineList
    width = wid
    height = hig
    radius = 13
    corner_wid = 20
    ballList = [] 
    lineList = []

    print('width:',wid,'height:',hig)
    init_balls(calballs)
    first_id = init_cue(cue)
    if first_id == -1:
        return None
    print('-------start-------')
    move(ballList[first_id])
    print('-------result-------')
    return lineList

if __name__=='__main__':
    calballs = np.array([[180, 185], [210, 50], [120, 420], [250, 300], [80, 75]])
    print('balls:\n', calballs)
    cue = np.array([[200, 200], [220, 220]])
    print('cue:\n', cue) 
    init(calballs, cue, 300, 500) 
    write()
