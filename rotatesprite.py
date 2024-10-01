import os, math, time
from readbmp import *

def rotatesprite (buffer,xpos,ypos,rot,q=2):
    height = width = 64
    rotatedsprite = Buffer(int(width*1.5),int(height*1.5))
    target(rotatedsprite)
    blitrotate (buffer,xpos,ypos,rot,q)
    target()
    return (rotatedsprite)

def blitrotate (buffer,xpos,ypos,rot,q=2):
    height = width = 64
    sinangle = math.sin(rot)
    cosangle = math.cos(rot)
    h2 = height / 2
    w2 = width / 2
    for x in range(0,width,q):
        for y in range(0,height,q):
            x1 = x - w2
            y1 = y - h2
            rotx = x1 * sinangle + y1 * cosangle
            roty = y1 * sinangle - x1 * cosangle
            
            blit(buffer,x,y,q,q,xpos + int(rotx),ypos + int(roty))

def update(tick) :
        global x,y,angle
        
        if (button(LEFT)) : x -= 1
        if (button(RIGHT)) : x += 1
        
        if (button(UP)) : y -= 1
        if (button(DOWN)) : y += 1
        
        angle += 0.05

angle = 0
def draw(tick) :
    
        global angle,x,y,rot
        pen(0,0,0)
        clear()
    
        pen (15,15,15)
        start = time.ticks_ms()
        
        # create a new rotated sprite then blit it to screen
        #sprite = rotatesprite(buffer,x,y,angle,2) # 68ms / 14 fps
        #blit(sprite,0,0,96,96,0,0)
        
        # directly blit while rotating
        blitrotate(buffer,x,y,angle,2) # 61ms / 16 fps
        
     
        timetaken = time.ticks_ms() - start
        print (timetaken, "ms", (1000 // timetaken), "fps")
        flip()

x = y = rot = 50
texWidth = 64
buffer = readbmp("crate.bmp")
start()
