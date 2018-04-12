import wx 
import os
from PIL import Image

# convierte a imagen a tono de grises
def tonogrises(imagen):
	im = imagen
	pixels = im.load()
	for w in range(0, im.width):
		for h in range(0, im.height):
			r= im.getpixel((w,h))[0]
			g= im.getpixel((w,h))[1]
			b= im.getpixel((w,h))[2]
			prom = (r+g+b) / 3
			pixels[w,h] = (prom,prom,prom)
	im.show()
	return im

def altocontraste(imagen):
	im = imagen
	pixels = im.load()
	for w in range(0, im.width):
		for h in range(0, im.height):
			r= im.getpixel((w,h))[0]
			g= im.getpixel((w,h))[1]
			b= im.getpixel((w,h))[2]
			prom = (r+g+b) / 3
			if prom > 127: pixels[w,h] = (255,255,255)
			else: pixels[w,h] = (0,0,0)
	#im.show()
	return im

"""
def cuenta(box):
	#print box
	#print type(box)
	#box.show()
	ancho = box.width # obtener ancho box	
	alto = box.height	# obtener alto box
	c_negros = 0
	for i in range(0,ancho):
		for j in range(0,alto):
			#print "(%s,%s)" % (i,j)
			color = box.getpixel((i,j))
			# aqui obtiene el rojo con getRed
			if color[2] == 0: 	
				c_negros = c_negros+1
	#print "total pix ",ancho*alto," negros ",c_negros
	return c_negros
"""

def centra(Nlineas,puntos):
	acomodados = []
	for tmp in range(0,Nlineas):
		acomodados.append(False)
	print 'puntos ',puntos
	n = puntos / 2
	if n % 2 ==1: m = n-1
	else: m = n
	print 'm ',m,' n ',n
	for i in range(Nlineas/2 -n , Nlineas/2 + m):
		acomodados[i] = True
	return acomodados
			
# donde t es el tamanio del efecto
def filtroatt(imagen,t):
	imagen = Image.open(imagen)
	#pixels = imagen.load()
	imagen = tonogrises(imagen) # la imagen se convierte a tono de grises
	imagen = altocontraste(imagen)	# le aplica alto contraste
	im = imagen
	ancho = imagen.width
	alto = imagen.height
	pixels = im.load()
	Nlineas = 15
	for i in range(0,ancho):
		for j in range(0,alto-Nlineas,Nlineas):
			puntos = 0
			print 'j+Nlineas ',j+Nlineas
			for y in range(j,(j+Nlineas)):
				if im.getpixel((i,y))[0] == 0:
					puntos = puntos + 1
			acomodados = centra(Nlineas,puntos)
			print acomodados
			for y in range(j,j+Nlineas):
				if acomodados[y-j]:
					pixels[i,y] = (0,0,0)
				else:
					pixels[i,y] = (255,255,255)
			#print im.getpixel((i,j))
	im.show()
	return im
	#ancho = imagen.
	#alto = imagen.alto
	#imagen.show()

filtroatt('pup.jpg',64)
