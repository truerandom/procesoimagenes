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
	
# donde t es el tamanio del efecto
def filtroatt(imagen,t):
	imagen = Image.open(imagen)
	#pixels = imagen.load()
	imagen = tonogrises(imagen) # la imagen se convierte a tono de grises
	imagen = altocontraste(imagen)	# le aplica alto contraste
	im = imagen
	pixels = im.load()
	xant = 0
	yant = 0
	nbloqx = im.width / t
	nbloqy = im.height / t
	for by in range(0,nbloqy):
		for bx in range(0,nbloqx):
			#print "(%d,%d) -> %d,%d,%d,%d" % (bx,by,xant,yant,xant+tamx,yant+tamy)
			box = (xant,yant,xant+t,yant+t)
			region = im.crop(box)
			nnegras = cuenta(region)
			nblancas = region.height*region.width - nnegras
			print 'negros ',nnegras,' pblancas ',nblancas
			if nblancas % 2 == 1:
				prom = (nblancas -1) /2
				res = 1
			else:
				prom = nblancas / 2
				res = 0
			# aqui hace una iteracion rara :,v
			for w in range(0,region.width):
				for h in range(0,region.width):
					print "(%s,%s)" % (w+xant,h+yant)
					print "prom %s res %s " % (prom,res)
								
			#region = mosaico_aux(region)
			im.paste(region, box)
			xant+=t
		xant = 0
		yant+=t
	im.show()
	return im
	#ancho = imagen.
	#alto = imagen.alto
	#imagen.show()

filtroatt('pup.jpg',64)
