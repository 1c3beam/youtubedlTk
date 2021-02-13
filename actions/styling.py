from tkinter import ttk
from youtubedltk import UI
class Styling(UI):
    def __init__(self, master):
        super().__init__(master)
        style=ttk.Style()
        # grid config
        # self.url_frame.grid_configure(pady=10,
        # sticky='w',
        # padx=8
        # )
        # self.url_subframe.grid_configure(sticky='w',
        # padx=8,
        # )
        # self.framebtn.grid_configure(sticky='w')
        # self.pauseallbtn.pack_configure(
        #     ipady=7
        #     )
        # self.pausebtn.pack_configure(
        #     pady=7
        #     )
        # self.removebtn.pack_configure(
        #     pady=7
        #     )
        # self.startbtn.pack_configure(
        #     pady=7
        #     )
        
        # style config
        self.url_frame.config(style='urlframe.TFrame')
        self.url_subframe.config(style='urlsubframe.TFrame')
        self.addbtn.config(style='addbtn.TButton')
        
        
        # styles
        style.theme_use('clam')
        style.configure('urlframe.TFrame',
        padding=10
        )
        style.configure('urlsubframe.TFrame',
        padding=10, width=100
        )
        
        style.configure('TButton',
        padding=3)