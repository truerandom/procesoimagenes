import os
import sys
from PIL import Image
from math import floor
def cuenta(filename):
        im,imbak = Image.open(filename).convert('RGB'),Image.open(filename).convert('RGB')
        pixels,pixelsbak = im.load(),imbak.load()
        ancho,alto = im.width,im.height
        cuenta,tam = [], ancho*alto
        for i in range(0,256):  cuenta.append(0)
        l = 256
        for i in range(0,ancho):
                for j in range(0,alto):
                        r,g,b = pixels[i,j]
                        newp = (r+g+b)/3
                        pixels[i,j] = (newp,newp,newp)
                        cuenta[newp] = cuenta[newp] + 1
        for i in range(0,ancho):
                for j in range(0,alto):
                        r,g,b = pixels[i,j]
                        newp = r
                        sum = 0
                        for k in range(0,newp):
                                sum+=(float(cuenta[k])/tam)
                        np = int(floor((l-1)*sum))
                        pixelsbak[i,j] = (np,np,np)
        im.show()
        imbak.show()

cuenta(sys.argv[1])

