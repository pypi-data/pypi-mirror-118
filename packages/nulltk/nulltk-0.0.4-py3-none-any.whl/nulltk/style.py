import tkinter as tk
from . import colors

def make_reactive(obj, activebg, activefg):
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

def style(widget, **kwargs):

    bg=colors.DarkGray.darker().darker()
    fg=colors.Aquamarine
    activebg=colors.DarkGray.darker()
    activefg=fg.lighter()
    bd=0
    highlightthickness=0
    insertbackground=colors.White

    widget.option_add("*background", bg.as_hex())
    widget.option_add("*foreground", fg.as_hex())
    widget.option_add("*activeBackground", activebg.as_hex())
    widget.option_add("*activeForeground", activefg.as_hex())
    widget.option_add("*insertBackground", insertbackground.as_hex())
    widget.option_add("*borderWidth", bd)
    widget.option_add("*Canvas*highlightThickness", highlightthickness)
    widget.option_add("*relief", tk.FLAT)

    if widget.__class__.__name__ in ('Button','Label',):
        make_reactive(widget, activebg, activefg)
    
    for child in widget.children.values(): style(child)
