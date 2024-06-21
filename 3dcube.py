# 3dcube - wireframe, solid and shaded
import os, math, time

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

    return ((nX,nY,nZ))
        
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
    z = z - 250
    x = x * 500  / z
    y = y * 500  / z
    return ((60 + int(x),60 + int(y)))

mode = angle = 0
facecolors= []
points = []
faces = []
def init() :
        global points, faces, facecolors 
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
        facecolors = [
            [15,0,0], # red
            [15,0,0],
            [0,15,0], # green
            [0,15,0],
            [0,0,15], # blue
            [0,0,15],
            [15,15,0], # yellow
            [15,15,0],
            [0,15,15], # cyan
            [0,15,15],
            [15,0,15], # magenta
            [15,0,15]
            ]
         
def update(tick) :
        global angle,mode
        if (tick % 50 == 0) :
            mode += 1
            if mode > 2 : mode = 0
        angle += 0.1
        
def draw(tick) :
        global angle,mode
        global facecolors
        
        start = time.ticks_ms()
        pen(0,0,0)
        clear()
        
        i = 0
        oldt2 = 0
        # get each face (3d triangle)
        for face in faces:
            triangle = []
            for pointindex in face:
                point3 = points[pointindex]
                rotated3 = rot3d(point3,[angle,0,angle])
                triangle.append (rotated3)      
            
            # find normal of triangle 
            n = normal(triangle)
            camera = (0,0,10)
            d = dotproduct(n,camera)
            
            #hidden surface removal
            #only draw if facing camera
            if (d > 0) : continue
            
            # 3d points to 2d screen
            t1,t2,t3 = triangle
            t1 = to2d(t1)
            t2 = to2d(t2)
            t3 = to2d(t3)
            
            if mode == 0:
                #wireframe
                # quad (merge 2 consecutive triangles)
                if (i % 2) :
                    pen(15,15,15)
                    poly (t2,t2old,t1,t3)
                t2old = t2
            if mode == 1:
                # shade by normal to screen camera
                d = abs(d) / 500
                d = int(d)
                pen(d,d,d)
                fpoly(t1,t2,t3)
            if mode == 2:
                # solid colors for faces
                r,g,b = facecolors[i]
                pen (r,g,b)
                fpoly(t1,t2,t3)    
            i += 1
                
        timetaken = time.ticks_ms() - start
        txt = " " + str (timetaken) + " ms - " + str (1000 // timetaken) + " fps"
        pen(15,15,15)
        text (txt,0,0)
        flip()
init()
start()