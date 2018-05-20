import wx 
import os
import numpy as np
from math import floor
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
                #filtro Floyd
                floydMenuItem = filtrosMenu.Append(wx.NewId(), "Floyd","Floyd")
                self.Bind(wx.EVT_MENU, self.onFloyd,floydMenuItem)
		#fake Floyd
                fakefloydMenuItem = filtrosMenu.Append(wx.NewId(), "Fake Floyd","Fake Floyd")
                self.Bind(wx.EVT_MENU, self.onFakeFloyd,fakefloydMenuItem)
		#jarvis
                jarvisMenuItem = filtrosMenu.Append(wx.NewId(), "Jarvis","Jarvis")
                self.Bind(wx.EVT_MENU, self.onJarvis,jarvisMenuItem)
		#stucki
                stuckiMenuItem = filtrosMenu.Append(wx.NewId(), "Stucki","Stucki")
                self.Bind(wx.EVT_MENU, self.onStucki,stuckiMenuItem)
		#atkinson
                atkinsonMenuItem = filtrosMenu.Append(wx.NewId(), "Atkinson","Atkinson")
                self.Bind(wx.EVT_MENU, self.onAtkinson,atkinsonMenuItem)
		#burkers
                burkesMenuItem = filtrosMenu.Append(wx.NewId(), "Burkes","Burkes")
                self.Bind(wx.EVT_MENU, self.onBurkes,burkesMenuItem)
		#sierra
                sierraMenuItem = filtrosMenu.Append(wx.NewId(), "Sierra","Sierra")
                self.Bind(wx.EVT_MENU, self.onSierra,sierraMenuItem)

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

        def onFloyd(self,event):
		idxs = [(0,1),(1,0),(1,1),(1,2)]
		factor = 32
		factors = [7,3,5,1]
		self.dither(factor,idxs,factors)
	
	def onFakeFloyd(self,event):
		idxs = [(0,1),(1,0),(1,1)]
		factor = 8
		factors = [3,3,2]
		self.dither(factor,idxs,factors)

	def onJarvis(self,event):
		idxs = [(0,1),(0,2),(1,0),(1,1),(1,2),(1,3),(1,4)]
		factor = 48
		factors = [7,5,3,5,7,5,3,1,3,5,3,1]
		self.dither(factor,idxs,factors)

	def onStucki(self,event):
		idxs = [(0,1),(0,2),(1,0),(1,1),(1,2),(1,3),(1,4),(2,0),(2,1),(2,2),(2,3),(2,4)]
		factor = 42
		factors = [(0,1),(0,2),(1,0),(1,1),(1,2),(1,3),(1,4),(2,0),(2,1),(2,2),(2,3),(2,4)]
		self.dither(factor,idxs,factors)

	def onAtkinson(self,event):
		idxs = [(0,1),(0,2),(1,0),(1,1),(1,2),(2,1)]
		factor = 8
		factors = [1,1,1,1,1,1]
		self.dither(factor,idxs,factors)

	def onBurkes(self,event):
		idxs = [(0,1),(0,2),(1,0),(1,1),(1,2),(1,3),(1,4)]
		factor = 32
		factors = [8,4,2,4,8,4,2]
		self.dither(factor,idxs,factors)

	def onSierra(self,event):
		idxs = [(0,1),(0,2),(1,0),(1,1),(1,2),(1,3),(1,4),(2,1),(2,2),(2,3)]
		factor = 32
		factors = [5,3,2,4,5,4,2,2,3,2]
		self.dither(factor,idxs,factors)

	def dither(self,factor,idxs,factors):
		img = Image.open(self.filename).convert('LA').convert('RGB')
		pixels = img.load()
		ancho,alto = img.width,img.height
		for i in range(0,ancho):
			for j in range(0,alto):
				r,g,b = pixels[i,j]
				# Si el pixel es < 128 lo cambio a negro si no a blanco mas el error
				if r > 127: error = r - 127
				else: error = 255 - r
				error = int(error / factor)
				# definimos el valor para los pixeles adyacentes (las coordenadas estan en idxs)
				for tupidx in range(0,len(idxs)):
					try:
						idxi = i + int(idxs[tupidx][0])
						idxj = j + int(idxs[tupidx][1])
						pix = pixels[idxi,idxj]
						nr,ng,nb = pix[0]+(error*factors[tupidx]),pix[1]+(error*factors[tupidx]),pix[2]+(error*factors[tupidx])
						pixels[idxi,idxj] = (nr,ng,nb)
					except Exception as e: pass
		# Conversion
                image = wx.EmptyImage(img.size[0], img.size[1])
                new_image = img.convert('RGB')
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

