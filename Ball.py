import math
import numpy as np

class Ball:
    width = 0
    height = 0
    radius = 0
     
    def __init__(self, id, pos = np.array([0,0]), heading = np.array([0,0])):
        self.id = id
        self.pos = pos
        #determine the end point
        self.heading = heading
        self.endpoint = self.cal_endpoint()
    
    def cal_endpoint(self):
        x = self.pos[0]
        y = self.pos[1]
        x_dir = self.heading[0]
        y_dir = self.heading[1]
        h = self.height
        w = self.width
        r = self.radius

        endpoint = self.pos
        x_bond = w-r if x_dir > 0 else r
        y_bond = h-r if y_dir > 0 else r
        #x_dir or y_dir is 0, but not both 
        if bool(x_dir) != bool(y_dir):
            if x_dir == 0:
                endpoint[1] = y_bond
            else:
                endpoint[0] = x_bond
        #x_dir and y_dir are not 0
        elif x_dir != 0 and y_dir != 0:
            tan = y_dir/x_dir
            x_new = x + (y_bond-y)/tan
            y_new = y + (x_bond-x)*tan

            if 0 <= x_new and x_new <= w: 
                endpoint = np.array([x_new, y_bond])
            else:
                endpoint = np.array([x_bond, y_new])
        return endpoint

    #after collision, pos will be the collision point, re-calculate the endpoints
    def collide(self, other):
        original_heading = (self.heading[0],self.heading[1])
        other.heading = ((((self.heading[0]*(self.pos[0]-other.pos[0]))+(self.heading[1]*(self.pos[1]-other.pos[1])))*(self.pos[0]-other.pos[0])/(self.dist(self.pos,other.pos)**2)),(((self.heading[0]*(self.pos[0]-other.pos[0]))+(self.heading[1]*(self.pos[1]-other.pos[1])))*(self.pos[1]-other.pos[1])/(self.dist(self.pos,other.pos)**2)))
        self.heading = ((self.heading[0] - ((self.heading[0]*(self.pos[0]-other.pos[0]))+(self.heading[1]*(self.pos[1]-other.pos[1])))*(self.pos[0]-other.pos[0])/(self.dist(self.pos,other.pos)**2)),(self.heading[1] - ((self.heading[0]*(self.pos[0]-other.pos[0]))+(self.heading[1]*(self.pos[1]-other.pos[1])))*(self.pos[1]-other.pos[1])/(self.dist(self.pos,other.pos)**2)))

        a = self.dist(self.pos,self.endpoint)**2
        b = 2*((self.pos[0]-other.pos[0])*(self.endpoint[0]-self.pos[0])+(self.pos[1]-other.pos[1])*(self.endpoint[1]-self.pos[1]))
        c = self.dist(self.pos,other.pos)**2-4*self.radius
        t = (-b+math.sqrt(b**2-4*a*c))/(2*a)
        self.pos = (self.pos[0]+t*original_heading[0],self.pos[1]+t*original_heading[1])
        self.endpoint = self.cal_endpoint()
        other.endpoint = other.cal_endpoint()

    #check distance from point to line using area
    #return the projection distance
    def check_collision(self, other, scale = 1):
        p1 = self.pos
        p2 = self.endpoint
        p3 = other.pos
        print('p1:',p1,'p2:',p2,'p3:',p3)
        distance = self.area(p1,p2,p3)/self.dist(p1,p2)
        if distance <= 2*self.radius*scale:
            return ((p3[0]-p1[0])*(p2[0]-p1[0])+(p3[1]-p1[1])*(p2[1]-p1[1]))/self.dist(p1,p2)
        else:
            return -1
    
    def area(self, p1, p2, p3):
        #return = p1[0]*p2[1]+p2[0]*p3[1]+p3[0]*p1[1]-p1[1]*p2[0]-p2[1]*p3[0]-p3[1]*p1[0]
        mat = np.ones([3, 3])
        mat[:, 1:] = np.array([p1, p2, p3]) 
        return abs(np.linalg.det(mat))
    
    def bounce(self):
        h = self.height
        w = self.width
        r = self.radius
        if self.pos[0] == r or self.pos[0] == w-r:
            self.heading[0] *= -1
        if self.pos[1] == r or self.pos[1] == h-r:
            self.heading[1] *= -1

        self.pos = self.endpoint 
        self.endpoint = self.cal_endpoint()

    def dist(self, p1, p2):
        return np.linalg.norm(p1-p2) 

if __name__=='__main__':

    Ball.width = 300
    Ball.height = 500
    Ball.radius = 12

    pos = np.array([100, 100])
    heading = np.array([-1, -1])
    b = Ball(0, pos=pos, heading=heading)

    print(b.endpoint)
