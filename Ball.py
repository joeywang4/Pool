import math
import numpy as np

class Ball:
    width = 582.0
    height = 303.0
    radius = 12.0
    
    def __init__(self, id, position = np.array([0,0]), heading = np.array([0,0])):
        self.id = id
        self.position = position[:2]
        #determine the end point
        self.heading = heading[:2]
        self.endpoint = self.cal_endpoint()
    
    def cal_endpoint(self):
        
        if self.heading[0] == 0:
            if self.heading[1] == 0:
                return self.position
            elif self.heading[1] > 0:
                return (self.position[0],self.height)
            elif self.heading[1] < 0:
                return (self.position[0],0.0)
    
        elif self.heading[0] > 0:
            if self.heading[1] == 0:
                return (self.width,self.position[1])
            elif self.heading[1] > 0:
                if (self.width-self.position[0])/self.heading[0] > (self.height-self.position[1])/self.heading[1]:
                    return (self.position[0]+(self.heading[0])*((self.height-self.position[1])/self.heading[1]),self.height)
                elif (self.width-self.position[0])/self.heading[0] < (self.height-self.position[1])/self.heading[1]:
                    return (self.width,self.position[1]+(self.heading[1])*((self.width-self.position[0])/self.heading[0]))
                else:
                    return (self.width,self.height)
            else:
                if (self.width-self.position[0])/self.heading[0] > self.position[1]/(-self.heading[1]):
                    return (self.position[0]+(self.heading[0])*(self.position[1]/(-self.heading[1])),0.0)
                elif (self.width-self.position[0])/self.heading[0] < self.position[1]/(-self.heading[1]):
                    return (self.width,self.position[1]+(self.heading[1])*((self.width-self.position[0])/self.heading[0]))
                else:
                    return (self.width,0.0)


        elif self.heading[0] < 0:
            if self.heading[1] == 0:
                return (0.0,self.position[1])
            elif self.heading[1] > 0:
                if (self.position[0])/(-self.heading[0]) > (self.height-self.position[1])/self.heading[1]:
                    return (self.position[0]+(self.heading[0])*((self.height-self.position[1])/self.heading[1]),self.height)
                elif (self.position[0])/(-self.heading[0]) < (self.height-self.position[1])/self.heading[1]:
                    return (0.0,self.position[1]+(self.heading[1])*((self.position[0])/(-self.heading[0])))
                else:
                    return (0.0,self.height)
            else:
                if (self.position[0])/(-self.heading[0]) > self.position[1]/(-self.heading[1]):
                    return (self.position[0]+(self.heading[0])*(self.position[1]/(-self.heading[1])),0.0)
                elif (self.position[0])/(-self.heading[0]) < self.position[1]/(-self.heading[1]):
                    return (0.0,self.position[1]+(self.heading[1])*((self.position[0])/(-self.heading[0])))
                else:
                    return (0.0,0.0)



    #after collision, position will be the collision point, re-calculate the endpoints
    def collide(self, other):
        original_heading = (self.heading[0],self.heading[1])
        other.heading = ((((self.heading[0]*(self.position[0]-other.position[0]))+(self.heading[1]*(self.position[1]-other.position[1])))*(self.position[0]-other.position[0])/(self.dist(self.position,other.position)**2)),(((self.heading[0]*(self.position[0]-other.position[0]))+(self.heading[1]*(self.position[1]-other.position[1])))*(self.position[1]-other.position[1])/(self.dist(self.position,other.position)**2)))
        self.heading = ((self.heading[0] - ((self.heading[0]*(self.position[0]-other.position[0]))+(self.heading[1]*(self.position[1]-other.position[1])))*(self.position[0]-other.position[0])/(self.dist(self.position,other.position)**2)),(self.heading[1] - ((self.heading[0]*(self.position[0]-other.position[0]))+(self.heading[1]*(self.position[1]-other.position[1])))*(self.position[1]-other.position[1])/(self.dist(self.position,other.position)**2)))

        a = self.dist(self.position,self.endpoint)**2
        b = 2*((self.position[0]-other.position[0])*(self.endpoint[0]-self.position[0])+(self.position[1]-other.position[1])*(self.endpoint[1]-self.position[1]))
        c = self.dist(self.position,other.position)**2-4*self.radius
        t = (-b+math.sqrt(b**2-4*a*c))/(2*a)
        self.position = (self.position[0]+t*original_heading[0],self.position[1]+t*original_heading[1])
        self.endpoint = self.cal_endpoint()
        other.endpoint = other.cal_endpoint()

    #check distance from point to line using area
    #return the projection distance
    def checkCollision(self, other, scale = 1):
        p1 = self.position
        p2 = self.endpoint
        p3 = other.position
        print('p1:',p1,'p2:',p2,'p3:',p3)
        distance = self.area(p1,p2,p3)/self.dist(p1,p2)
        if distance <= 2*self.radius*scale:
            return ((p3[0]-p1[0])*(p2[0]-p1[0])+(p3[1]-p1[1])*(p2[1]-p1[1]))/self.dist(p1,p2)
        else:
            return -1
    
    def area(self,p1=(0,0),p2=(0,0),p3=(0,0)):
        return abs(p1[0]*p2[1]+p2[0]*p3[1]+p3[0]*p1[1]-p1[0]*p3[1]-p2[0]*p1[1]-p3[0]*p2[1])
    
    def bounce(self):
        if self.endpoint[0] == 0 :
            self.position = (self.radius,self.endpoint[1]-self.radius*(self.heading[1])/(-self.heading[0]))
            self.heading = (-self.heading[0],self.heading[1])

        elif self.endpoint[0] == self.width :
            self.position = (self.width-self.radius,self.endpoint[1]-self.radius*self.heading[1]/self.heading[0])
            self.heading = (-self.heading[0],self.heading[1])
            
        elif self.endpoint[1] == 0 :
            self.position = (self.endpoint[0]-self.radius*self.heading[0]/(-self.heading[1]),self.radius)
            self.heading = (self.heading[0],-self.heading[1])

        elif self.endpoint[1] == self.height :
            self.position = (self.endpoint[0]-self.radius*self.heading[0]/self.heading[1],self.height-self.radius)
            self.heading = (self.heading[0],-self.heading[1])
            
        self.endpoint = self.cal_endpoint()

    def dist(self, p1 = (0,0), p2 = (0,0)):
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
