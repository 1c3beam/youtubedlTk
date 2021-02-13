from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import subprocess as sp
import threading as th
import os
import sys
from pathlib import Path
from time import sleep
import json
from actions.actions import Actions
from actions.callbacks import CallBacks

class UI(Actions, CallBacks):

    def __init__(self, master):
        self.status=[]
        self.killproc=[]
        self.procs=[]
        self.base_dir=Path(Path.home(), 'youtubedl0')
        if not os.path.exists(self.base_dir):
            os.mkdir(self.base_dir)
        # Frame for Url
        self.url_frame=ttk.Frame(master)
        self.url_frame.pack(side='top', fill='both', padx=5, pady=5)
        self.url_entry=ttk.Entry(self.url_frame, width=60)
        self.url_entry.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self.url_entry.insert(0, 'Paste Url Here')
        
        # Destination
        self.dest=ttk.Combobox(self.url_frame,
        text='')
        self.dest.grid(row=1, column=0, padx=5, pady=5)
        self.dest.insert(0, 'Select Destination ....')
        self.dest.state(['readonly'])
        
        # Select a format
        self.formats=ttk.Combobox(self.url_frame, values=(
            'mp4', 'mp3'))
        self.formats.grid(row=1, column=1, pady=5)
        self.formats.insert(0, 'Select Format')
        self.formats.state(['readonly'])
        
        # Adds Url
        self.addbtn=ttk.Button(self.url_frame,
        text='Add', command=self._addBtn)
        self.addbtn.grid(row=1, column=2, pady=5)
        
        # Info Box
        self.info_frame=ttk.Frame(master)
        self.info_frame.pack(side='top', fill='both', padx=5, pady=5)
        self.info_tree=ttk.Treeview(self.info_frame)
        self.info_tree.grid(row=0, column=0)
        self.info_tree.config(columns=('key', 'no', 'url', 'name', 'yttype','size', 'dlspeed', 'status'))
        self.info_tree.column('#0', width=0, stretch='no')
        self.info_tree.column('key', width=0, stretch='no')
        self.info_tree.column('no', width=30)
        self.info_tree.column('url', width=150)
        self.info_tree.column('name', width=100)
        self.info_tree.column('yttype', width=60)
        self.info_tree.column('size', width=70)
        self.info_tree.column('dlspeed', width=90)
        self.info_tree.column('status', width=100)
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
        
        # scrollbar for info tree
        self.scroll_bar=ttk.Scrollbar(self.info_frame, orient='vertical', command=self.info_tree.yview)
        self.scroll_bar.grid(row=0, column=1, sticky='ns')
        self.info_tree.config(yscrollcommand=self.scroll_bar.set)
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
        self.framebtn=ttk.Frame(master)
        self.framebtn.pack(side='top', fill='both', padx=5, pady=5)
        
        self.pauseallbtn=ttk.Button(self.framebtn, text='Pause All', command=self._pauseall)
        self.pauseallbtn.pack(side='left', padx=5, pady=5)
        
        self.pausebtn=ttk.Button(self.framebtn, text='Pause', command=self._pause)
        self.pausebtn.pack(side='left', padx=5, pady=5)
        
        self.removebtn=ttk.Button(self.framebtn, text='Remove', command=self._remove)
        self.removebtn.pack(side='left', padx=5, pady=5)
        
        self.startbtn=ttk.Button(self.framebtn, text='Start', command=self._startBtn)
        self.startbtn.pack(side='left', padx=5, pady=5)
        
        # treeinfo bind
        self.info_tree.bind('<<TreeviewSelect>>', self.infoTreeSelect)
        
        # dest bind
        self.dest.bind('<1>', self.fileDest)
        
        # url entry bind
        self.url_entry.bind('<1>', self.clear)