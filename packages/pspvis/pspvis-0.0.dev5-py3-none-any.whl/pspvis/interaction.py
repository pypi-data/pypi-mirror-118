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

import tkinter as tk
import webbrowser
from tkinter import ttk

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


def info(master):
    "Show info message"
    ext_links = {
        'source-code': 'https://gitlab.com/pradyparanjpe/pspvis.git',
        'readthedocs': 'https://pradyparanjpe.gitlab.io/pspvis',
        'pip': 'https://pypi.org/project/pspvis',
        'license': 'https://www.gnu.org/licenses/lgpl-3.0.html'
    }
    message = PopUp(master, title=f'About {_program} {__version__}')
    l_index = 0
    link_f = ttk.Frame(message)
    link_f.grid(row=1, column=0, columnspan=10, sticky=tk.NS, padx=10, pady=10)
    for text, url in ext_links.items():
        l_index += 1
        link_label = ttk.Label(link_f,
                               text=f'{l_index}. {text}',
                               foreground='#33f',
                               cursor='hand2')
        link_label.bind('<Button-1>',
                        lambda *_, url=url: webbrowser.open_new_tab(url))
        link_label.grid(row=l_index, sticky=tk.NSEW)
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

        self.progress.grid(row=1, column=0, columnspan=10, sticky=tk.NSEW)
        self.ready.grid(row=10, column=4, columnspan=2, sticky=tk.NSEW)

        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def busy(self):
        self.ready.config(text='ready')
        self.progress.start()

    def done(self):
        self.ready.config(text='done')
        self.progress.stop()
        self.destroy()
