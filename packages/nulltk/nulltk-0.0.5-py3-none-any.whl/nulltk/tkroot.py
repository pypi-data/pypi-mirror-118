import tkinter as tk
from .style import Style

class Tk(tk.Tk):
    def __init__(self, *args, style=Style(), **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        style.apply(self)
