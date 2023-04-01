from tkinter import *
from PIL import ImageTk, Image 
import util
import jsonFunctions

class Window:
	focus = 0
	settings = jsonFunctions.openSettingsData()
	bgColor = settings["graphics"]["bgColor"]
	font = settings["graphics"]["font"]
	fontColor = settings["graphics"]["fontColor"]
	removeColor = settings["graphics"]["removeColor"]
	secondColor = settings["graphics"]["iconColor"]
	images = []
	
	def __focus_in(self, event):
		self.focus += 1

	def __focus_out(self, event):
	    self.focus -= 1
	    if self.focus == 0:
	        self.window.destroy()

	def round_rectangle(self, x1, y1, x2, y2, radius=8, color=fontColor, **kwargs):
	        points = [x1+radius, y1,
	                x1+radius, y1,
	                x2-radius, y1,
	                x2-radius, y1,
	                x2, y1,
	                x2, y1+radius,
	                x2, y1+radius,
	                x2, y2-radius,
	                x2, y2-radius,
	                x2, y2,
	                x2-radius, y2,
	                x2-radius, y2,
	                x1+radius, y2,
	                x1+radius, y2,
	                x1, y2,
	                x1, y2-radius,
	                x1, y2-radius,
	                x1, y1+radius,
	                x1, y1+radius,
	                x1, y1]
	        return self.canvas.create_polygon(points, **kwargs, smooth=True, fill=color)

	def __init__(self, name, x, y, width, height, fontDim, innerHeight = None, autoClose = False):
		if innerHeight == None:
			innerHeight = height
		self.smallerFont = self.font + " " + str(fontDim-6)
		self.font = self.font + " " + str(fontDim)
		self.window = Tk(className = name)
		self.window.overrideredirect(True)
		self.window.geometry(str(width) + "x" + str(height) + "+" + str(x) + "+" + str(y))
		self.window.configure(bg = self.removeColor)
		self.window.attributes("-transparentcolor", self.removeColor)
		self.window.resizable(width = 0, height = 0)
		if autoClose:
			self.window.bind("<FocusIn>", self.__focus_in)
			self.window.bind("<FocusOut>", self.__focus_out)

		self.canvas = Canvas(
		    self.window,
		    bg = self.removeColor,
		    highlightthickness = 0,
		    )
		self.canvas.pack(fill = BOTH, expand = 1)

		self.round_rectangle(0, 0, width, innerHeight, color = self.secondColor) # light border
		self.round_rectangle(1, 1, width-1, innerHeight-1, color = self.bgColor) # main

	def addImage(self, path, x, y, root = None, width = 37, height = 37):
		if root == None:
			root = self.canvas
		if util.imageIsSet(path):
			img_path = path
		else:
			img_path = "icons/accounts/default-logo.png"
		i = Image.open(img_path)
		img = ImageTk.PhotoImage(i.resize((width, height), Image.ANTIALIAS))
		self.images.append(img)
		frameIMG = Frame(root)
		frameIMG.place(x=x, y=y)
		labelIMG = Label(
		    frameIMG,
		    image = img,
		    bg = self.bgColor,
		    borderwidth = 0,
		    highlightthickness = 0
		    )
		labelIMG.pack(side = RIGHT)
		return frameIMG

	def addLabel(self, text, x = -1 , y = -1, root = None, pos = False, yPos = 5):
		if root == None:
			root = self.canvas
		l = Label(
			root,
			font = self.font,
			fg = self.fontColor,
	        bg = self.bgColor,
	        text = text
			)
		if pos:
			l.pack(fill='both', pady = yPos, padx = 2)
		elif x != -1 and y != -1:
			l.place(x = x, y = y)
		return l

	def addSmallerLabel(self, text, x = -1 , y = -1, root = None, pos = False, yPos = 5):
		if root == None:
			root = self.canvas
		l = Label(
			root,
			font = self.smallerFont,
			fg = self.fontColor,
	        bg = self.bgColor,
	        text = text
			)
		if pos:
			l.pack(fill='both', pady = yPos, padx = 2)
		elif x != -1 and y != -1:
			l.place(x = x, y = y)
		return l

	def destroy(self):
		self.window.destroy()

	def display(self):
		self.window.mainloop()

	def setFocus(self):
		self.window.after(1, lambda: self.window.focus_force())