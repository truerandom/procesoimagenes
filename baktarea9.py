import os
import sys
from PIL import Image
from math import floor
def floyd(filename):
	img = Image.open(filename).convert('LA').convert('RGB')
	pixels = img.load()
	ancho,alto = img.width,img.height
	img.show()
	factor = 32
	for i in range(0,alto):
		for j in range(0,ancho):
			r,g,b = pixels[i,j]
			# blanco 255,255,255, negro 0,0,0
			# Si el pixel es < 128 lo cambio a negro si no a blanco mas el error
			if r > 127: error = r - 127
			else: error = 255 - r
			error = int(error / factor)
			# definimos el valor para los pixeles adyacentes
			try:
				nr,ng,nb = pixels[i,j+1][0]+(error*7),pixels[i,j+1][1]+(error*7),pixels[i,j+1][2]+(error*7)
				pixels[i,j+1] = (nr,ng,nb)
			except Exception as e:pass
			try:
				nr,ng,nb = pixels[i+1,j-1][0]+(error*3),pixels[i+1,j-1][1]+(error*3),pixels[i+1,j-1][2]+(error*3)
				pixels[i+1,j-1] = (nr,ng,nb)
			except Exception as e:pass
			try:
				nr,ng,nb = pixels[i+1,j][0]+(error*5),pixels[i+1,j][1]+(error*5),pixels[i+1,j][2]+(error*5)
				pixels[i+1,j] = (nr,ng,nb)
			except Exception as e:pass
			try:
				nr,ng,nb = pixels[i+1,j+1][0]+(error),pixels[i+1,j+1][1]+(error),pixels[i+1,j+1][2]+(error)
				pixels[i+1,j+1] = (nr,ng,nb)
			except Exception as e:pass
	img.show()

def fakefloyd(filename):
	img = Image.open(filename).convert('LA').convert('RGB')
	pixels = img.load()
	ancho,alto = img.width,img.height
	img.show()
	factor = 8
	for i in range(0,alto):
		for j in range(0,ancho):
			r,g,b = pixels[i,j]
			# blanco 255,255,255, negro 0,0,0
			# Si el pixel es < 128 lo cambio a negro si no a blanco mas el error
			if r > 127: error = r - 127
			else: error = 255 - r
			error = int(error / factor)
			# definimos el valor para los pixeles adyacentes
			try:
				nr,ng,nb = pixels[i,j+1][0]+(error*3),pixels[i,j+1][1]+(error*3),pixels[i,j+1][2]+(error*3)
				pixels[i,j+1] = (nr,ng,nb)
			except Exception as e:pass
			try:
				nr,ng,nb = pixels[i+1,j-1][0]+(error*3),pixels[i+1,j-1][1]+(error*3),pixels[i+1,j-1][2]+(error*3)
				pixels[i+1,j-1] = (nr,ng,nb)
			except Exception as e:pass
			try:
				nr,ng,nb = pixels[i+1,j-1][0]+(error*2),pixels[i+1,j-1][1]+(error*2),pixels[i+1,j-1][2]+(error*2)
				pixels[i+1,j-1] = (nr,ng,nb)
			except Exception as e:pass
	img.show()


floyd(sys.argv[1])

