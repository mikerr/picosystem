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
 