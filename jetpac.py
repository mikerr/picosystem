# jetpac

import time,random
from readbmp import *

class spriteobj:
    x = y = 0
    xdir = ydir = 0.5
    time = grabbed = 0
    img = [0,0]
    w = h = 8
    
def collide (obj,sprite,xdistance):
    ydistance = 10
    if (abs(sprite.x - obj.x) < xdistance  and abs(sprite.y - obj.y) < ydistance) : return True
    else : return False

def hitplatform (platforms,sprite):
    for p in platforms:
            px,py,width = p
            if ( (sprite.x > px and (sprite.x-px) < width) and (abs(py - sprite.y - 4) < 4)) : return True
    return False

def blitsprite (spritesheet,sprite,mirror = 0):
     offset = 0
     if sprite.h > 8 : offset = 8  - sprite.h
     blit(spritesheet,sprite.img[0],sprite.img[1],sprite.w,sprite.h,int(sprite.x),int(sprite.y) + offset,sprite.w,sprite.h,mirror)
    
# initialize
spritebuffer = readbmp ("jetpac.bmp")

screensize = 120
ground = 110
jetman = spriteobj()
jetman.img = [18,13]
jetman.h = 12

rocket = spriteobj()
rocket.img = [20,32]
rocket.h = 32
rocket.x = 70

splat = spriteobj()
splat.img = [35,0]

fuel = spriteobj()
fuel.x = 50
fuel.img = [53,50]
fuel.w = 11

gem = spriteobj()
gem.img = [53,0]
gem.w = 10

fuelled = takeoff = firing = 0

aliens = [spriteobj() for i in range(4)]
for alien in aliens :
    alien.x = random.randrange(screensize)
    alien.y = random.randrange(screensize)
    alien.img = [0,25] 
    
platforms = [(16,45,20), (45,75,20), (86,26,30), (-10,118,130)]

def update (ticks) :
    global firing,takeoff,fuelled
    
    if (button(A)) : firing  = 1
    else : firing = 0
        
    if (button(LEFT)):  jetman.xdir -= 1
    if (button(RIGHT)): jetman.xdir += 1
    if (button(X) or button(UP)): jetman.ydir -= 1   
    
     # not too fast
    if (abs(jetman.xdir) > 5): jetman.xdir *= 0.5
    if (abs(jetman.ydir) > 5): jetman.ydir *= 0.9
    jetman.xdir *= 0.8
    # keep on screen / wrap left/right
    jetman.y = min(ground,jetman.y)
    jetman.y = max(0,jetman.y)
    if (jetman.x < 0 or jetman.x > screensize) : jetman.x = screensize - jetman.x
     
    jetman.x += jetman.xdir 
    jetman.y += jetman.ydir
        
    # gravity
    jetman.ydir += 0.4
    
    if (hitplatform(platforms,jetman)):
                if (jetman.ydir > 0) :
                    jetman.y -= 1
                    jetman.ydir = 0
                else :
                    jetman.ydir = - jetman.ydir #bounce underneath
                jetman.img = [8* (int(jetman.x) % 4),0] #walking
    if (abs(jetman.ydir) > 1) : jetman.img = [18,13]  # flying
        
    if collide(gem,jetman,10):
            gem.img[1] = 10 * random.randrange(4) # gems at 0,10,20,30,40
            gem.x = random.randrange(screensize)
            gem.y = -100
            gem.ydir = 2
    gem.y += gem.ydir        
    fuel.y += fuel.ydir
    if (fuel.ydir > 0) : fuel.ydir += 0.02
    if (hitplatform(platforms,gem)) : gem.ydir = 0
    if (hitplatform(platforms,fuel)) : fuel.ydir = 0    

    # fuel grabbing and dropping
    dropzone = 70
    if (not fuel.grabbed and collide(fuel,jetman,10)) : fuel.grabbed = 1
    if (fuel.grabbed) :
                fuel.x = jetman.x
                fuel.y = jetman.y + 8
                fuel.ydir = 1
                if (abs(fuel.x - dropzone) < 5) :
                    fuel.grabbed = 0
                    fuel.x = dropzone
    if (fuel.x == dropzone and fuel.y > 110) :
            fuelled += 1
            fuel.x = random.randrange(screensize)
            fuel.y = -50
            fuel.ydir = 1
    # rocket
    rocket.y = ground - takeoff + 6
    if (fuelled >= 3) :
                takeoff += 1
                if (takeoff > 100) :
                    takeoff = fuelled = 0
                    rocket.img[0] +=8
                    if (rocket.img[0] > 45): rocket.img[0] = 20
    #aliens
    for alien in aliens :
            alien.x += alien.xdir
            alien.y += alien.ydir
            dead = 0
            if (alien.x > screensize or alien.x < -25) : dead = 1
            if (hitplatform(platforms,alien)) : dead = 1
            if (firing and collide(alien,jetman,50)) : dead = 1
            # player collides with alien
            if (collide(alien,jetman,10)) :
                jetman.xdir = alien.xdir * 2
                jetman.ydir = -1
                dead = 1
            if (dead) :
                    splat.x = alien.x
                    splat.y = alien.y
                    splat.time = 5
                    
                    alien.xdir = 1 + random.randrange(2)
                    alien.y = random.randrange(screensize)
                    if (random.randrange(5) > 1) :
                        alien.x = -10
                    else :
                        alien.x = 120
                        alien.xdir = alien.xdir * -1
                    
def draw (ticks) :
        global fuelled,takeoff

        pen(0,0,0)
        clear()   
        blitsprite(spritebuffer,gem)    
        #laser
        if firing:
            pen(15,15,15)
            for laser in range(5,50):
                if (jetman.xdir > 0) : laser *= -1;
                if (random.random() > 0.5) : pixel(int(jetman.x) - laser,int(jetman.y))
        for alien in aliens :
            if (alien.xdir < 0) : mirror = HFLIP
            else : mirror = 0
            blitsprite(spritebuffer,alien,mirror)
        #explosions stay on screen for 5 frames    
        if (splat.time  > 0) :
            splat.time -= 1
            blitsprite(spritebuffer,splat) 
        # rocket
        blitsprite(spritebuffer,rocket)
        if (fuelled < 3) :    
            for f in range(fuelled) :
                blit(spritebuffer,54,50,12,8,70,ground - (f * 8))
        blitsprite(spritebuffer,fuel)     
        # jetman
        if (jetman.xdir > 0) : mirror = HFLIP
        else : mirror = 0
        blitsprite(spritebuffer,jetman,mirror)
        # platforms    
        pen(0,15,0) # green
        for p in platforms:
            px,py,width = p
            hline(px, py, width)
        flip()
start()
