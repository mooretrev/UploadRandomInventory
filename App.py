import tkinter as tk
import Config as cg
from SQLServerConnect import SQL
import GenerateRandomTables as grt
import pyodbc
from GraphUI import MainWindow
import Log as log
from LoadingScreen import Splash
from tkinter import messagebox

class App(tk.Tk):
	def __init__(self):
		'''
		Main setup up for the Random Table Generator program. All of items needed for the program to run
		are created here such as SQL server connection, gui setup, and the Random Table Generator.
		'''

		tk.Tk.__init__(self)

		self.withdraw()
		loading_screen = Splash(self)

		self.title('Random Inventory Generator')
		self.configure(background='white')
		try:
			self.iconbitmap(cg.icon_location)
		except Exception:
			print('Icon could not be found')

		try:
			sql = SQL()
			gui = MainWindow(self)
			helper_random_table_gen = grt.GenerateRandomTables()

			cg.setup(sql)
			gui.setup(sql, helper_random_table_gen)
			helper_random_table_gen.intial_setup(sql, gui)

		except pyodbc.Error as ex:
			message = 'There was an error connecting to SQL server.\n\nError Message:'
			message += ex.args[1]
			message += '\n\nExiting now.'
			messagebox.showerror(title='Error in connection to SQL server', message=message)
			exit()
		# except:
		# 	messagebox.showerror(title='Unknown Error', message='Error occured due to a unknown reason. Exiting now. Caught in app.')
		# 	exit()

		loading_screen.destroy()
		self.update()
		self.minsize(self.winfo_reqwidth(), self.winfo_reqheight()) #set the min size of the window

		self.deiconify()
		self.mainloop() #nothing can be called after this. This puts the gui in the infinite loop

	def destroy(self):
		'''
		Overrides the parent function. This method is called when the gui is closed. Therefore, it is used
		close the log file.
		'''
		super().destroy()
		log.close_file()
