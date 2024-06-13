# jetpac

import time,random

def readbmp(filename):
        # read a 24bit bmp
        
        spritebuffer = Buffer(128,128)
        # set buffer as target for gfx operations e.g. pixel()
        target(spritebuffer)
        
        def lebytes_to_int(bytes):
            n = 0x00
            while len(bytes) > 0:
                n <<= 8
                n |= bytes.pop()
            return int(n)

        f = open(filename, 'rb') 
        img_bytes = list(bytearray(f.read(26))) # just read header
        start_pos = lebytes_to_int(img_bytes[10:14])

        width = lebytes_to_int(img_bytes[18:22])
        height = lebytes_to_int(img_bytes[22:26])
        
        seektostart = f.read(start_pos - 26)
                             
        for x in range(height):
            colrow= list(bytearray(f.read(3 * width)))
            for y in range(width):       
                #col = lebytes_to_int(list(bytearray(f.read(3))))
                b,g,r = colrow[y*3:y*3+3]
                pen(r >> 4,g >> 4,b >> 4)
                pixel(y//2,(height - x) //2)
        f.close()
        
        # set gfx buffer back to screen
        target()
        return (spritebuffer)
    
class spriteobj:
    x = y = 0
    xdir = ydir = 0.5
    time = 0
    grabbed = 0
    
def collide (obj,x,y,xdistance):
    ydistance = 10
    if (abs(x - obj.x) < xdistance  and abs(y - obj.y) < ydistance) : return True
    else : return False

def hitplatform (platforms,x,y):
    for p in platforms:
            px,py,width = p
            if ( (x > px and (x-px) < width) and (abs(py - y - 4) < 4)) : return True
    return False

# initialize
spritebuffer = readbmp ("jetpac.bmp")

SCREENX = 120
x = y = 90
xdir = ydir = 1
    
splat = spriteobj()
fuel = spriteobj()
fuel.x = 50
    
aliens = [spriteobj() for i in range(4)]
for alien in aliens :
    alien.x = random.randrange(SCREENX)
    alien.y = random.randrange(SCREENX)
    
platforms = [(16,45,20), (45,75,20), (86,26,30), (-10,118,125)]

def update (ticks) :
    global x,y,xdir,ydir

    if (button(LEFT)): xdir -= 1
    if (button(RIGHT)): xdir += 1
    if (button(X) or button(UP)): ydir -= 1   
    
     # not too fast
    if (abs(xdir) > 5): xdir *= 0.5
    xdir *= 0.9
    # keep on screen
    if (x < 0 ): x = 120
    if (x > SCREENX) : x = 0
    if (y > 110): y = 110
    if (y < 0) :
        y = 10
        ydir = 0
        
    x += xdir 
    y += ydir
        
    # gravity
    ydir += 0.4
    
def draw (ticks) :
        global x,y,xdir,ydir
        
        pen(0,0,0)
        clear()   

        fuel.y += fuel.ydir
        if (fuel.ydir > 0) : fuel.ydir += 0.05
        
        if (hitplatform(platforms,fuel.x,fuel.y)) :
            fuel.ydir = 0
        if (hitplatform(platforms,x,y)):
                if (ydir > 0) : ydir = 0
                #else : ydir = 3 #bounce underneath
                
        #laser
        if (button(A)) : firing  = 1
        else : firing = 0
    
        if firing:
            pen(15,15,15)
            for laser in range(5,50):
                if (xdir > 1) : laser *= -1;
                if (random.random() > 0.5) : pixel(int(x) - laser,int(y))
        
        #aliens
        for alien in aliens :
            alien.x += alien.xdir
            alien.y += alien.ydir
            dead = 0
            if (alien.x > SCREENX or alien.x < -25) : dead = 1
            if (hitplatform(platforms,alien.x,alien.y)) : dead = 1
            if (firing and collide(alien,x,y,50)) : dead = 1
            # player collides with alien
            if (collide(alien,x,y,10)) :
                xdir = alien.xdir * 2
                ydir = -1
                dead = 1
            if (dead) :
                    splat.x = alien.x
                    splat.y = alien.y
                    splat.time = 5
                    
                    alien.xdir = 1 + random.randrange(2)
                    alien.y = random.randrange(100)
                    if (random.randrange(5) > 1) :
                        alien.x = -10
                    else :
                        alien.x = 120
                        alien.xdir = alien.xdir * -1      
            blit(spritebuffer,0,25,8,8,int(alien.x),int(alien.y))
            
        #explosions stay on screen for 5 frames    
        if (splat.time  > 0) :
            splat.time -= 1
            blit(spritebuffer,35,0,8,8,int(splat.x),int(splat.y),0)
        
        # fuel grabbing and dropping
        if (not fuel.grabbed and collide(fuel,x,y,10)) : fuel.grabbed = 1
        if (fuel.grabbed) :
                fuel.x = x
                fuel.y = y + 8
                fuel.ydir = 1
                dropzone = 80
                if (abs(fuel.x - dropzone) < 5) : fuel.grabbed = 0
        if (fuel.y > 120) :
            fuel.x = 100
            fuel.y = 0
            fuel.ydir = 1
        blit(spritebuffer,20,32,10,32,80,90)
        blit(spritebuffer,54,50,12,12,int(fuel.x),int(fuel.y))
        
        # jetman
        if (xdir > 0) : mirror = HFLIP
        else : mirror = 0
        blit(spritebuffer,0,0,8,12,int(x),int(y)-5,8,12,mirror)
        
        # platforms
        for p in platforms:
            px,py,width = p
            pen(0,15,0) # green
            line(px, py, px +width ,py)
        flip()
start()