from tkinter import *
from winObj import Window
from identityCheck import IdentityCheckWindow
import jsonFunctions

class SearchBar(Window):
	listBox = None
	listBoxB = None

	optionSpecialChar = "." 
	elementDisplayedList = []
	elementImgList = []
	options = jsonFunctions.openOptionsData()["options"]

	def __searchingForOptions(self, ui):
		if len(ui)>0:
			if ui[0] == self.optionSpecialChar:
				return True
		return False

	def __searchOptions(self, ui):
		opt = ui[1:].lower()
		optList = []
		if len(opt) == 0:
			for o in self.options:
				optList.append(o)
		else:
			for o in self.options:
				if opt in o["name"].lower():
					if o["name"] not in optList:
						optList.append(o)
				else:
					for a in o["alias"]:
						if opt in a and o not in optList:
							optList.append(o)
		return optList

	def __emptyDisplayedList(self):
		for e in self.elementDisplayedList:
			e.destroy()
		for i in self.elementImgList:
			i.destroy()

	def __clickEvent(self, e):
	    self.destroy()
	    if e in self.options:
	    	IdentityCheckWindow.makeIdentityCheckWindow(e, True)	    
	    else:
	    	IdentityCheckWindow.makeIdentityCheckWindow(e, False)	 
	
	def __enterEvent(self, ui):
		if self.__searchingForOptions(ui):
			l = self.__searchOptions(ui)
		else:
		    l = self.__searchingAccount(ui)
		if len(l) > 0:
			self.__clickEvent(l[0])

	def __searchingAccount(self, name):
	    accountsFound = []
	    if name == "":
	        return accountsFound
	    for a in self.accounts["accountDetails"]:
	        if name.lower() in a["name"].lower():
	        	accountsFound.append(a)
	    return accountsFound

	def __searchDisplayArea(self, n):
	    if n == 0:
	        return
	    self.listBoxB = self.round_rectangle(0, 25+68, 673, 25+(68*n)+68, color = self.secondColor)
	    self.listBox = self.round_rectangle(1, 26+68, 672, 25+(68*n)+67, color = self.bgColor)

	def __displayElement(self, element, pos):
	    f = Frame(
	        self.canvas,
	        height = 66,
	        bg = self.bgColor,
	        width = 671,
	        )
	    f.pack_propagate(0)
	    f.place(x = 1, y = 94+68*pos)
	    
	    elementBox = self.addLabel(element["name"], 70, 15, root = f)

	    img = self.addImage(
	    	path = element["img"],
	    	x = 19,
	    	y = 15,
	    	root = f
	    	)
	    self.elementImgList.append(img)
	    img.winfo_children()[0].bind("<Button-1>", lambda event, e = element: self.__clickEvent(e))

	    elementBox.bind("<Button-1>", lambda event, e = element: self.__clickEvent(e))
	    f.bind("<Button-1>", lambda event, e = element: self.__clickEvent(e))
	    return f

	def __displayElements(self, elementList):
	    pos = 0
	    self.__emptyDisplayedList()
	    for e in elementList[:3]:
	        self.elementDisplayedList.append(self.__displayElement(e, pos))
	        pos+=1

	def __search(self, ui):
	    self.canvas.delete(self.listBoxB)
	    self.canvas.delete(self.listBox)
	    if self.__searchingForOptions(ui):
	    	l = self.__searchOptions(ui)
	    else:
		    l = self.__searchingAccount(ui)
	    self.__searchDisplayArea(len(l[:3]))
	    self.__displayElements(l)


	def addInput(self, x, y):
		userInput = StringVar()
		userInput.trace("w", lambda name, index, mode, ui = userInput: self.__search(ui.get().strip()))
		inputBox = Entry(
		    self.canvas,
		    width = 38,
		    font = self.font,
		    bg = self.bgColor,
		    bd = 0,
		    fg = self.fontColor,
		    insertbackground = self.fontColor,
		    textvariable = userInput
		    )
		inputBox.place(x=x, y=y)
		inputBox.focus_set()
		inputBox.bind("<Return>", lambda event, ui = userInput: self.__enterEvent(ui.get().strip()))

	@staticmethod
	def makeSearchBar(name = "Password Manager - SearchBar", x = 623, y = 307, width = 673, height = 373, fontDim = 20, innerHeight = 68, autoClose = True):
		s = SearchBar(name, x, y, width, height, fontDim, innerHeight, autoClose = autoClose)
		s.accounts = jsonFunctions.openAccountsData()
		s.addInput(
			x = 20,
			y = 17
			)
		s.addImage(
			path = "icons/search.png",
			x = 620,
			y= 17
			)
		return s
