import tkinter as tk
from .color import Color
from .mixins import Reactive

class TabbedFrame(tk.Frame):
	def __init__(self, *args, tabs: list, **kwargs):
		tk.Frame.__init__(self, *args, **kwargs)

		fg_hex = self.option_get('foreground','Foreground')
		bg_hex = self.option_get('background','Background')
		if fg_hex == '': fg_hex = '#000000'
		if bg_hex == '': bg_hex = '#ffffff'

		self.fg_color = Color.from_hex(fg_hex)
		self.bg_color = Color.from_hex(bg_hex)

		topbar = tk.Frame(self)
		self._elements = {}
		self._tabs = {}
		for tabname in tabs:
			buttonframe = tk.Frame(topbar)
			button = Reactive(tk.Button(buttonframe, anchor=tk.W, text=tabname, command=lambda arg=tabname: self.on_button(arg)))
			underline = tk.Frame(buttonframe,
				height=2,
				background = self.option_get('foreground','Foreground')
			)
			button.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
			underline.pack(side=tk.BOTTOM, anchor=tk.S, fill=tk.X, expand=True)
			self._tabs[tabname] = tk.Frame(self)
			self._elements[tabname] = (underline, button)
			buttonframe.pack(side=tk.LEFT, anchor=tk.W, fill=tk.BOTH, expand=True)
		topbar.pack(side=tk.TOP, fill=tk.X, expand=True)

		self.on_button(tuple(tabs)[0])

	def on_button(self, tabname):
		for (name, frame), (spacer, button) in zip(self._tabs.items(), self._elements.values()):
			if name != tabname:
				frame.pack_forget()
				spacer.config(background=self.fg_color.as_hex(), height=1)
				button.config(foreground=self.fg_color.as_hex())
			else:
				frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
				spacer.config(background=self.fg_color.lighter().as_hex(), height=2)
				button.config(foreground=self.fg_color.lighter().as_hex())

	def tab_frames(self):
		return tuple(self._tabs.values())

	def tab_frame(self, index):
		return self.tab_frames()[index]

	def tabs(self):
		return tuple(self._tabs.values())
