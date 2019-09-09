import tkinter as tk
from tkinter.ttk import Progressbar
from PIL import ImageTk, Image
import Config as cg

class Splash(tk.Toplevel):
	'''
	Loading screen that shows when application starts and when the button select sites in query is pressed
	'''
	def __init__(self, parent):
		self.root = parent
		tk.Toplevel.__init__(self, parent)
		self.height, self.width = 350, 300
		self.title("Loading")
		self.geometry('{}x{}'.format(self.width, self.height))
		self.configure(bg='white')
		self.create_frames()
		try:
			self.iconbitmap(cg.icon_location)
		except Exception:
			print('Icon could not be found')

		self.update()

	def create_frames(self):
		logo_frame = tk.Frame(self, height=self.height * 0.85, width=self.width, bg = 'white')
		logo_frame.pack()
		try:
			image = Image.open(cg.icon_location)
			img = ImageTk.PhotoImage(image)
			label = tk.Label(logo_frame, image=img, height=self.height * 0.85, width=self.width, bg='white')
			label.image = img
			label.pack()
		except:
			print('Loading Logo Could not be found')
		logo_frame.pack_propagate(False)

		loading_frame = tk.Frame(self, height=self.height * 0.15, width=self.width, bg ='white')
		loading_frame.pack()
		wait_label = tk.Label(loading_frame, text='Loading, please wait.', bg='white')
		wait_label.pack()

	def start(self):
		self.mainloop()