import tkinter as tk

class ScrollableWidget(tk.Frame):
	def __init__(self, root, **options):
		tk.Frame.__init__(self, root, **options)

		self.canvas = tk.Canvas(root, borderwidth=0, background='white', bd=0, highlightthickness=0, relief='ridge')
		self.frame = tk.Frame(self.canvas, background='white', height=100, width=100)

		self.vsb = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview, bd=0, highlightthickness=0, relief='ridge', borderwidth=0)
		self.vsb.pack(side="right", fill="y")

		self.canvas.pack(side="left", fill="both", expand=True)
		temp = self.canvas.create_window((0, 0), window=self.frame, tags="self.frame", anchor='center', tag='window')
		self.canvas.configure(yscrollcommand=self.vsb.set)
		print(temp)

		#grid manager weigth config
		self.grid_rowconfigure(0,weight=1)
		self.grid_columnconfigure(0, weight=1)
		self.canvas.grid_columnconfigure(0, weight=1)
		self.canvas.grid_rowconfigure(0, weight=1)

		#key bindings
		self.canvas.bind('<Configure>', self._on_canvas_config)
		self.frame.bind("<Configure>", self._on_frame_config)
		self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

	def get_parent(self):
		return self.frame

	def _on_mousewheel(self, event):
		self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

	def _on_frame_config(self, event):
		'''Reset the scroll region to encompass the inner frame'''
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))

	def _on_canvas_config(self, event):
		'''.configure(height=event.height, width=event.width)'''
		self.update()
		self.update_idletasks()
		self.frame.grid_propagate(False)
		self.frame.configure(height=self.canvas.winfo_height(), width=self.canvas.winfo_width())







