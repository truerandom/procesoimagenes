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
		
		fileMenu = wx.Menu()
		abrirMenuItem = fileMenu.Append(wx.NewId(), "Abrir","Open Image")
		self.Bind(wx.EVT_MENU, self.onAbrir, abrirMenuItem)
		exitMenuItem = fileMenu.Append(wx.NewId(), "Exit","Exit the application")
		self.Bind(wx.EVT_MENU, self.onExit, exitMenuItem)
		
		filtrosMenu = wx.Menu()
		grisesMenuItem = filtrosMenu.Append(wx.NewId(), "Grises","Open Image")
		self.Bind(wx.EVT_MENU, self.onGrises,grisesMenuItem)
		
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
	
	def onGrises(self,event):
		print "aqui va el filtro de grises"
		im = Image.open(self.filename)
		im = im.convert('LA')
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
			
if __name__ == "__main__":
	app = wx.App(False)
	frame = MyForm().Show()
	app.MainLoop()
