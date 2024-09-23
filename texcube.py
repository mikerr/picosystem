import os, math, time
from readbmp import *

def rot3d (point,rotate) :
    x,y,z = point
    rx,ry,rz = rotate
            
    # about z axis 
    nX = (math.cos(rz) * x) - (math.sin(rz) * y)
    nY = (math.sin(rz) * x) + (math.cos(rz) * y)
    x = nX 
    y = nY

    # about x axis 
    nZ = (math.cos(rx) * z) - (math.sin(rx) * y)
    nY = (math.sin(rx) * z) + (math.cos(rx) * y)
    z = nZ

    # about y axis 
    nX = (math.cos(ry) * x) - (math.sin(ry) * z)
    nZ = (math.sin(ry) * x) + (math.cos(ry) * z)

    return ([nX,nY,nZ])

def normal (triangle) :
    t1,t2,t3 = triangle
    
    x1,y1,z1 = t1
    x2,y2,z2 = t2
    x3,y3,z3 = t3
    
    #A = t2 - t1
    A = (x2-x1, y2-y1, z2-z1)
    
    #B = t3 - t1
    B = (x3-x1, y3-y1, z3-z1)
    
    # A cross product B
    Ax,Ay,Az = A
    Bx,By,Bz = B
    
    Nx = Ay * Bz - Az * By
    Ny = Az * Bx - Ax * Bz
    Nz = Ax * By - Ay * Bx
    
    return ((Nx,Ny,Nz))

def dotproduct(A,B):
     ax,ay,az = A
     bx,by,bz = B
     return ( ax * bx + ay * by + az * bz)

def to2d(xyz):
    x,y,z = xyz
    z = z - 400
    x = x * 1000  / z
    y = y * 1000  / z
    return [60 + int(x),60 + int(y)]

def line2 (xy,xy2):
    x,y = xy
    x2,y2 = xy2
    line(x,y,x2,y2)

def getlinepoints (p1,p2) :
    p1x,p1y = p1
    p2x,p2y = p2
    
    dx = (abs(p2x - p1x))
    dy = -(abs(p2y - p1y))
    
    step = 1
    sx = sy = step
    if (p1x > p2x) : sx *= -1
    if (p1y > p2y) : sy *= -1
    
    err = dx + dy;

    linepoints = []
    p = p1
    px,py = p
    while (True) :
        
        linepoints.append(p)
        if (abs(px - p2x) < step and abs(py - p2y) < step) : break
        
        e2 = err * 2
        if (e2 > dy) : err += dy; px += sx 
        if (e2 < dx) : err += dx; py += sy 
        
        p = [int(px),int(py)]
    return (linepoints)

def texline ( p1, p2, y) :
    linepoints = getlinepoints (p1,p2)
    #scale non-repeating texture to face width
    linelen = len(linepoints)
    if linelen == 0 : return
    step = texWidth / linelen
    x = 0
    for p in linepoints :
        px,py = p
        blit(buffer,int(x),int(y),2,2,px,py)
        x += step
    
def texquad( t1, t2, t3, t4) :
    sideApoints = getlinepoints (t2,t1)
    sideBpoints = getlinepoints (t3,t4)
    sblen = len(sideBpoints)
    if (sblen == 0) : return
    step = texWidth / sblen
    sb = y = 0
    for p in sideApoints :
        p1 = sideBpoints[sb]
        texline(p,p1,y)
        sb += 1
        if sb >= sblen : break
        y += step
   
points = []
faces = []
def init() :
        global points, faces 
        #cube points
        points = [
            [ 10,  10,  10],
             [-10,  10,  10],
             [-10, -10,  10],
             [ 10, -10,  10],
             [ 10,  10, -10],
             [-10,  10, -10],
             [-10, -10, -10],
             [ 10, -10, -10]]
        # cube faces
        # (triangles)
        faces = [
            [0, 1, 2],
            [0, 2, 3],
            [4, 0, 3],
            [4, 3, 7],
            [5, 4, 7],
            [5, 7, 6],
            [1, 5, 6],
            [1, 6, 2],
            [4, 5, 1],
            [4, 1, 0],
            [2, 6, 7],
            [2, 7, 3]]
         
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

        i = 0
        for face in faces:
            triangle = []
            for pointindex in face:
                point3 = points[pointindex]
                rotated3 = rot3d(point3,[0,angle,angle])
                triangle.append (rotated3)
            
            # find normal of triangle 
            n = normal(triangle)
            camera = (0,0,10)
            d = dotproduct(n,camera)
            
            #hidden surface removal
            #only draw if facing camera
            if (d > 0) : continue
            
            t1,t2,t3 = triangle
            t1 = to2d(t1)
            t2 = to2d(t2)
            t3 = to2d(t3)
            
            if (i % 2) : #quad
                texquad(t2,oldt2,t1,t3)
                #poly(tuple(t2),tuple(oldt2),tuple(t1),tuple(t3))
            oldt2 = t2            
            i += 1
        timetaken = time.ticks_ms() - start
        print (timetaken, "ms", (1000 // timetaken), "fps")
        flip()
init()
x = y = rot = 60
texWidth = 64
buffer = readbmp("crate.bmp")
start()
