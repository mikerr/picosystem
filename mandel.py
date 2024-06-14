# mandelbrot fractal

# move with cursors,
# Y/A to zoom in/out
# X invert colours
# B grayscale

import time, math
WIDTH = HEIGHT = 120

def mandel(i,res) :
    max_iter = 255  // res
    y = (i - HEIGHT/2) * scale + cy;
    for j in range (0,WIDTH, res):
        x = (j - WIDTH/2) * scale + cx;
        
        xs = (x - 0.25)
        zx = math.sqrt(xs * xs + y * y)
        if (x < zx - 2 * zx * zx + 0.25) : continue
        if ((x + 1)*(x + 1) + y * y < 1/16) : continue

        zx = zy = zx2 = zy2 = 0
        iter = 0
        for n in range (max_iter -1):
            iter = n
            zy = 2 * zx * zy + y
            zx = zx2 - zy2 + x
            zx2 = zx * zx
            zy2 = zy * zy
            if (zx2 + zy2 > 4) : break
            
        if (iter < max_iter):
                c = iter * res
                colorpixel(j,i,c)

def colorpixel(x,y,c):
    c = clr [c]
    if invertcolors : c = 255 -c
    
    if not grayscale :
        pen (hsv(c / 255,1,1))
    else : 
        r = g = b = c >> 4
        pen (r,g,b)
    pixel(x,y)
    
scale = 1./48
cx = -.6
cy = 0
invertcolors = 0
grayscale  = 0

clr= [int(255*((i/255)**12)) for i in range(255,-1,-1)]

while True:
    res = 4
    i = 0

    while True :
        if i == 0: t_start = time.ticks_ms()
               
        #scrub previous scanline
        pen(0,0,0)
        frect(0,i,WIDTH,res)
        
        if (res > 0) : mandel(i,res)
        flip()
                   
        i += res
        if i > HEIGHT :
            i = 0  
            t_end = time.ticks_ms()
            print(f"resolution {res} in {t_end - t_start} ms")
            res = res // 2
            
        if button(X) :
            invertcolors = not invertcolors
            break
        if button(B) :
            grayscale = not grayscale
            break
        if button(A) :
            scale = scale * 0.9
            break
        if button(Y) :
            scale = scale * 1.1
            break
        move = scale *5
        if button(LEFT) :
            cx -= move
            break
        if button(RIGHT) :
            cx += move
            break
        if button(UP) :
            cy -= move
            break
        if button(DOWN) :
            cy += move
            break
