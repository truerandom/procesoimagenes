import wx 
import os
import numpy as np
import sys
from PIL import Image

def altocontraste(imagen,cuadranteFoto,salida):
	im = Image.open(imagen)
	pixel = im.load()
	code='<table border="0" cellspacing="0" cellpadding="0"\n<tr>'
	imgtemp = ''
	imagenes = []
	rojoRGB ,verdeRGB,azulRGB,red,green,blue = 0,0,0,0,0,0
	promedio = 0
	for i in range(0,im.width,cuadranteFoto):
		terminoX = i + cuadranteFoto
		#print 'TerminoX ',terminoX
		ltemp = []
		for j in range(0,im.height,cuadranteFoto):
			terminoY = j+cuadranteFoto
			#print 'TerminoY ',terminoY
			for k in range(i,terminoX):
				if k >= im.width: break
				for l in range(j,terminoY):
					if l >= im.height: break
					colororg = pixel[k,l]
					rojoRGB+= colororg[0]
					verdeRGB+= colororg[1]
					azulRGB+=colororg[2]
					promedio = promedio+1
			#print 'promedio ',promedio
			red,green,blue = rojoRGB/promedio,verdeRGB/promedio,azulRGB/promedio
			rojoRGB = verdeRGB = azulRGB = promedio = 0;
			promedio2 = red+green+blue
			promedio2 = promedio2 /3
			#print 'promedio2mul ',promedio2
			if 255-promedio2 < 25: imagenTemp = "1.png"
			elif 255-promedio2 < 50: imagenTemp = "2.png"
			elif 255-promedio2 < 75: imagenTemp = "3.png"
			elif 255-promedio2 < 100: imagenTemp = "4.png"
			elif 255-promedio2 < 125: imagenTemp = "5.png"
			elif 255-promedio2 < 150: imagenTemp = "6.png"
			elif 255-promedio2 < 175: imagenTemp = "7.png"
			elif 255-promedio2 < 200: imagenTemp = "8.png"
			elif 255-promedio2 < 225: imagenTemp = "9.png"
			else: imagenTemp = "10.png"
			texto='<td><img src="'+imagenTemp+'" width="4", height="4"></td>\n';
			#print imagenTemp
			ltemp.append(texto)
		imagenes.append(ltemp)
	#[[],[],[]]
	for i in range(0,len(imagenes[0])):
		for img in imagenes:
			code+=img[i]
		texto = "</tr><tr>\n"
		code+=texto
	texto = '</tr>\n</table></center>'
	code+=texto
	print code
altocontraste(sys.argv[1],3,'poc.html')
