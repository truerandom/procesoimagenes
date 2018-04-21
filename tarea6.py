import wx 
import os
import numpy as np
from PIL import Image
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
		#filtro sepia
		sepiaMenuItem = filtrosMenu.Append(wx.NewId(), "Sepia","Open Image")
		self.Bind(wx.EVT_MENU, self.onSepia,sepiaMenuItem)
		#filtro luz negra
		luznegraMenuItem = filtrosMenu.Append(wx.NewId(), "LuzNegra","Open Image")
		self.Bind(wx.EVT_MENU, self.onLuzNegra,luznegraMenuItem)

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

	def onSepia(self,event):
		im = Image.open(self.filename)
		# donde t es el tamanio del efecto
		imagen = im
		ancho = imagen.width
		alto = imagen.height
		pixels = im.load()
		for i in range(0,ancho):
			for j in range(0,alto):
				p = pixels[i,j]
				r = int(p[0]*0.393) + int(p[1]*0.769) + int(p[2]*0.189)
				g = int(p[0]*0.349) + int(p[1]*0.686) + int(p[2]*0.168)
				b = int(p[0]*0.272) + int(p[1]*0.534) + int(p[2]*0.131)
				if r > 255: r = 255
				if g > 255: g = 255
				if b > 255: b = 255
				pixels[i,j] = (r,g,b)
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
		#return im

	def onLuzNegra(self,event):
		im = Image.open(self.filename)
		# donde t es el tamanio del efecto
		imagen = im
		ancho = imagen.width
		alto = imagen.height
		pixels = im.load()
		for i in range(0,ancho):
			for j in range(0,alto):
				p = pixels[i,j]
				r,g,b = p[0],p[1],p[2]
				l = (222* r + 707 * g + 71 * b) // 1000
				r = abs(r-l) * 2
				g = abs(g-l) * 2
				b = abs(b-l) * 2
				if r > 255: r = 255
				if g > 255: g = 255
				if b > 255: b = 255
				pixels[i,j] = (r,g,b)
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

if __name__ == "__main__":
	app = wx.App(False)
	frame = MyForm().Show()
	app.MainLoop()

