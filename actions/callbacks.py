from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox as msgbox
import subprocess as sp
import threading as th
import os
import sys
from time import sleep
import json

class CallBacks:
    
    # button command functions
    # add url to infotree
    def _addBtn(self):
        entries={'url':(self.url_entry.get(), 'Paste Url Here', ''),
        'format':(self.formats.get(), 'Select Format', '')}
        empty=[
        k
        for k, v in entries.items()
        if v[0] == v[1] or v[0] == v[2]
        ]
        if empty:
            if len(empty) == 2:
                empty[-1]=f'and {empty[-1]}'
                msg=' '.join(empty)
            else:
                msg=' '.join(empty)
            msgbox.showwarning('Empty', f'You must fill {msg} first')
        else:
            command=['youtube-dl', f'{self.url_entry.get()}', '--get-title']
            filename='title_tmp'
            filename_err='title_tmp_err'
            self._tail(command, filename, filename_err, 'title')
    
    # start download
    def _startBtn(self):
        if self.dest.get() == 'Select Destination ....':
            if not os.path.exists(f'{self.base_dir}/ytdlfiles'):
                os.mkdir(f'{self.base_dir}/ytdlfiles')
            self.dest.state(['!readonly'])
            self.dest.delete(0, END)
            self.dest.insert(0, f'{self.base_dir}/ytdlfiles')
            self.dest.state(['readonly'])
            dest=self.dest.get()
        
        else:
            dest=self.dest.get()
        frmt=self.formats.get()
        with open(f'{self.base_dir}/dbUrls.json', 'r') as db_rurl:
            load_data=json.load(db_rurl)
        filtered_items={k:v for k,v in load_data.items() if v[-1] == 0}
        if not filtered_items:
            msgbox.showerror('No Item', 'No item to download')
        else:
            for k in filtered_items.keys():
                if f'item{k}' in self.procs:
                    filtered_items[k]=None
            for k, v in filtered_items.items():
                if v != None:
                    print('active threads:', th.active_count())
                    th.Thread(target=self._downloadUrl, args=(v[0], k, dest, frmt)).start()
                    sleep(0.4)
            
    # bind functions
    # infotree bind function
    def infoTreeSelect(self, event):
        self.item_selected=self.info_tree.selection()
        print(self.item_selected)
    
    # dest bind function
    def fileDest(self, event):
        self.dest.state(['!readonly'])
        self.dest.delete(0, END)
        loc=filedialog.askdirectory()
        self.dest.insert(0, loc)
        self.dest.state(['readonly'])
    
    # clears url entry
    def clear(self, event):
        self.url_entry.delete(0, END)
    
    def _remove(self):
        if not self.item_selected:
            msgbox.showerror('Select Item', 'No item to remove!')
        else:
            for item in self.item_selected:
                for k, v in self.status.items():
                    if k == item and (v == 'done' or v == 'paused'):
                        items=self.info_tree.get_children('')
                        item_info=[self.info_tree.set(item) for item in items if item not in self.item_selected]
                        keys=[v for item in item_info for k, v in item.items() if k == 'key']
                        get_infos=self.info_tree.set(item)
                        infos=[v for k, v in get_infos.items()]
                        infos.pop(0)
                        infos.pop(0)
                        infos.append(1)
                        self.info_tree.delete(item)
                        with open(f'{self.base_dir}/dbUrls.json', 'r') as db_rurl:
                            load_data=json.load(db_rurl)
                        load_data[str(get_infos['key'])]=infos
                        with open(f'{self.base_dir}/dbUrls.json', 'w') as db_wurl:
                            json.dump(load_data, db_wurl, indent=4)
                        num=1
                        for key in keys:
                            self.info_tree.set(f'item{key}', 'no', value=num)
                            num+=1
                
    def _pause(self):
        active_th=th.enumerate()
        keys=[i.getName() for i in active_th]
        try:
            for item in self.item_selected:
                for k, v in self.status.items():
                    if k == item and (v == 'downloading' or v == 'starting'):
                        self.killproc.append(item)
                        self.status[item]='paused'
                        print(self.status)
        except Exception as e:
            print(e)
            msgbox.showerror('Select Item', 'Select an item')
    def _pauseall(self):
        active_th=th.enumerate()
        active_th.pop(0)
        keys=[i.getName() for i in active_th]
        for k, v in self.status.items():
            if v == 'downloading' or v == 'starting':
                self.killproc.append(k)
        if keys == []:
            msgbox.showerror('No Item', 'No items to pause')