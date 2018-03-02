from PIL import Image
import sys
"""
Esta funcion toma una subseccion de la imagen y hace el promedio
de los pixeles blanco y negro ignorando los pixeles de color
despues regresa ese promedio para ponerlo como el valor de ese pixel
"""
def getProm(img):
	pixels = img.load()
	tamimg =  img.width*img.height
	rt,gt,bt=(0,0,0)
	numpixeles = 0
	for w in range(0, img.width):
		for h in range(0, img.height):
			# si es de color no deberia incluirlo en el promedio
			r,g,b = img.getpixel((w,h))[0],img.getpixel((w,h))[1],img.getpixel((w,h))[2]
			if r==g and g==b:
				rt+=img.getpixel((w,h))[0]
				gt+=img.getpixel((w,h))[1]
				bt+=img.getpixel((w,h))[2]
				numpixeles+=1
	rt,gt,bt = (rt/numpixeles,gt/numpixeles,bt/numpixeles)
	return (rt,gt,bt)

"""
Recorre la imagen por renglones y columnas cada que detecta un pixel px
de color hace una subseccion donde las esquinas son desde 
px-margen,py-margen hasta px+margen,py+margen y remplaza este pixel por
el valor del promedio de el area subyacente
"""
def recorre(imgname,margen):
	img = Image.open(imgname)
	pixels = img.load()
	tamimg =  img.width*img.height
	rt,gt,bt=(0,0,0)
	img.show()
	for w in range(0, img.width):
		for h in range(0, img.height):
			r,g,b = img.getpixel((w,h))[0],img.getpixel((w,h))[1],img.getpixel((w,h))[2]
			if r!=g or g!=b:
				try:
					box = (w-margen),(h-margen),(w+margen),(h+margen)
					region = img.crop(box)
					pixval = getProm(region)
					pixels[w,h] = pixval
				except Exception as e:
					print e
					pixels[w,h] = (0,255,0)
	img.show()

if len(sys.argv)==3:
	recorre(sys.argv[1],int(sys.argv[2]))
else:
	print sys.argv[0],"image","boxsize"
