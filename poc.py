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
	
	def onIcon(self,event,tamx=10,tamy=10):
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
			
if __name__ == "__main__":
	app = wx.App(False)
	frame = MyForm().Show()
	app.MainLoop()
