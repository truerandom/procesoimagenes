from PIL import Image
def mosaico(imgname,tamx,tamy):
	im = Image.open(imgname)
	# p1 = (x1,y1),p2=(x2,y2) donde lo recortado es un rectangulo con esq opuestas p1 y p2
	# itero x con i , y se queda fija, esto mientras haya bloques de x, ie tamx*iteracion < anchodela imagen
	# luego reinicio x a 0 y aumento y por el tam del bloque
	nbloqx = im.width / tamx
	nbloqy = im.height / tamy
	xant = 0
	yant = 0
	for by in range(0,nbloqy):
		for bx in range(0,nbloqx):
			#print "(%d,%d) -> %d,%d,%d,%d" % (bx,by,xant,yant,xant+tamx,yant+tamy)
			box = (xant,yant,xant+tamx,yant+tamy)
			region = im.crop(box)
			region = region.transpose(Image.ROTATE_180)
			mosaico_aux(region)
			#region = mosaico_aux(region)
			im.paste(region, box)
			xant+=tamx
		xant = 0
		yant+=tamy
	im.show()

def mosaico_aux(box):
	pixels = box.load()
	tambox =  box.width*box.height
	r,g,b=(0,0,0)
	for w in range(0, box.width):
		for h in range(0, box.height):
			r+= box.getpixel((w,h))[0]
			g+= box.getpixel((w,h))[1]
			b+= box.getpixel((w,h))[2]
	r,g,b=(r/tambox,g/tambox,b/tambox)
	for w in range(0, box.width):
		for h in range(0, box.height):
			pixels[w,h] = (r,g,b)
# COleSec.inventedtheinternet.com
mosaico("char.png",5,5)
