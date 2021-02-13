from tkinter import *
from actions.styling import Styling
if __name__ == '__main__':
    root=Tk()
    # this Styling inherits from UI which contain the
    # actual UI
    style=Styling(root)
    root.mainloop()