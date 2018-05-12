import math
import numpy as np

class ball:
    width = 0
    height = 0
    radius = 0
     
    def __init__(self, id, pos = np.array([0,0]), heading = np.array([0,0])):
        self.id = id
        self.pos = pos
        self.heading = heading
        # determine the end point
        self.endpoint = self.calc_endpoint()
    
    def calc_endpoint(self):
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
        # x_dir or y_dir is 0, but not both 
        if bool(x_dir) != bool(y_dir):
            if x_dir == 0:
                endpoint[1] = y_bond
            else:
                endpoint[0] = x_bond
        # both x_dir and y_dir are not 0
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
        p1 = self.pos
        p2 = self.endpoint
        p3 = other.pos
        r = self.radius
        # p4 is collision point of self
        v1 = p2-p1
        v2 = p3-p1
        # v3 = p4-p1 = t*v1
        # apply law of cosine: v3**2+v2**2-2*v1*v3 = 4r*2
        a = (v1**2).sum()
        b = -2*np.dot(v1, v2)
        c = (v2**2).sum() - 4*r**2
        t = (-b-math.sqrt(b**2-4*a*c))/(2*a)
        assert t > 0
        p4 = p1 + t*v1
        # the two new headings are orthogonal
        other.heading = p3-p4
        self.heading = np.array([-other.heading[1], other.heading[0]])
        if np.dot(self.heading, v1) < 0:
            self.heading *= -1
        self.endpoint = self.calc_endpoint()
        other.endpoint = other.calc_endpoint()
        print('b1:', self.heading)
        print('b2:', other.heading)
        

    #check distance from a point (ball's pos) to the line (vector of moving ball)
    #return the projection distance
    #return -1 if no collision
    def check_collision(self, other):
        p1 = self.pos
        p2 = self.endpoint
        p3 = other.pos
        r = self.radius
        print('p1:',p1,'p2:',p2,'p3:',p3)
        distance = self.dist_pt_line(p3, p1, p2) 
        print(distance)

        if distance < 2*r and np.dot(p3-p1, p2-p1) > 0:
            return self.projection(p1, p2, p3) 
        else:
            return -1
    
    def bounce(self):
        h = self.height
        w = self.width
        r = self.radius
        if self.endpoint[0] == r or self.endpoint[0] == w-r:
            self.heading[0] *= -1
        if self.endpoint[1] == r or self.endpoint[1] == h-r:
            self.heading[1] *= -1

        self.pos = self.endpoint 
        self.endpoint = self.calc_endpoint()

    # project common-p2 to common p1
    def projection(self, common, p1, p2):
        return np.dot(p1-common, p2-common)/self.dist(common ,p1)

    # dist of pt and line p1-p2
    def dist_pt_line(self, pt, p1, p2):
        return self.area(p1, p2, pt)/self.dist(p1, p2)

    def area(self, p1, p2, p3):
        #return = p1[0]*p2[1]+p2[0]*p3[1]+p3[0]*p1[1]-p1[1]*p2[0]-p2[1]*p3[0]-p3[1]*p1[0]
        mat = np.ones([3, 3])
        mat[:, 1:] = np.array([p1, p2, p3]) 
        return abs(np.linalg.det(mat))

    def dist(self, p1, p2):
        return np.linalg.norm(p1-p2) 

if __name__=='__main__':

    ball.width = 300
    ball.height = 500
    ball.radius = 12

    pos = np.array([100, 100])
    heading = np.array([-1, -1])
    b = ball(0, pos=pos, heading=heading)
    c = ball(1, pos=np.array([50, 60]))
    dist = b.check_collision(c)
    print(dist)
    if dist != -1:
        b.collide(c)
