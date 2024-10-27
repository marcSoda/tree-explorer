import math
import numpy as np
import random

colorStepSize = 30
newBranchScale = .67

class Branch:
    def __init__(self, start, end, angle, rootColor):
        self.start = start[:] #create copy eliminates pass by reference issue
        self.end = end[:] #create copy eliminates pass by reference issue
        self.angle = angle #angle of branch
        self.drawn = False #performance booster
        self.color = self.colorStep(rootColor) #each child has slightly difference color

        self.distFromStart = 0
        self.grown = False
        self.tempEnd = [start[0], start[1]]

    def getBranches(self, angle): #return two child branches
        return Branch(self.end, self.rotate(angle), self.angle + angle, self.color), \
               Branch(self.end, self.rotate(-angle), self.angle - angle, self.color)

    def rotate(self, angle): #return x and y of child endpoint
        length = newBranchScale * self.getLength()
        newX = self.end[0] + (length * np.sin(np.deg2rad(self.angle + angle)))
        newY = self.end[1] - (length * np.cos(np.deg2rad(self.angle + angle)))
        return [newX, newY]

    def move(self, vector): #takes a movement vector. not sure why I did it like this. overcomplicated
        self.start[0] += vector[0]
        self.start[1] += vector[1]
        self.end[0] += vector[0]
        self.end[1] += vector[1]

    def zoom(self, factor, width, height): #"zoom" each branch. it's not actually zooming, dialate each branch about screen center
        self.start[0] += (self.start[0] - width/2) * factor
        self.start[1] += (self.start[1] - height/2) * factor
        self.end[0] += (self.end[0] - width/2) * factor
        self.end[1] += (self.end[1] - height/2) * factor

    def getLength(self): #its just the distance formula (between start and end)
        return math.sqrt(((self.end[0]-self.start[0])**2)+((self.end[1]-self.start[1])**2))

    #todo fix this retarded ass algorithm lazy
    def colorStep(self, rootColor): #slightly change the color of each branch. fix this later its retarded
        rand1 = random.randint(0,2)
        rand2 = random.randint(0,1)
        r,g,b = rootColor
        c = [r,g,b]
        if rand2 == 1:
            if c[rand1] <= 255 - colorStepSize:
                c[rand1] += colorStepSize
        elif rand2 == 0:
            if c[rand1] >= colorStepSize:
                c[rand1] -= colorStepSize
        return(c[0],c[1],c[2])
