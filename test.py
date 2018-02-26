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
			im.paste(region, box)
			xant+=tamx
		xant = 0
		yant+=tamy
	im.show()

mosaico("dranzer.jpg",16,16)
