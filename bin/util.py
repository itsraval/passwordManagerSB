from os.path import exists
from os import makedirs
import os
import pyperclip
import webbrowser
import shutil
from tkinter import filedialog
import jsonFunctions

def stopProcess():
	os._exit(1)

def imageIsSet(path):
	return exists(path)

def dotPassword(str):
	return "●" * len(str)

def copyToClipboard(str):
	pyperclip.copy(str)

def openLink(url):
	webbrowser.open(url, new=0, autoraise=True)
	return

def path_exists():
	dirs = ["icons\\accounts"]
	files = [jsonFunctions.accountsPath]
	for d in dirs:
		if not exists(d):
			makedirs(d)
	for f in files:
		if not exists(f):
			return False
	return True

def copy_file(src, dst, filename):
	f = "."+src.split(".")[-1]
	shutil.copyfile(src, dst + filename + f)
	return dst + filename + f

def import_picture(filename):
	f_path = filedialog.askopenfilename(filetypes=[("Images", ".png .jpg .jpeg")])
	path = "icons/accounts/"
	return copy_file(f_path, path,filename)