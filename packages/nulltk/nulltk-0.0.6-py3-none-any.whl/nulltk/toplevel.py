import tkinter as tk

class Toplevel(tk.Toplevel):
	def __init__(self, *args, **kwargs):
		tk.Toplevel.__init__(self, *args, **kwargs)
