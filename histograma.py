import os
import sys
from PIL import Image
def cuenta(filename):
        im =  Image.open(filename).convert('RGB')
        pixels = im.load()
        ancho,alto = im.width,im.height
        for i in range(0,ancho):
                for j in range(0,alto):
                        r,g,b = pixels[i,j]
                        np = int(floor((l-1)*sum))
                        pixelsbak[i,j] = (np,np,np)
        im.show()


