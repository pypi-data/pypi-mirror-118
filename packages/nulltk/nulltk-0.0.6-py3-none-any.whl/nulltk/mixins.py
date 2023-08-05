import tkinter as tk

def Reactive(obj):
	activebg = obj.option_get('activeBackground', '')
	activefg = obj.option_get('activeForeground', '')
	obj.prevBG = obj['background']
	try:
		obj.prevFG = obj['foreground']
	except tk.TclError: pass

	def on_enter(e):
		obj.prevBG = obj['background']
		obj['background'] = activebg
		if hasattr(obj,'prevFG'):
			obj.prevFG = obj['foreground']
			obj['foreground'] = activefg

	def on_leave(e):
		obj['background'] = obj.prevBG
		if hasattr(obj,'prevFG'):
			obj['foreground'] = obj.prevFG

	obj.bind("<Enter>", on_enter)
	obj.bind("<Leave>", on_leave)

	return obj
