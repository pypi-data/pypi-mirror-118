#!/usr/bin/env python
# -*- coding: utf-8; mode: python; -*-
# Copyright © 2020-2021 Pradyumna Paranjape
#
# This file is part of pspvis.
#
# pspvis is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pspvis is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pspvis. If not, see <https://www.gnu.org/licenses/>.
#
"""
Interactive message boxes, dialog boxes, etc
"""

import threading
import tkinter as tk
from tkinter import ttk

from tkhtmlview import HTMLLabel

from . import __version__, _program

ANNOT_FILES = (('yaml files', '*.yml *.yaml'), ('toml files', '*.toml'),
               ('conf files', '*.conf *.cfg'))
SHEET_FILES = (('spreadsheet files', '*.csv *.tsv'), )


class PopUp(tk.Toplevel):
    '''
    Toplevel popup dialog with customizable contents
    '''
    def __init__(self, master, title, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)

        self.geometry('480x270')

        self.title(title)
        self.attributes('-type', 'dialog')
        # OK button
        spacer = ttk.Separator(self, orient='horizontal')
        spacer.grid(row=10, column=0, columnspan=10, sticky=tk.NS)
        ok_btn = ttk.Button(self, text='OK', command=self.destroy)
        ok_btn.grid(row=11,
                    column=4,
                    columnspan=2,
                    padx=10,
                    pady=5,
                    sticky=tk.NS)
        self.grid_rowconfigure(10, weight=1)
        self.grid_columnconfigure(4, weight=1)


class HyperMessage(PopUp):
    """
    Toplevel Widget with embeded links
    """
    def __init__(self, master, htmltext, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        label = HTMLLabel(master=self, html=htmltext)
        label.grid(sticky=tk.NSEW, column=0, columnspan=10, row=1)
        label.fit_height()


def what_s_missing(master):
    """
    Show TODOs
    """
    todo = [
        '"Resize Spot size" option',
        'Fix Freeze while loading data',
        'Progress Bar',
    ]
    messagebox = PopUp(master, 'What\'s missing...')
    for idx, missing in enumerate(todo):
        list_label = ttk.Label(messagebox, text=missing)
        list_label.grid(sticky=tk.NS, row=idx, column=0, columnspan=10)
    master.wait_window(messagebox)


def info(master):
    "Show info message"
    ext_links = {
        'source-code':
        ('gitlab', 'https://gitlab.com/pradyparanjpe/pspvis.git'),
        'readthedocs':
        ('gitlab-pages', 'https://pradyparanjpe.gitlab.io/pspvis'),
        'pip': ('Pypi', 'https://pypi.org/project/pspvis')
    }
    html_info = ['<html>', '<body>']
    html_info.append(f'<h3>{_program}</h3>')
    html_info.append(f'<b>version</b>: {__version__}<br>')
    for resource, url in ext_links.items():
        html_info.append(
            f'<b>{resource}</b>: <a href="{url[1]}">{url[0]}</a><br>')
    html_info.extend(('</body>', '</html>'))
    message = HyperMessage(master,
                           htmltext='\n'.join(html_info),
                           title=f'About {_program}')
    master.wait_window(message)


class PlotProgress(tk.Toplevel):
    """
    Indeterminate progress bar for plot progress
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.attributes('-type', 'dialog')
        self.progress = ttk.Progressbar(master=self,
                                        length=300,
                                        mode='indeterminate',
                                        orient='horizontal')
        self.ready = ttk.Label(master=self)
        self.progress.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.ready.pack(side=tk.RIGHT, fill=tk.X)

    def busy(self):
        self.ready.config(text='ready')
        self.progress.start()

    def done(self):
        self.ready.config(text='done')
        self.progress.stop()
        self.destroy()
