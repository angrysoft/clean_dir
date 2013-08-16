#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       clean_dir.py
#
#       Copyright 2010 - 2012 Sebastian Zwierzchowski <sebastian.zwierzchowski@gmail.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import os
import sys
from shutil import move

class CleanDir:
    """ Class doc """

    def __init__ (self,dir_path):
        """ Class initialiser """
        self.files = {
        'movie'    : [],
        'archive'  : [],
        'iso'      : [],
        'win'      : [],
        'mac'      : [],
        'torrent'  : [],
        'photo'    : [],
        'doc'      : [],
        'music'    : [],
        'html'     : [],
        'flash'    : [],
        'sources'  : [],
        'playlist' : [],
        'text'     : [],
        'cad'      : [],
        'blender'  : [],
        'wysiwyg'  : []
        }

        self.file_list = []
        self.dir_path = dir_path.rstrip('/')
        for f in os.listdir(self.dir_path):
            if f[0] =='.': continue
            if os.path.isdir("{0}/{1}".format(self.dir_path,f)): continue
            self.file_list.append("{0}/{1}".format(self.dir_path,f))


    def file_type (self,file_path):
        """ Function doc """
        filetypes = {
        'movie'    : ['asf', 'avi', 'flv', 'mkv' , 'mov', 'mp4', 'mpe', 'mpg', 'mpeg','rmvb', 'wmv', '3pg', '3gp'],
        'archive'  : ['tar', 'tgz', 'gz', 'bz2', 'tbz2', 'zip', '7zip', '7z', 'rar'],
        'pdf'      : ['pdf'],
        'iso'      : ['iso', 'cue', 'bin', 'img'],
        'win'      : ['exe', 'msi'],
        'mac'      : ['dmg', 'app', 'pkg'],
        'torrent'  : ['torrent'],
        'photo'    : ['bmp', 'gif', 'jpg', 'jpeg', 'png', 'tiff', 'xcf'],
        'doc'      : ['doc', 'ods', 'odt', 'pp', 'pps','sxw', 'xls', 'pdf', 'rtf', 'epub', 'mobi'],
        'music'    : ['flac', 'mp2', 'mp3', 'mid', 'mpc','ogg', 'wav', 'wma', ],
        'html'     : ['htm', 'html'],
        'flash'    : ['swf'],
        'sources'  : ['c', 'cc', 'cpp', 'h', 'pl', 'py', 'ru', 'sh' ],
        'playlist' : ['asx', 'm3u', 'pls', 'ram'],
        'text'     : ['txt', 'sub', 'srt', 'rtxt'],
        'cad'      : ['dwg'],
        'blender'  : ['blend'],
        'wysiwyg'  : ['wyg']
        }
        
        suffix = ''
        if file_path.find('.') > 0:
            suffix = file_path.rsplit('.',1)[1].lower()

        for ft in filetypes:
            if (suffix in filetypes[ft]): return ft

        return None


    def __move_subtitles(self):
        """ Function doc """
        movie = []
        for m in self.files['movie']:
            movie.append(m.rsplit('.',1)[0].lower())
        
        txt = self.files['text'][:]
        for t in self.files['text']:
            if t.rsplit('.',1)[0].lower() in movie:
                self.files['movie'].append(t)
                txt.remove(t)
        self.files['text'] = txt

        
    def order_files (self):
        """ Function doc """

        for f in self.file_list:
            ft = self.file_type(f)
            if not ft: continue
            self.files[ft].append(f)
        
        self.__move_subtitles()


    def move_files (self):
        """ Function doc """
        for f in self.files:
            if self.files[f] == []: continue
            d = "{0}/{1}".format(self.dir_path,f)

            if not os.path.exists(d): os.mkdir(d)

            for s in self.files[f]:
                if os.path.exists("{0}/{1}".format(d,os.path.basename(s))):
                    print(("File {0} allready exists".format("{0}/{1}".format(d,os.path.basename(s)))))
                    continue
                move(s,d)


    def print_files (self):
        """ Function doc """
        for f in self.files:
            print(('{0} : {1}'.format(f,self.files[f])))
            
            
### Class CleanDir ###



if __name__ == '__main__':
    if(len(sys.argv)==1) or not os.path.isdir(sys.argv[1]):
        sys.exit(1)
    d = CleanDir(sys.argv[1])
    d.order_files()
    d.move_files()
    #d.print_files()

