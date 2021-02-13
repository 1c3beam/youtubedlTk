from tkinter import *
from youtubedltk import UI
from actions.styling import Styling
if __name__ == '__main__':
    root=Tk()
    ui=UI(root)
    style=Styling(root)
    root.mainloop()