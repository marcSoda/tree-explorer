import random
import pygame as pg
from Branch import Branch

screenHeight = 1000 #smaller = better performance
screenWidth = 1900 #smaller = better performance
screenColor = (0,0,0) # RGB black (must be a len 3 tuple)
frameRate = 60 #smaller = better performance
scrollRate = 3 #pixels per frame movement using wasd
zoomFactor = .01 #how quickly the screen "zooms in"
minLength = 10 #minimum branch length (the higher the value, the better the performance, but the worse the quality
angle = 120 #angle of each branch to its root branch
lineThickness = 2 #thickness of the branch
branches = [] #dynamic array of all branch objects

rootColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) #random initial color
root = Branch([screenWidth/2, screenHeight], [screenWidth/2, screenHeight / 1.6], 0, rootColor) #first branch
branches.append(root) #add the first branch to the array. branches are grown from this root branch

def branchEngine(): #manipulate all branches every frame
    for branch in branches: #for every branch
        if not branch.drawn:  #only append branches that are not in the list AND
            if not branch.getLength() < minLength:  # only append branches that are greater than 1 px long
                newBranches = branch.getBranches(angle) #returns two child branches
                branches.append(newBranches[0]) #add left child
                branches.append(newBranches[1]) #add right child
                branch.drawn = True #keeps same branch from being drawn every frame
        if ((branch.start[0] > screenWidth and branch.end[0] > screenWidth) #edge detection
                or (branch.start[0] < 0 and branch.end[0] < 0) #edge detection
                or (branch.start[1] > screenHeight and branch.end[1] > screenHeight) #edge detection
                or (branch.start[1] < 50 and branch.end[1] < 0)): #edge detection
            # TODO dynamic panning
            branches.remove(branch) #dont keep track of offscreen branches anymore. performance boost
        pg.draw.line(screen, branch.color, branch.start, branch.end, lineThickness)  # draw branches
        branch.zoom(zoomFactor, screenWidth, screenHeight) #zoom in

def checkKeyPress(): #keypresses
    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        for branch in branches:
            branch.move([0,scrollRate])
    if keys[pg.K_s]:
        for branch in branches:
            branch.move([0,-scrollRate])
    if keys[pg.K_a]:
        for branch in branches:
            branch.move([scrollRate,0])
    if keys[pg.K_d]:
        for branch in branches:
            branch.move([-scrollRate,0])

pg.init()  # initialize pygame
pg.event.set_allowed([pg.QUIT, pg.KEYDOWN]) #only check for quit and keydown events. improves performance
screen = pg.display.set_mode((screenWidth, screenHeight))  # set screensize
pg.display.set_caption('Fractal Tree Explorer') #title bar
clock = pg.time.Clock()  # for framerate
complete = False  # when true, game ends

while not complete: #things in this loop happen every frame
    for event in pg.event.get():  # if 'x' is pressed, exit
        if event.type == pg.QUIT:
            complete = True
    clock.tick(frameRate)  # for framerate
    screen.fill(screenColor) #set screen color
    branchEngine() #keep track of branches
    checkKeyPress() #duh
    pg.display.update() #update
pg.quit() #duh
