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
                #filtro sepia
                histogramaMenuItem = filtrosMenu.Append(wx.NewId(), "Histograma","Histograma")
                self.Bind(wx.EVT_MENU, self.onHistograma,histogramaMenuItem)

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

        def onHistograma(self,event):
                im = Image.open(self.filename)
                # donde t es el tamanio del efecto
                im,imbak = Image.open(self.filename).convert('RGB'),Image.open(self.filename).convert('RGB')
                pixels,pixelsbak = im.load(),imbak.load()
                ancho,alto = im.width,im.height
                cuenta,tam = [], ancho*alto
                for i in range(0,256):  cuenta.append(0)
                l = 256
                for i in range(0,ancho):
                        for j in range(0,alto):
                                r,g,b = pixels[i,j]
                                newp = (r+g+b)/3
                                pixels[i,j] = (newp,newp,newp)
                                cuenta[newp] = cuenta[newp] + 1
                for i in range(0,ancho):
                        for j in range(0,alto):
                                r,g,b = pixels[i,j]
                                newp = r
                                sum = 0
                                for k in range(0,newp):
                                        sum+=(float(cuenta[k])/tam)
                                np = int(floor((l-1)*sum))
                                pixelsbak[i,j] = (np,np,np)
                image = wx.EmptyImage(imbak.size[0], imbak.size[1])
                new_image = imbak.convert('RGB')
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

if __name__ == "__main__":
        app = wx.App(False)
        frame = MyForm().Show()
        app.MainLoop()

