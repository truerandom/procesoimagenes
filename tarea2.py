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
		#filtro blur
		blurMenuItem = filtrosMenu.Append(wx.NewId(), "Blur","Open Image")
		self.Bind(wx.EVT_MENU, self.onBlur,blurMenuItem)
		#filtro motion blur
		motionblurMenuItem = filtrosMenu.Append(wx.NewId(), "MotionBlur","Open Image")
		self.Bind(wx.EVT_MENU, self.onMotionBlur,motionblurMenuItem)
		# filtro encuentra bordes
		encuentrabordesMenuItem = filtrosMenu.Append(wx.NewId(), "EncuentraBordes","Open Image")
		self.Bind(wx.EVT_MENU, self.onEncuentraBordes,encuentrabordesMenuItem)
		# filtro sharpen
		sharpenMenuItem = filtrosMenu.Append(wx.NewId(), "Sharpen","Open Image")
		self.Bind(wx.EVT_MENU, self.onEncuentraBordes,encuentrabordesMenuItem)
		# filtro relieve
		relieveMenuItem = filtrosMenu.Append(wx.NewId(), "Relieve","Open Image")
		self.Bind(wx.EVT_MENU, self.onRelieve,relieveMenuItem)
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

	def onBlur(self,event):
		matriz = np.matrix([[0.0,0.2,0.0], [0.2,0.2,0.2], [0.0,0.2,0.0]])
		factor,ajuste = 1.0,0.0
		img = self.convolucion(matriz,factor,ajuste)
		# Conversion
		image = wx.EmptyImage(img.size[0], img.size[1])
		new_image = img.convert('RGB')
		data = new_image.tobytes()
		image.SetData(data)
		# Fin conversion
		fgs = wx.FlexGridSizer(cols=1, hgap=10, vgap=10)
		sb1 = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(image))
		fgs.Add(sb1)
		self.panel.SetSizerAndFit(fgs)
		self.Fit()
		self.Refresh()

	def onMotionBlur(self,event):
		matriz = np.matrix([[1,0,0,0,0,0,0,0,0], [0,1,0,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0],
				[0,0,0,1,0,0,0,0,0],[0,0,0,0,1,0,0,0,0],[0,0,0,0,0,1,0,0,0],
				[0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,0,1]])
		factor,ajuste = 1.0/9.0,0.0
		img = self.convolucion(matriz,factor,ajuste)
		# Conversion
		image = wx.EmptyImage(img.size[0], img.size[1])
		new_image = img.convert('RGB')
		data = new_image.tobytes()
		image.SetData(data)
		# Fin conversion
		fgs = wx.FlexGridSizer(cols=1, hgap=10, vgap=10)
		sb1 = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(image))
		fgs.Add(sb1)
		self.panel.SetSizerAndFit(fgs)
		self.Fit()
		self.Refresh()

	def onEncuentraBordes(self,event):
		matriz = np.matrix([[0,0,-1,0,0],[0,0,-1,0,0],[0,0, 2,0,0],[0,0,0,0,0],[0,0, 0,0,0]])
		factor,ajuste = 1.0,0.0
		img = self.convolucion(matriz,factor,ajuste)
		# Conversion
		image = wx.EmptyImage(img.size[0], img.size[1])
		new_image = img.convert('RGB')
		data = new_image.tobytes()
		image.SetData(data)
		# Fin conversion
		fgs = wx.FlexGridSizer(cols=1, hgap=10, vgap=10)
		sb1 = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(image))
		fgs.Add(sb1)
		self.panel.SetSizerAndFit(fgs)
		self.Fit()
		self.Refresh()

	def onSharpen(self,event):
		matriz = np.matrix([[-1,-1,-1],[-1, 9,-1],[-1,-1,-1]])
		factor,ajuste = 1.0,0.0
		img = self.convolucion(matriz,factor,ajuste)
		# Conversion
		image = wx.EmptyImage(img.size[0], img.size[1])
		new_image = img.convert('RGB')
		data = new_image.tobytes()
		image.SetData(data)
		# Fin conversion
		fgs = wx.FlexGridSizer(cols=1, hgap=10, vgap=10)
		sb1 = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(image))
		fgs.Add(sb1)
		self.panel.SetSizerAndFit(fgs)
		self.Fit()
		self.Refresh()
	
	def onRelieve(self,event):
		matriz = np.matrix([[-1,-1, 0],[-1, 0, 1],[ 0, 1, 1]])
		factor,ajuste = 1.0,128
		img = self.convolucion(matriz,factor,ajuste)
		# Conversion
		image = wx.EmptyImage(img.size[0], img.size[1])
		new_image = img.convert('RGB')
		data = new_image.tobytes()
		image.SetData(data)
		# Fin conversion
		fgs = wx.FlexGridSizer(cols=1, hgap=10, vgap=10)
		sb1 = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(image))
		fgs.Add(sb1)
		self.panel.SetSizerAndFit(fgs)
		self.Fit()
		self.Refresh()

	def convolucion(self,matriz,factor,ajuste):
		x,y = matriz.shape
		im = Image.open(self.filename).convert('RGB')
		ancho = im.width
		alto = im.height 
		pixels = im.load()
		for i in range(0,ancho):
			for j in range(0,alto):
				red,green,blue = 0.0,0.0,0.0
				for k in range(x):
					for l in range(y):
						imageX = (i - x / 2 + k + ancho) % ancho
						imageY = (j - y / 2 + l + alto) % alto
						r,g,b = im.getpixel((imageX,imageY))
						valor = matriz.item(k,l)
						red+=r*valor
						green+=g*valor
						blue+=b*valor
				redx = min(max((factor * red + ajuste),0),255)
				greenx = min(max((factor * green + ajuste),0),255)
				bluex = min(max((factor * blue + ajuste),0),255)
				pixels[i,j] = (int(redx),int(greenx),int(bluex))
		return im

if __name__ == "__main__":
	app = wx.App(False)
	frame = MyForm().Show()
	app.MainLoop()

