from tkinter import *
from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox
from tkinter import font
import Config as cg
from PIL import ImageTk, Image
from resizeimage import resizeimage
from tkinter.ttk import Progressbar
import Queries as qr
import numpy as np
import Log as log
from ScrollableWidget import ScrollableWidget
from LoadingScreen import Splash
import Exceptions as exp

class MainWindow(Frame):
	'''
	This class is the main interface of Random Inventory Generator and is often referred to as the gui. Problems with
	interface could originate from here.
	'''
	def __init__(self, root, helper_random_table_gen=None, outLoc='', sql = None):
		Frame.__init__(self)
		self.super_root = root
		self.configure(bg='white')
		self.helper_random_table_gen = helper_random_table_gen
		self.outputFileLocation = outLoc
		self.sites_in_query = set()
		self.openOutputFolder = 0
		self.num_of_results = 15
		self.sql = sql
		'''column 0 -- selected, column 1 -- site location, column 2 --checkbox obj'''
		self.checkboxes_mat = np.empty([0,3])


	def setup(self, sql, helper_random_table_gen):
		self.create_widgets()
		self.setup_header_frame()
		self.setup_control_frame()
		self.setup_checkbox_canvas()
		self.setup_generate_results_frame()
		self.setup_footer_frame()

		gui = self
		gui.pack(fill=BOTH, expand=1)
		gui.set_sql(sql)
		gui.button_select_checkboxes_in_query()
		gui.set_helper_random_table_gen(helper_random_table_gen)

	###CREATING GUI WIDGETS#########################################################################################

	def create_widgets(self):
		'''
		Creates the outline frames for the respective widgets to be put in.
		:return:
		'''

		num_of_rows = 14

		self.header = Frame(self, bg='white')
		self.header.grid(row=0, column=0, columnspan=3, sticky='nsew', pady=4)

		self.leftMargin = Frame(self, bg='white', pady=4)
		self.leftMargin.grid(row=1, column=0, rowspan=num_of_rows-1, sticky='nsew')

		self.frame_selection_control = Frame(self, bg='white', pady=4)
		self.frame_selection_control.grid(row=1, column=1, sticky='nsew')

		self.frame_scrollable_widget = Frame(self, bg='white', pady=4)
		self.frame_scrollable_widget.grid(row=2, column=1, sticky='nsew')

		self.scrollable_widget_checkboxes = ScrollableWidget(self.frame_scrollable_widget, bg='white', pady=4)
		self.scrollable_widget_checkboxes.pack(fill=BOTH, expand=1)


		self.centerMid = Frame(self, bg='white', pady=4)
		self.centerMid.grid(row=3, column=1, sticky='nsew')

		self.rightMargin = Frame(self, bg='white', pady=4)
		self.rightMargin.grid(row=1, column=2, rowspan=num_of_rows, sticky='nsew')

		self.footer = Frame(self, bg='white', pady=4)
		self.footer.grid(row=10, column=0, columnspan=3, sticky='nsew')

		#Congfig of the weights as the window changes sizes
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=5)
		self.grid_columnconfigure(2, weight=1)
		self.grid_rowconfigure(0, weight=0)
		self.grid_rowconfigure(2, weight=10)
		self.grid_rowconfigure(3, weight=1)
		self.grid_rowconfigure(10, weight=0)

	def setup_header_frame(self):
		l = Label(self.header, bg='white', text="Random Inventory Audit Sheet Creator", font=font.Font(weight='bold'))
		l.pack(fill=BOTH)

	def setup_control_frame(self):
		self.frame_selection_control
		button_select_all = Button(self.frame_selection_control, text='Select All', command=self.button_select_all)
		button_select_all.grid(row=0, column=0)

		button_deselect_all = Button(self.frame_selection_control, text='Deselect All', command=self.button_deselect_all)
		button_deselect_all.grid(row=0, column=1)

		button_select_checkboxes_in_query = Button(self.frame_selection_control, text='Select Sites in Query',
		                                           command=self._button_select_checkboxes_in_query)
		button_select_checkboxes_in_query.grid(row=0, column=2)

		self.scrollable_widget_checkboxes.grid_rowconfigure(0, weight=2)

		entries_frame = Frame(self.frame_selection_control)
		entries_frame.grid(row=0, column=3, columnspan=2)
		entries_label = Label(entries_frame, bg='white', text='How many material numbers per site? ')
		entries_label.grid(row=0, column=0)
		self.entries = tk.Text(entries_frame, highlightbackground='black', highlightcolor='black', highlightthickness=1,
		                       height=1, width=10)
		self.entries.grid(row=0, column=1)
		self.entries.delete('1.0', END)
		self.entries.insert(END, '15')

		self.checkbox_sqrt_value = BooleanVar(False)
		checkbox_sqrt = Checkbutton(self.frame_selection_control, text='Decrease Possibility of High Value Materials', bg='white', variable=self.checkbox_sqrt_value)
		checkbox_sqrt.grid(row=1, column=0, columnspan=5, sticky='w')

		self.frame_selection_control.grid_columnconfigure(0, weight=1)
		self.frame_selection_control.grid_columnconfigure(1, weight=1)
		self.frame_selection_control.grid_columnconfigure(2, weight=1)
		self.frame_selection_control.grid_columnconfigure(3, weight=1)
		self.frame_selection_control.grid_rowconfigure(0, weight=1)
		self.frame_selection_control.grid_rowconfigure(1, weight=1)


	def setup_checkbox_canvas(self):
		row = 0
		self.scrollable_widget_checkboxes.get_parent().grid_propagate(True)

		for i in range(cg.get_site_location_length()):
			temp = tk.IntVar()
			text = cg.get_site_location_values()[i] + ' (' + cg.get_site_location_keys()[i] + ')'
			c = Checkbutton(self.scrollable_widget_checkboxes.get_parent(), bg='white', variable=temp, text=text)
			c.grid(row=row, column=i % 5, sticky='W')
			if i % 5 == 4:
				row += 1
			self.scrollable_widget_checkboxes.get_parent().grid_rowconfigure(row, weight=1)
			self.scrollable_widget_checkboxes.get_parent().grid_columnconfigure(i % 5, weight=1)
			self.add_to_checkbox_matrix(temp, cg.get_site_location_keys()[i], c)


	def setup_generate_results_frame(self):
		l3 = Label(self.centerMid, bg='white', padx=3, text='Output Save Location')
		l3.grid(row=0, column=0, sticky='w')
		self.textbox3 = tk.Text(self.centerMid, highlightbackground='black', padx=4, highlightcolor='black',
		                        highlightthickness=1, height=1)
		self.textbox3.grid(row=0, column=1, sticky='nsew')
		b2 = Button(self.centerMid, padx=3, text="Browse", command=self.callback3)
		b2.grid(row=0, column=2, sticky='e')

		b = tk.Button(self.centerMid, text="Generate Random Inventory Check", command=self.button_generate_rits,
		              height=1, justify=CENTER)
		b.grid(row=5, column=0, rowspan=4, columnspan=4, pady=7, sticky='nsew')

		self.bar = Progressbar(self.centerMid, orient=HORIZONTAL, mode='determinate')
		self.bar.grid(row=10, column=0, columnspan=3, sticky='ew')

		self.centerMid.grid_columnconfigure(1, weight=1)

	def setup_footer_frame(self):
		try:
			image = Image.open(cg.EDPR_logo_location)
			width, height = image.size
			width = int(width / 5)
			height = int(height / 5)
			image = resizeimage.resize_cover(image, [width, height])
			img = ImageTk.PhotoImage(image)
			label = tk.Label(self.footer, image=img, bg='white')
			label.image = img
			label.pack()
		except:
			print('Footer logo could not be found')

	def setup_scrollbar_for_checkbox_canvas(self, num_rows):
		myscrollbar = Scrollbar(self.scrollable_widget_checkboxes, orient="vertical", command=self.scrollable_widget_checkboxes.yview)
		self.scrollable_widget_checkboxes.configure(yscrollcommand=myscrollbar.set)
		myscrollbar.grid(row=0, column=2, rowspan=num_rows, sticky='ns')
		self.scrollable_widget_checkboxes.config(yscrollcommand=myscrollbar.set)

	###ACTION FUNCTION##############################################################################################

	#Button functions
	def callback3(self):
		self.filename = filedialog.askdirectory()
		self.textbox3.delete('1.0', END)
		self.textbox3.insert(tk.END, self.filename)

	def button_generate_rits(self):
		print(self.checkbox_sqrt_value.get())
		if not self.output_location_ready():
			self.error_message(title="Error", message="Please input a valid output location.")
		elif not self.site_selected():
			self.error_message(title='Error', message='Please select a site')
		else:
			log.setup(self.get_output_location())
			log.message('start: generate random inventory tables button has been pushed')
			self._button_generate_rits()
			log.message('end: generate random inventory table button')

	# Generate buttons helper functions
	def _button_generate_rits(self):
		try:
			self.helper_random_table_gen.reset_progressbar()
			self.prepare_and_execute_table_gen()
		except PermissionError:
			self.gui.error_message(title='Writing Permission Denied',
			                       message='Please close all excels, as there was an error in writing an the excel files. ')
			log.error_message('Permission was denied to one or more when writing an excel. Rerun the generation.')
		except ValueError:
			self.error_message(title='Error',
			                   message='Please enter a number in the field \'How many material numbers per site?\'')
			log.error_message('Could not convert output number to a string')
		except exp.EmptyGeneration as ex:
			self.error_message(title='No SQL Data', message=str(ex))
			log.error_message(str(ex))
		# except Exception as ex:
		# 	self.error_message(title='Unknown Error', message=str(ex))
		# 	log.error_message(str(ex))


	def output_location_ready(self):  # makes sure the output file is not empty
		return self.get_output_location() != ''

	def site_selected(self):
		for i in self.checkboxes_mat[:,0]:
			if i.get() == 1:
				return True
		return False

	def selected_sites_not_in_query(self, sitesFromQuery, sitesFromSelected):  # determines whether the user has selected sites that are not in the query
		sitesFromQuery, sitesFromSelected = set(sitesFromQuery), set(sitesFromSelected)
		diff = sitesFromSelected - sitesFromQuery
		if not len(diff) == 0:
			message = 'There are sites you have selected that are not contained in the query data. Those selected sites will be skipped.\n\nThe following sites will not be included:'
			for x in diff:
				message += '\n' + cg.site_location[x] + ' (' + x + ')'
			messagebox.showwarning(title='Warning: Selected items not in query', message=message)
		out = sitesFromSelected - diff
		return list(out)

	def prepare_and_execute_table_gen(self):
		selectedSites = self.selected_sites_not_in_query(sitesFromQuery=self.get_sites_in_query(),
		                                             sitesFromSelected=self.get_user_selected_checkboxes())
		if not len(selectedSites) > 0:
			raise exp.EmptyGeneration('None of the selected sites are contained in within the SQL database.')
		self.helper_random_table_gen.final_setup(selectedSites, self.get_output_location(), self.get_number_entries_in_output(), self.checkbox_sqrt_value.get())
		self.helper_random_table_gen.generate_tables()

	def button_select_all(self):
		for x in self.checkboxes_mat[:,2]:
			x.select()


	def button_deselect_all(self):
		for x in self.checkboxes_mat[:,2]:
			x.deselect()


	def _button_select_checkboxes_in_query(self):
		loading = Splash(self.super_root)
		self.button_select_checkboxes_in_query()
		loading.destroy()


	def button_select_checkboxes_in_query(self):
		if self.sql is None:
			raise Exception('SQL has not been intiazied in the GraphUI Class')
		df = self.sql.query_and_export(qr.get_query_text_sites_in_data_more_than_x(15))
		self.sites_in_query = df.iloc[:,0].to_numpy()
		self.button_deselect_all()
		for i in range(np.size(self.checkboxes_mat, 0)):
			if self.checkboxes_mat[i, 1] in self.sites_in_query:
				self.checkboxes_mat[i, 2].select()

	#UTILTY FUNCTIONS
	def warning(self, title, message):
		messagebox.showwarning(title=title, message=message)

	def error_message(self, title, message):
		messagebox.showerror(title=title, message=message)

	def message(self, title, message):
		messagebox.showinfo(title=title, message=message)

	def add_to_checkbox_matrix(self, selected, sap_plant, checkbox_object):
		self.checkboxes_mat = np.vstack((self.checkboxes_mat, np.array([selected, sap_plant, checkbox_object])))

	#SETTERS and GETTERS
	def set_helper_random_table_gen(self, helper_random_table_gen):
		self.helper_random_table_gen = helper_random_table_gen

	def get_user_selected_checkboxes(self):  # determines which sites have been selected by the user via the checkboxes
		out = []
		for i in range(np.size(self.checkboxes_mat, 0)):
			if self.checkboxes_mat[i][0].get() == 1:
				out.append(self.checkboxes_mat[i][1])
		return out

	def get_sites_in_query(self):
		return self.sites_in_query

	def get_output_location(self): #gets the output location for the excel for the files. input by the user
		temp = self.textbox3.get("1.0", END)
		temp = temp.strip()
		return temp

	def get_number_entries_in_output(self):
		temp = self.entries.get("1.0", END)
		temp = temp.strip()
		converted_int = int(temp)
		if (converted_int <= 0):
			self.error_message(title='Error', message='You have to have a number less than 0 in the field \'How many material numbers per site?\'')
		return converted_int



	def set_sql(self, sql):
		self.sql = sql

