import wx 
import os
from PIL import Image
########################################################################
class MyForm(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, title="Filtros")
		self.panel = wx.Panel(self, wx.ID_ANY)
		self.setMenu()
		
	def setMenu(self):
		menuBar = wx.MenuBar()
		# menus
		fileMenu = wx.Menu()
		abrirMenuItem = fileMenu.Append(wx.NewId(), "Abrir","Open Image")
		self.Bind(wx.EVT_MENU, self.onAbrir, abrirMenuItem)
		exitMenuItem = fileMenu.Append(wx.NewId(), "Exit","Exit the application")
		self.Bind(wx.EVT_MENU, self.onExit, exitMenuItem)
		# opciones de menu
		filtrosMenu = wx.Menu()
		# grispromedio
		grispromedioMenuItem = filtrosMenu.Append(wx.NewId(), "GrisPromedio","Open Image")
		self.Bind(wx.EVT_MENU, self.onGrisPromedio,grispromedioMenuItem)
		# grisecuacion 
		grisecuacionMenuItem = filtrosMenu.Append(wx.NewId(), "GrisEcuacion","Open Image")
		self.Bind(wx.EVT_MENU, self.onGrisEcuacion,grisecuacionMenuItem)
		# gris rojo
		grisrojoMenuItem = filtrosMenu.Append(wx.NewId(), "GrisRojo","Open Image")
		self.Bind(wx.EVT_MENU, self.onGrisRojo,grisrojoMenuItem)
		# gris verde
		grisverdeMenuItem = filtrosMenu.Append(wx.NewId(), "GrisVerde","Open Image")
		self.Bind(wx.EVT_MENU, self.onGrisVerde,grisverdeMenuItem)
		# gris azul
		grisazulMenuItem = filtrosMenu.Append(wx.NewId(), "GrisAzul","Open Image")
		self.Bind(wx.EVT_MENU, self.onGrisAzul,grisazulMenuItem)
		# filtros por color
		rojoMenuItem = filtrosMenu.Append(wx.NewId(), "FiltroRojo","Open Image")
		self.Bind(wx.EVT_MENU, self.onRojo,rojoMenuItem)
		verdeMenuItem = filtrosMenu.Append(wx.NewId(), "FiltroVerde","Open Image")
		self.Bind(wx.EVT_MENU, self.onVerde,verdeMenuItem)
		azulMenuItem = filtrosMenu.Append(wx.NewId(), "FiltroAzul","Open Image")
		self.Bind(wx.EVT_MENU, self.onAzul,azulMenuItem)
		# icon 
		iconMenuItem = filtrosMenu.Append(wx.NewId(), "ToIcon","Open Image")
		self.Bind(wx.EVT_MENU, self.onIcon,iconMenuItem)
		# mosaico
		mosaicoMenuItem = filtrosMenu.Append(wx.NewId(), "Mosaico","Open Image")	
		self.Bind(wx.EVT_MENU, self.onMosaico,mosaicoMenuItem)
		# onImgLetrasGrises
		imgletrasgrisesMenuItem = filtrosMenu.Append(wx.NewId(), "ImgLetrasGrises","Open Image")	
		self.Bind(wx.EVT_MENU, self.onImgLetrasGrises,imgletrasgrisesMenuItem)
		# onImgLetraGris
		imgletragrisMenuItem = filtrosMenu.Append(wx.NewId(), "ImgLetraGris","Open Image")	
		self.Bind(wx.EVT_MENU, self.onImgLetraGris,imgletragrisMenuItem)
		# onImgLetraColor
		imgletracolorMenuItem = filtrosMenu.Append(wx.NewId(), "ImgLetraColor","Open Image")	
		self.Bind(wx.EVT_MENU, self.onImgLetraColor,imgletracolorMenuItem)
		# onDomino
		dominoMenuItem = filtrosMenu.Append(wx.NewId(), "Domino","Open Image")	
		self.Bind(wx.EVT_MENU, self.onDomino,dominoMenuItem)
		# onNaipes
		naipesMenuItem = filtrosMenu.Append(wx.NewId(), "Naipes","Open Image")	
		self.Bind(wx.EVT_MENU, self.onNaipes,naipesMenuItem)
		
		menuBar.Append(fileMenu, "&Archivos")
		menuBar.Append(filtrosMenu, "&Filtros")
		self.SetMenuBar(menuBar)
				
	def onExit(self, event): self.Close()
	def onAbrir(self,event):
		wildcard = ""
		dialog = wx.FileDialog(None, "Choose a file", os.getcwd(),"", wildcard, wx.OPEN)
		if dialog.ShowModal() == wx.ID_OK:
			self.filename = dialog.GetPath()
			dialog.Destroy()
			fgs = wx.FlexGridSizer(cols=2, hgap=10, vgap=10)
			img1 = wx.Image(self.filename, wx.BITMAP_TYPE_ANY)
			sb1 = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(img1))
			fgs.Add(sb1)
			self.panel.SetSizerAndFit(fgs)
			self.Fit()
	
	def onIcon(self,event,tamx=15,tamy=15):
		im = Image.open(self.filename)
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
				self.icon_aux(region)
				#region = mosaico_aux(region)
				im.paste(region, box)
				xant+=tamx
			xant = 0
			yant+=tamy
		# convertimos la imagen de pil a raster
		image = wx.EmptyImage(im.size[0], im.size[1])
		new_image = im.convert('RGB')
		data = new_image.tobytes()
		image.SetData(data)
		# fin conversion
		fgs = wx.FlexGridSizer(cols=1, hgap=10, vgap=10)
		sb1 = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(image))
		fgs.Add(sb1)
		self.panel.SetSizerAndFit(fgs)
		self.Fit()
		self.Refresh()
		
	def icon_aux(self,box):
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
			
	def onRojo(self,event): self.filtroRGB(1,0,0)
	def onVerde(self,event): self.filtroRGB(0,1,0)
	def onAzul(self,event): self.filtroRGB(0,0,1)	
	def filtroRGB(self,rx,gx,bx):
		im = Image.open(self.filename)
		pixels = im.load()
		for w in range(0, im.width):
			for h in range(0, im.height):
				r= im.getpixel((w,h))[0]
				g= im.getpixel((w,h))[1]
				b= im.getpixel((w,h))[2]
				prom1,prom2,prom3 = (0,0,0)
				#actual = (data[i]*0.3 + data[i+1]*0.59 + data[i+2]*0.11) / 3
				if rx == 1: prom1= r
				if gx == 1: prom2 = g
				if bx == 1: prom3 = b
				pixels[w,h] = (prom1,prom2,prom3)
		# convertimos la imagen de pil a raster
		image = wx.EmptyImage(im.size[0], im.size[1])
		new_image = im.convert('RGB')
		data = new_image.tobytes()
		image.SetData(data)
		# fin conversion
		fgs = wx.FlexGridSizer(cols=1, hgap=10, vgap=10)
		sb1 = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(image))
		fgs.Add(sb1)
		self.panel.SetSizerAndFit(fgs)
		self.Fit()
		self.Refresh()
	
	def onGrisRojo(self,event):self.onGrisRGB(1,0,0)	
	def onGrisVerde(self,event): self.onGrisRGB(0,1,0)
	def onGrisAzul(self,event): self.onGrisRGB(0,0,1)
	def onGrisRGB(self,rx,gx,bx):
		im = Image.open(self.filename)
		pixels = im.load()
		for w in range(0, im.width):
			for h in range(0, im.height):
				r= im.getpixel((w,h))[0]
				g= im.getpixel((w,h))[1]
				b= im.getpixel((w,h))[2]
				#actual = (data[i]*0.3 + data[i+1]*0.59 + data[i+2]*0.11) / 3
				if rx == 1: prom = r
				if gx == 1: prom = g
				if bx == 1: prom = b
				pixels[w,h] = (prom,prom,prom)
		# convertimos la imagen de pil a raster
		image = wx.EmptyImage(im.size[0], im.size[1])
		new_image = im.convert('RGB')
		data = new_image.tobytes()
		image.SetData(data)
		# fin conversion
		fgs = wx.FlexGridSizer(cols=1, hgap=10, vgap=10)
		sb1 = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(image))
		fgs.Add(sb1)
		self.panel.SetSizerAndFit(fgs)
		self.Fit()
		self.Refresh()
		
	def onGrisPromedio(self,event):
		im = Image.open(self.filename)
		pixels = im.load()
		for w in range(0, im.width):
			for h in range(0, im.height):
				r= im.getpixel((w,h))[0]
				g= im.getpixel((w,h))[1]
				b= im.getpixel((w,h))[2]
				prom = (r+g+b) / 3
				pixels[w,h] = (prom,prom,prom)
		# convertimos la imagen de pil a raster
		image = wx.EmptyImage(im.size[0], im.size[1])
		new_image = im.convert('RGB')
		data = new_image.tobytes()
		image.SetData(data)
		# fin conversion
		fgs = wx.FlexGridSizer(cols=1, hgap=10, vgap=10)
		sb1 = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(image))
		fgs.Add(sb1)
		self.panel.SetSizerAndFit(fgs)
		self.Fit()
		self.Refresh()	
		
	def onGrisEcuacion(self,event):
		im = Image.open(self.filename)
		pixels = im.load()
		for w in range(0, im.width):
			for h in range(0, im.height):
				r= im.getpixel((w,h))[0]
				g= im.getpixel((w,h))[1]
				b= im.getpixel((w,h))[2]
				#actual = (data[i]*0.3 + data[i+1]*0.59 + data[i+2]*0.11) / 3
				prom = int((r*0.3+ g*0.59 + b * 0.11)/3)
				pixels[w,h] = (prom,prom,prom)
		# convertimos la imagen de pil a raster
		image = wx.EmptyImage(im.size[0], im.size[1])
		new_image = im.convert('RGB')
		data = new_image.tobytes()
		image.SetData(data)
		# fin conversion
		fgs = wx.FlexGridSizer(cols=1, hgap=10, vgap=10)
		sb1 = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(image))
		fgs.Add(sb1)
		self.panel.SetSizerAndFit(fgs)
		self.Fit()
		self.Refresh()
		
	def onMosaico(self,event,tamx=5,tamy=5):
		im = Image.open(self.filename)
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
				self.mosaico_aux(region)
				#region = mosaico_aux(region)
				im.paste(region, box)
				xant+=tamx
			xant = 0
			yant+=tamy
		# convertimos la imagen de pil a raster
		image = wx.EmptyImage(im.size[0], im.size[1])
		new_image = im.convert('RGB')
		data = new_image.tobytes()
		image.SetData(data)
		# fin conversion
		fgs = wx.FlexGridSizer(cols=1, hgap=10, vgap=10)
		sb1 = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(image))
		fgs.Add(sb1)
		self.panel.SetSizerAndFit(fgs)
		self.Fit()
		self.Refresh()
		
	def mosaico_aux(self,box):
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
	
	def onImgLetrasGrises(self,event):
		im = Image.open(self.filename)
		pixels = im.load()
		htmlcode='<html><head><style>body { line-height: 0; white-space: pre; font-family:Consolas,Monaco,Lucida Console,Liberation Mono,DejaVu Sans Mono,Bitstream Vera Sans Mono,Courier New, monospace; }</style></head><body>\n'
		for h in range(0, im.height):
			for w in range(0, im.width):
				r= im.getpixel((w,h))[0]
				g= im.getpixel((w,h))[1]
				b= im.getpixel((w,h))[2]
				#actual = (data[i]*0.3 + data[i+1]*0.59 + data[i+2]*0.11) / 3
				prom = int((r+ g+ b  )/3)
				if 0 <= prom <= 15: htmlcode+='M'
				if 16 <= prom <= 31: htmlcode+='N'
				if 32 <= prom <= 47: htmlcode+='H'
				if 48 <= prom <= 63: htmlcode+='#'
				if 64 <= prom <= 79: htmlcode+='Q'
				if 80 <= prom <= 95: htmlcode+='U'
				if 96 <= prom <= 111: htmlcode+='A'
				if 112 <= prom <= 127: htmlcode+='D'
				if 128 <= prom <= 143: htmlcode+='0'
				if 144 <= prom <= 159: htmlcode+='Y'
				if 160 <= prom <= 175: htmlcode+='2'
				if 176 <= prom <= 191: htmlcode+='$'
				if 192 <= prom <= 209: htmlcode+='%'
				if 210 <= prom <= 225: htmlcode+='+'
				if 226 <= prom <= 239: htmlcode+='.'
				if 240 <= prom <= 255: htmlcode+=' ' 
				if w == im.width-1:
					htmlcode+='\n<p>'
		htmlcode+='\n</body><html>'
		with open(self.filename+'.html', 'w') as f:
			print >> f, htmlcode
			print 'Archivo generado'
			
	def onImgLetraGris(self,event):
		im = Image.open(self.filename)
		pixels = im.load()
		htmlcode='<html><head><style>body { line-height: 0; white-space: pre; font-family:Consolas,Monaco,Lucida Console,Liberation Mono,DejaVu Sans Mono,Bitstream Vera Sans Mono,Courier New, monospace; }</style></head><body>\n'
		for h in range(0, im.height):
			for w in range(0, im.width):
				r= im.getpixel((w,h))[0]
				g= im.getpixel((w,h))[1]
				b= im.getpixel((w,h))[2]
				#actual = (data[i]*0.3 + data[i+1]*0.59 + data[i+2]*0.11) / 3
				prom = int((r+ g+ b  )/3)
				if 0 <= prom <= 15: htmlcode+='<font color="#000000">@</font>'
				if 16 <= prom <= 31: htmlcode+='<font color="#101010">@</font>'
				if 32 <= prom <= 47: htmlcode+='<font color="#202020">@</font>'
				if 48 <= prom <= 63: htmlcode+='<font color="#303030">@</font>'
				if 64 <= prom <= 79: htmlcode+='<font color="#404040">@</font>'
				if 80 <= prom <= 95: htmlcode+='<font color="#505050">@</font>'
				if 96 <= prom <= 111: htmlcode+='<font color="#606060">@</font>'
				if 112 <= prom <= 127: htmlcode+='<font color="#696969">@</font>'
				if 128 <= prom <= 143: htmlcode+='<font color="#787878">@</font>'
				if 144 <= prom <= 159: htmlcode+='<font color="#909090">@</font>'
				if 160 <= prom <= 175: htmlcode+='<font color="#A0A0A0">@</font>'
				if 176 <= prom <= 191: htmlcode+='<font color="#B0B0B0">@</font>'
				if 192 <= prom <= 209: htmlcode+='<font color="#C8C8C8">@</font>'
				if 210 <= prom <= 225: htmlcode+='<font color="#D8D8D8">@</font>'
				if 226 <= prom <= 239: htmlcode+='<font color="#E8E8E8">@</font>'
				if 240 <= prom <= 255: htmlcode+='<font color="#F8F8F8">@</font>' 
				if w == im.width-1:
					htmlcode+='\n<p>'
		htmlcode+='\n</body><html>'
		with open(self.filename+'.html', 'w') as f:
			print >> f, htmlcode
			print 'Archivo generado'
			
	def onImgLetraColor(self,event):
		im = Image.open(self.filename)
		pixels = im.load()
		htmlcode='<html><head><style>body { line-height: 0; white-space: pre; font-family:Consolas,Monaco,Lucida Console,Liberation Mono,DejaVu Sans Mono,Bitstream Vera Sans Mono,Courier New, monospace; }</style></head><body>\n'
		for h in range(0, im.height):
			for w in range(0, im.width):
				r= im.getpixel((w,h))[0]
				g= im.getpixel((w,h))[1]
				b= im.getpixel((w,h))[2]
				#actual = (data[i]*0.3 + data[i+1]*0.59 + data[i+2]*0.11) / 3
				prom = '#%02x%02x%02x' % (r, g, b)
				htmlcode+='<font color="%s">@</font>' % (prom)
				if w == im.width-1:
					htmlcode+='\n<p>'
		htmlcode+='\n</body><html>'
		with open(self.filename+'.html', 'w') as f:
			print >> f, htmlcode
			print 'Archivo generado'
	
	def onDomino(self,event):
		im = Image.open(self.filename)
		pixels = im.load()
		htmlcode='<html><head><style>body { line-height: 0; white-space: pre; font-family:Consolas,Monaco,Lucida Console,Liberation Mono,DejaVu Sans Mono,Bitstream Vera Sans Mono,Courier New, monospace; }</style></head><body>\n'
		for h in range(0, im.height):
			for w in range(0, im.width):
				r= im.getpixel((w,h))[0]
				g= im.getpixel((w,h))[1]
				b= im.getpixel((w,h))[2]
				#actual = (data[i]*0.3 + data[i+1]*0.59 + data[i+2]*0.11) / 3
				prom = int((r+ g+ b  )/3)
				if 0 <= prom <= 15: htmlcode+='&#127074;'
				if 16 <= prom <= 31: htmlcode+='&#127123;'
				if 32 <= prom <= 47: htmlcode+='&#127122;'
				if 48 <= prom <= 63: htmlcode+='&#127115;'
				if 64 <= prom <= 79: htmlcode+='&#127114;'
				if 80 <= prom <= 95: htmlcode+='&#127107;'
				if 96 <= prom <= 111: htmlcode+='&#127106;'
				if 112 <= prom <= 127: htmlcode+='&#127099;'
				if 128 <= prom <= 143: htmlcode+='&#127099;'
				if 144 <= prom <= 159: htmlcode+='&#127098;'
				if 160 <= prom <= 175: htmlcode+='&#127091;'
				if 176 <= prom <= 191: htmlcode+='&#127090;'
				if 192 <= prom <= 209: htmlcode+='&#127083;'
				if 210 <= prom <= 225: htmlcode+='&#127082;'
				if 226 <= prom <= 239: htmlcode+='&#127075;'
				if 240 <= prom <= 255: htmlcode+='&#127075;' 
				if w == im.width-1:
					htmlcode+='\n<p>'
		htmlcode+='\n</body><html>'
		with open(self.filename+'.html', 'w') as f:
			print >> f, htmlcode
			print 'Archivo generado'
			
	def onNaipes(self,event):
		im = Image.open(self.filename)
		pixels = im.load()
		htmlcode='<html><head><style>body { line-height: 0; white-space: pre; font-family:Consolas,Monaco,Lucida Console,Liberation Mono,DejaVu Sans Mono,Bitstream Vera Sans Mono,Courier New, monospace; }</style></head><body>\n'
		for h in range(0, im.height):
			for w in range(0, im.width):
				r= im.getpixel((w,h))[0]
				g= im.getpixel((w,h))[1]
				b= im.getpixel((w,h))[2]
				#actual = (data[i]*0.3 + data[i+1]*0.59 + data[i+2]*0.11) / 3
				prom = int((r+ g+ b  )/3)
				# &#127178;
				prom = int((r+ g+ b  )/3)
				if 0 <= prom <= 15: htmlcode+='<font color="#000000">&#127178;</font>'
				if 16 <= prom <= 31: htmlcode+='<font color="#101010">&#127178;</font>'
				if 32 <= prom <= 47: htmlcode+='<font color="#202020">&#127178;</font>'
				if 48 <= prom <= 63: htmlcode+='<font color="#303030">&#127178;</font>'
				if 64 <= prom <= 79: htmlcode+='<font color="#404040">&#127178;</font>'
				if 80 <= prom <= 95: htmlcode+='<font color="#505050">&#127178;</font>'
				if 96 <= prom <= 111: htmlcode+='<font color="#606060">&#127178;</font>'
				if 112 <= prom <= 127: htmlcode+='<font color="#696969">&#127178;</font>'
				if 128 <= prom <= 143: htmlcode+='<font color="#787878">&#127178;</font>'
				if 144 <= prom <= 159: htmlcode+='<font color="#909090">&#127178;</font>'
				if 160 <= prom <= 175: htmlcode+='<font color="#A0A0A0">&#127178;</font>'
				if 176 <= prom <= 191: htmlcode+='<font color="#B0B0B0">&#127178;</font>'
				if 192 <= prom <= 209: htmlcode+='<font color="#C8C8C8">&#127178;</font>'
				if 210 <= prom <= 225: htmlcode+='<font color="#D8D8D8">&#127178;</font>'
				if 226 <= prom <= 239: htmlcode+='<font color="#E8E8E8">&#127178;</font>'
				if 240 <= prom <= 255: htmlcode+='<font color="#F8F8F8">&#127178;</font>' 
				if w == im.width-1:
					htmlcode+='\n<p>'
		htmlcode+='\n</body><html>'
		with open(self.filename+'.html', 'w') as f:
			print >> f, htmlcode
			print 'Archivo generado'
		
if __name__ == "__main__":
	app = wx.App(False)
	frame = MyForm().Show()
	app.MainLoop()
