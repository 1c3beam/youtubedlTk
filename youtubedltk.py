from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import subprocess as sp
import threading as th
import os
import sys
from time import sleep
import json
from actions.actions import Actions
from actions.callbacks import CallBacks

class UI(Actions, CallBacks):

    def __init__(self, master):
        self.base_dir=os.getcwd()
        # Frame for Url
        self.url_frame=Frame(master, relief=SUNKEN).grid(
            row=0, column=3)
        
        self.url_entry=ttk.Entry(self.url_frame, width=80)
        self.url_entry.grid(
            row=0, column=0, columnspan=4, rowspan=2
            )
        self.url_entry.insert(0, 'Paste Url Here')
        
        # Destination
        self.dest=ttk.Combobox(self.url_frame,
        text='')
        self.dest.grid(
            row=4, column=0
            )
        self.dest.insert(0, 'Select Destination ....')
        self.dest.state(['readonly'])
        
        # Adds Url
        self.addbtn=ttk.Button(self.url_frame,
        text='Add', command=self._addBtn)
        self.addbtn.grid(
            row=4, column=1
            )
        
        # Select a format
        self.formats=ttk.Combobox(self.url_frame, values=(
            'mp4', 'mp3', 'wma'))
        self.formats.grid(
            row=4, column=2
            )
        self.formats.insert(0, 'Select Format')
        self.formats.state(['readonly'])
        
        # Info Box
        self.info_frame=ttk.Frame(master).grid(
            row=5, column=0
            )
        # self.scroll_bar=ttk.Scrollbar(self.info_frame, orient='vertical')
        # self.scroll_bar.grid(
        #     row=6, column=0
        #     )
        self.info_tree=ttk.Treeview(self.info_frame)
        self.info_tree.grid(
            row=6, column=0, columnspan=4
            )
        # self.info_tree.yview_scroll(self.scroll_bar).anchor('ns')
        self.info_tree.config(columns=('key', 'no', 'url', 'name', 'yttype','size', 'dlspeed', 'status'))
        self.info_tree.column('#0', width=0, stretch='no')
        self.info_tree.column('key', width=0, stretch='no')
        self.info_tree.column('no', width=30)
        self.info_tree.column('url', width=150)
        self.info_tree.column('name', width=100)
        self.info_tree.column('yttype', width=50)
        self.info_tree.column('size', width=60)
        self.info_tree.column('dlspeed', width=90)
        self.info_tree.column('status', width=150)
        self.info_tree.heading('#0', text='None')
        self.info_tree.heading('key', text='None')
        self.info_tree.heading('no', text='No.')
        self.info_tree.heading('url', text='Url')
        self.info_tree.heading('name', text='Name')
        self.info_tree.heading('yttype', text='Format')
        self.info_tree.heading('size', text='Size')
        self.info_tree.heading('dlspeed', text='Down Speed')
        self.info_tree.heading('status', text='Status')
        # end info box
        # load data into info box if any
        try:
            with open('dbUrls.json', 'r') as db_rurl:
                load_data=json.load(db_rurl)
            filtered_items={k:v for k,v in load_data.items() if v[-1] == 0}
            num=1
            for k,v in filtered_items.items():
                v.pop(-1)
                v.insert(0, num)
                v.insert(0, k)
                self.info_tree.insert('', index=END, iid=f'item{k}', values=tuple(v))
                num+=1
        except:
            pass
        # Action buttons
        self.framebtn=Frame(master).grid(
            row=7, column=0
            )
        self.pauseallbtn=Button(self.framebtn, text='Pause All').grid(
            row=8, column=0
            )
        self.pausebtn=Button(self.framebtn, text='Pause',
        command=self._pause).grid(
            row=8, column=1
            )
        self.removebtn=Button(self.framebtn, text='Remove',
        command=self._remove).grid(
            row=8, column=2
            )
        self.startbtn=Button(self.framebtn, text='Start',
        command=self._startBtn).grid(
            row=8, column=3
            )
        
        # treeinfo bind
        self.info_tree.bind('<<TreeviewSelect>>', self.infoTreeSelect)
        
        # dest bind
        self.dest.bind('<1>', self.fileDest)
        
        # url entry bind
        self.url_entry.bind('<1>', self.clear)
        
if __name__ == '__main__':
    root=Tk()
    start_ui = UI(root)
    root.mainloop()