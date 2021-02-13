from tkinter import ttk
from youtubedltk import UI
class Styling(UI):
    def __init__(self, master):
        super().__init__(master)
        style=ttk.Style()
        # styles
        style.theme_use('clam')
        style.configure(
            'TFrame', padding=(5, 5), relief='flat'
            )
        style.configure(
            'Treeview', highlightthickness=0, bd=0, font=('Helvetica', 11),
            )