import os
import sys
from PIL import Image
from math import floor

"""
idxs son los indices a cambiar a partir del pixel actual:
donde idxs := [(),()] es una lista de tuplas
tal que el primer elemento es el offset de x y el segundo el offset de y
factors es una lista con el factor de amplificacion para los pixeles
de las tuplas anteriores
"""
def floyd(filename):
	idxs = [(0,1),(1,0),(1,1),(1,2)]
	factor = 32
	factors = [7,3,5,1]
	dither(filename,factor,idxs,factors)

def fakefloyd(filename):
	idxs = [(0,1),(1,0),(1,1)]
	factor = 8
	factors = [3,3,2]
	dither(filename,factor,idxs,factors)

def jarvis(filename):
	idxs = [(0,1),(0,2),(1,0),(1,1),(1,2),(1,3),(1,4)]
	factor = 48
	factors = [7,5,3,5,7,5,3,1,3,5,3,1]
	dither(filename,factor,idxs,factors)

def stucki(filename):
	idxs = [(0,1),(0,2),(1,0),(1,1),(1,2),(1,3),(1,4),(2,0),(2,1),(2,2),(2,3),(2,4)]
	factor = 42
	factors = [8,4,2,4,8,4,2,1,2,4,2,1]
	dither(filename,factor,idxs,factors)

def atkinson(filename):
	idxs = [(0,1),(0,2),(1,0),(1,1),(1,2),(2,1)]
	factor = 8
	factors = [1,1,1,1,1,1]
	dither(filename,factor,idxs,factors)

def burkes(filename):
	idxs = [(0,1),(0,2),(1,0),(1,1),(1,2),(1,3),(1,4)]
	factor = 32
	factors = [8,4,2,4,8,4,2]
	dither(filename,factor,idxs,factors)

def sierra(filename):
	idxs = [(0,1),(0,2),(1,0),(1,1),(1,2),(1,3),(1,4),(2,1),(2,2),(2,3)]
	factor = 32
	factors = [5,3,2,4,5,4,2,2,3,2]
	dither(filename,factor,idxs,factors)

def dither(filename,factor,idxs,factors):
	img = Image.open(filename).convert('LA').convert('RGB')
	img.show()
	pixels = img.load()
	ancho,alto = img.width,img.height
	for i in range(0,ancho):
		for j in range(0,alto):
			r,g,b = pixels[i,j]
			# blanco 255,255,255, negro 0,0,0
			# Si el pixel es < 128 lo cambio a negro si no a blanco mas el error
			if r > 127: error = r - 127
			else: error = 255 - r
			error = int(error / factor)
			# definimos el valor para los pixeles adyacentes (las coordenadas estan en idxs)
			for tupidx in range(0,len(idxs)):
				try:
					idxi = i + int(idxs[tupidx][0])
					idxj = j + int(idxs[tupidx][1])
					pix = pixels[idxi,idxj]
					nr,ng,nb = pix[0]+(error*factors[tupidx]),pix[1]+(error*factors[tupidx]),pix[2]+(error*factors[tupidx])
					pixels[idxi,idxj] = (nr,ng,nb)
				except Exception as e: pass
	img.show()
	
floyd(sys.argv[1])
