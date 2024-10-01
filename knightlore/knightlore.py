# knightlore - isometric game

import time,random
from readbmp import *

class spriteobj:
    x = y = 20
    xdir = ydir = 0.5
    time = grabbed = 0
    img = [0,0]
    w = h = 32

def blitsprite (spritesheet,sprite,mirror = 0):
     offset = 0
     if sprite.h > 8 : offset = 8  - sprite.h
     blit(spritesheet,sprite.img[0],sprite.img[1],sprite.w,sprite.h,int(sprite.x),int(sprite.y) + offset,sprite.w,sprite.h,mirror)
    
# initialize
spritebuffer = readbmp ("sabreman.bmp")

screensize = 120
ground = 110
sabreman = spriteobj()
sabreman.img = [0,32]
sabreman.w = 23

man = 0
def update (ticks) :
    global firing,wolf,man
    
    
    if (button(A)) : firing  = 1
    else : firing = 0
    
    if (button(Y)) : man = 65 - man
    
    wolfimg = 64
    
    if (button(DOWN)):
        sabreman.img[1] = man + 32 #facing front
        sabreman.xdir -= 1
        sabreman.ydir += 1
    if (button(RIGHT)):
        sabreman.img[1] = man + 32  # facing front
        sabreman.xdir += 1
        sabreman.ydir += 1
        
    if (button(UP)):
        sabreman.img[1] = man # facing away
        sabreman.ydir -= 1
        sabreman.xdir += 1
    if (button(LEFT)):
        sabreman.img[1] = man # facing away
        sabreman.xdir -= 1
        sabreman.ydir -= 1
    
    sabreman.xdir *= 0.7
    sabreman.ydir *= 0.7
    # keep on screen / wrap left/right
    sabreman.y = min(ground,sabreman.y)
    if (sabreman.x < 0 or sabreman.x > screensize) : sabreman.x = screensize - sabreman.x
    sabreman.y = max(0,sabreman.y)
        
    sabreman.x += sabreman.xdir 
    sabreman.y += sabreman.ydir
  
    if (abs(sabreman.xdir) > 0.5) : ## walking
        frame = sabreman.img[0]
        if frame < 100 : frame += 24
        else : frame = 0
        sabreman.img[0] = frame

def draw (ticks) :
        pen(0,0,0)
        clear()   
        
        # sabreman
        mirror = 0
        if (sabreman.xdir < 0 and sabreman.ydir > 0) : mirror = HFLIP
        if (sabreman.xdir > 0 and sabreman.ydir < 0) : mirror = HFLIP
        #else : mirror = 0
        blitsprite(spritebuffer,sabreman,mirror)
        
        flip()
start()
