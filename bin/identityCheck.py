from tkinter import *
from winObj import Window
from accountView import accountView
import myCipher

class IdentityCheckWindow(Window):
	element = ""
	isOption = False
	triesCounter = 0

	def checkIdentity(self, psw):
		if myCipher.identityCheck(psw):
			self.destroy()
			if self.isOption:
				# TO DO
				print("DO SOMETHING HERE FOR THE MULTIPLE OPTIONS")
			else:
				accountView.makeAccountViewWindow(self.element, psw)
		else:
			self.triesCounter += 1
			if self.triesCounter > 4:
				self.destroy()

	def addInput(self, x, y):
		userInput = StringVar()
		inputBox = Entry(
		    self.canvas,
		    width = 20,
		    font = 'Helvetica 15',
		    bg = self.bgColor,
		    bd = 1,
		    fg = self.fontColor,
		    insertbackground = self.fontColor,
		    textvariable = userInput,
		    show = "●"
		    )
		inputBox.place(x=x, y=y)
		inputBox.focus_set()
		inputBox.bind("<Return>", lambda event, ui = userInput: self.checkIdentity(ui.get()))

	@staticmethod
	def makeIdentityCheckWindow(element, isOption, name = "Password Manager - Identity Check", x = 1400, y = 950, width = 300, height = 150, fontDim = 25, autoClose = True):
		icw = IdentityCheckWindow(name, x, y, width, height, fontDim, autoClose = autoClose)
		icw.setFocus()
		icw.element = element
		icw.isOption = isOption
		
		icw.addLabel(
			text = "ID CHECK",
			pos = True,
			yPos = 20
			)
		icw.addInput(38, 85)			
		return icw