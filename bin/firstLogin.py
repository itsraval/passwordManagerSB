# graphic interface
# input box for password
# generate json with password and format
# check if the json file already exists -> if so display msg file already exits
import myCipher
import jsonFunctions
from searchbar import SearchBar
from winObj import Window
from tkinter import *

class FirstLogin(Window):

  def createAccountsDataFile(self, psw):
    k = myCipher.pbkdf2(psw)
    jsonFunctions.createAccountsData(k)
    self.destroy()
    SearchBar.makeSearchBar()

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
    inputBox.bind("<Return>", lambda event, ui = userInput: self.createAccountsDataFile(ui.get()))

  @staticmethod
  def makeFirstLogin(name = "Password Manager - First Login", x = 810, y = 500, width = 300, height = 170, fontDim = 25, autoClose = True):

    fl = FirstLogin(name, x, y, width, height, fontDim, autoClose = autoClose)
    fl.setFocus()
    
    fl.addLabel(
      text = "Password Manager\nset your password",
      pos = True,
      yPos = 20
      )
    fl.addInput(38, 125)      
    return fl