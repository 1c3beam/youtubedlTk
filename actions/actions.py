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


class Actions:
    
    # this function is used for downloading and getting title
    # this code is for tailing a tmpfile to update a certain
    # part of the gui
    def _tail(self, command, filename, filename_err, state=None, d=None, key=None):
        if state == 'download':
            os.chdir(d)
        if not os.path.exists(f'{self.base_dir}/.tmp'):
            os.mkdir(f'{self.base_dir}/.tmp')
        tmpfile=f'{self.base_dir}/.tmp/{filename}'
        tmperrfile=f'{self.base_dir}/.tmp/{filename_err}'
        infos=[]
        with open(tmpfile, 'wb') as twFile,\
        open(tmpfile, 'rb') as trFile,\
        open(tmperrfile, 'wb') as twerrFile,\
        open(tmperrfile, 'rb') as trerrFile:
            proc=sp.Popen(command, stdout=twFile, stderr=twerrFile)
            while proc.poll() is None:
                twFile.flush()
                twerrFile.flush()
                line=trFile.readline().decode()
                line_err=trerrFile.readline().decode()
                words=line.split()
                words_err=line_err.split()
                if state == 'title':
                    self._modifyTitle(words, words_err)
                else:
                    self._modifyDl(words, words_err, key)
                sleep(0.09)
        with open(tmpfile, 'rb') as trFile,\
        open(tmperrfile, 'rb') as trerrFile:
            line=trFile.readlines()
            line_err=trerrFile.readlines()
            try:
                words=line[-1].decode().split()
            except:
                words=None
            try:
                words_err=line_err[-1].decode.split()
            except:
                words_err=None
            if state == 'title':
                self._modifyTitle(words, words_err)
            else:
                self._modifyDl(words, words_err, key)
    
    # helper function for _getTitle
    def _modifyTitle(self, words, words_err):
        if words_err == None:
            # this code here is for _getTitle's exiting while loop
            pass
        else:
            if words_err == []:
                pass
            
            else:
                if len(words_err) < 21:
                    ytUrls={}
                    frmt=self.formats.get()
                    # checks dbUrls json
                    path=f'{self.base_dir}/dbUrls.json'
                    if not os.path.exists(path):
                        with open(f'{self.base_dir}/dbUrls.json', 'w') as db_wurl:
                            json.dump(ytUrls, db_wurl, indent=4)
                        with open(f'{self.base_dir}/dbUrls.json') as db_rurl:
                            data=json.load(db_rurl)
                    # if dbUrls have been initiated
                    else:
                        with open(f'{self.base_dir}/dbUrls.json', 'r') as db_rurl:
                            data=json.load(db_rurl)
                    # end checking
                    num=[k for k, v in data.items() if v[-1] == 0]
                    key=str(len(data))
                    data[key]=[
                        self.url_entry.get(),
                        '--',
                        f'{frmt}',
                        '--',
                        '--',
                        'idle ...',
                        0
                        ]
                    with open(f'{self.base_dir}/dbUrls.json', 'w') as db_wurl:
                        json.dump(data, db_wurl, indent=4)
                    with open(f'{self.base_dir}/dbUrls.json', 'r') as db_rurl:
                        load_data=json.load(db_rurl)
                    infos=[v for v in load_data[key] if load_data[key][-1] == 0]
                    infos.pop(-1)
                    infos.insert(0, len(num)+1)
                    infos.insert(0, key)
                    self.info_tree.insert('', index=END, iid=f'item{key}', values=tuple(infos))
        # if words_err == None:
        #     pass
        # else:
        #     if words_err == []:
        #         pass
            
        #     else:
        #         try:
        #             if words_err[-22] == 'ERROR:':
        #                 print('title: Encountered an Error')
        #         except:
        #             pass # text 'WARNING:' are ignored
    
    # helper function for _dl 
    def _modifyDl(self, words, words_err, key):
        if words == None:
            pass
        else:
            if words == []:
                pass
            # this code will check every output in tmpfile and
            # parse specific word to display to the user
            if len(words) < 7:
                pass
            else:
                infos=[]
                with open(f'{self.base_dir}/dbUrls.json', 'r') as db_rurl:
                    cdata=json.load(db_rurl)
                for i in cdata[str(key)]:
                    infos.append(i)
                if words[-7] == '100.0%':
                    words[-7]='Done'
                self.info_tree.set(f'item{str(key)}', 'size', value=words[-5])
                self.info_tree.set(f'item{str(key)}', 'dlspeed', value=words[-3])
                self.info_tree.set(f'item{str(key)}', 'ststus', value=words[-7])
        
        if words_err == None:
            pass
        # this code is for error checking
        else:
            if words_err == []:
                pass
            
            else:
                try:
                    if words_err[-22] == 'ERROR:':
                        self.info_tree.set(f'item{str(key)}', 'status', value='Failed!')
                        print('download: An error occured')
                except:
                    pass

    # helper function for startBtn
    def _downloadUrl(self, u, k, d, f):
        filename=f'tmpdl{k}'
        filename_err=f'tmperror{k}'
        if f == 'mp4':
            cmd_dl=['youtube-dl', f'{u}']
            th.Thread(target=self._tail, args=(cmd_dl, filename, filename_err, 'download', d, k), name=f'item{k}').start()
            # print('threads running:', th.)
        else:
            cmd_dl=['youtube-dl', '-x', f'{u}', '--audio-format' ,'mp3']
            th.Thread(target=self._tail, args=(cmd_dl, filename, filename_err, 'download', d, k), name=f'item{k}').start()
