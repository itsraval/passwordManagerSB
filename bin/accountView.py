from tkinter import *
from PIL import ImageTk, Image 
from winObj import Window
import util
import myCipher
from timer import logOutTimer

class accountView(Window):
	pswVisibility = False

	def __close(self):
		self.destroy()
		util.stopProcess()

	## TO DO
	def __edit_account(self, account):
		return 

	def __change_password_field(self, psw_field, psw):
		self.t.reset()
		if self.pswVisibility:
			psw_field.config(text = psw)
		else:
			psw_field.config(text = util.dotPassword(psw))
		return

	def __cp_psw_press(self, imgLabel):
		self.t.reset()
		i = Image.open("icons/copy_psw - press.png")
		pic = ImageTk.PhotoImage(i.resize((30, 30), Image.ANTIALIAS))
		imgLabel.config(image=pic)
		imgLabel.image = pic

	def __cp_psw_release(self, imgLabel, psw):
		util.copyToClipboard(psw)
		i = Image.open("icons/copy_psw.png")
		pic = ImageTk.PhotoImage(i.resize((30, 30), Image.ANTIALIAS))
		imgLabel.config(image=pic)
		imgLabel.image = pic

	def __cp_user_press(self, imgLabel):
		self.t.reset()
		i = Image.open("icons/copy_user - press.png")
		pic = ImageTk.PhotoImage(i.resize((30, 30), Image.ANTIALIAS))
		imgLabel.config(image=pic)
		imgLabel.image = pic

	def __cp_user_release(self, imgLabel, user):
		util.copyToClipboard(user)
		i = Image.open("icons/copy_user.png")
		pic = ImageTk.PhotoImage(i.resize((30, 30), Image.ANTIALIAS))
		imgLabel.config(image=pic)
		imgLabel.image = pic

	def __visibility(self, psw_field, visON, visOFF, account, psw):
		if self.pswVisibility:
			visON.place_forget()
			visOFF.place(x = 135, y = 270)
			self.pswVisibility = False
		else:
			visON.place(x = 135, y = 270)
			visOFF.place_forget()
			self.pswVisibility = True
		self.__change_password_field(psw_field, psw)
		return

	@staticmethod
	def makeAccountViewWindow(account, key, name = "Password Manager - Account", x = 1400, y = 790, width = 300, height = 350, fontDim = 20):
		aw = accountView(name, x, y, width, height, fontDim)
		if (account["password"] != ""):
			psw = myCipher.decrypt(account["password"], key)
		else:
			psw = ""
		img = aw.addImage(
			path = account["img"],
			x = 117.5,
			y = 20,
			width = 65,
			height = 65
			)
		name = aw.addLabel(
			text = account["name"],
			pos = True,
			yPos = 100
			)
		if account["url"] != "":
			img.winfo_children()[0].bind("<ButtonPress-1>", lambda event, url = account["url"]: util.openLink(url))
			name.bind("<ButtonPress-1>", lambda event, url = account["url"]: util.openLink(url))
		if len(account["user"])>32:
			aw.addSmallerLabel(
				text = account["user"].split("@")[0],
				x = 15,
				y = 150
				)
			aw.addSmallerLabel(
				text = "@" + account["user"].split("@")[1],
				x = 80,
				y = 180
				)
			psw_field = aw.addSmallerLabel(
				text = util.dotPassword(psw),
				x = 15,
				y = 220
				)
		else:
			aw.addSmallerLabel(
				text = account["user"],
				x = 15,
				y = 150
				)
			psw_field = aw.addSmallerLabel(
				text = util.dotPassword(psw),
				x = 15,
				y = 200
				)
			
		copy_user = aw.addImage(
			path = "icons/copy_user.png",
			x = 85,
			y = 270,
			width = 30,
			height = 30
			)
		copy_user.winfo_children()[0].bind("<ButtonPress-1>", lambda event, copy_user = copy_user.winfo_children()[0]: aw.__cp_user_press(copy_user))
		copy_user.winfo_children()[0].bind("<ButtonRelease-1>", lambda event, copy_user = copy_user.winfo_children()[0], user = account["user"]: aw.__cp_user_release(copy_user, user))
			

		visON = aw.addImage(
			path = "icons/visibility_ON.png",
			x = 135,
			y = 270,
			width = 30,
			height = 30
			)
		visOFF = aw.addImage(
			path = "icons/visibility_OFF.png",
			x = 135,
			y = 270,
			width = 30,
			height = 30
			)
		visON.place_forget()
		visON.winfo_children()[0].bind("<Button-1>", lambda event, a = account, psw = psw, psw_field = psw_field, visON = visON, visOFF = visOFF: aw.__visibility(psw_field, visON, visOFF, a, psw))
		visOFF.winfo_children()[0].bind("<Button-1>", lambda event, a = account, psw = psw, psw_field = psw_field, visON = visON, visOFF = visOFF: aw.__visibility(psw_field, visON, visOFF, a, psw))
		
		copy_psw = aw.addImage(
			path = "icons/copy_psw.png",
			x = 185,
			y = 270,
			width = 30,
			height = 30
			)
		copy_psw.winfo_children()[0].bind("<ButtonPress-1>", lambda event, copy_psw = copy_psw.winfo_children()[0]: aw.__cp_psw_press(copy_psw))
		copy_psw.winfo_children()[0].bind("<ButtonRelease-1>", lambda event, copy_psw = copy_psw.winfo_children()[0], psw = psw: aw.__cp_psw_release(copy_psw, psw))

		edit_account = aw.addImage(
			path = "icons/edit.png",
			x = 240,
			y = 315,
			width = 25,
			height = 25
			)
		edit_account.winfo_children()[0].bind("<Button-1>", lambda event, a = account: aw.__edit_account(a))
		close = aw.addImage(
			path = "icons/close.png",
			x = 270,
			y = 315,
			width = 25,
			height = 25
			)
		close.winfo_children()[0].bind("<Button-1>", lambda event: aw.__close())
		aw.t = logOutTimer(aw.settings["security"]["logOutTimer"])
		return aw