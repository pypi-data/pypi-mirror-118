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
Menu for QMainWindow

"""

import sys
import tkinter as tk

from . import __version__, _program
from .interaction import info


class PlotMenu(tk.Menu):
    """
    Plot menu

    Args:
        parent: parent widget
        *args: all are passed to QMenuBar
        *kwargs: all are passed to QMenuBar

    Attributes:
        ui: parent
        scheme_menu: scheme menu handle to clear and refresh

    """
    def __init__(self, master: 'TkUI', *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)
        self.ui: 'TkUI' = master
        self.scheme_menu: tk.Menu
        self.add_apple_menu()
        self.add_file_menu()
        self.add_view_menu()
        self.add_theme_menu()
        self.add_help_menu()

    def add_apple_menu(self):
        """
        placeholder
        """
        if sys.platform.startswith('darwin'):
            appmenu = tk.Menu(self, name='apple')
            self.add_cascade(menu=appmenu)
            appmenu.add_command(label=f'About {_program} {__version__}',
                                command=lambda *_: info(self.ui))
            appmenu.add_separator()

    def add_file_menu(self):
        """
        File menu
        File  >> Load Sheet/Load Annotation/Redraw plot/Exit
        """
        file_menu = tk.Menu(self)
        file_menu.add_command(label='Load Spreadsheet',
                              command=self.ui.load_sheet)
        file_menu.add_command(label='Load Annotation',
                              command=self.ui.load_annot)
        file_menu.add_command(
            label='Throw data',
            command=lambda *_: self.ui.refresh_plot(inherit=False))
        file_menu.add_command(label='Exit', command=self.ui.quit)
        file_menu.entryconfigure('Load Spreadsheet', accelerator='<Ctrl+o>')
        file_menu.entryconfigure('Throw data', accelerator='<Ctrl+q>')
        file_menu.entryconfigure('Load Annotation',
                                 accelerator='<Ctrl+Shift+O>')
        self.add_cascade(label='File', menu=file_menu)

    def add_theme_menu(self):
        """
        File menu
        Themes >> Window >> [UI Themes]
        Themes >> Plot >> [mpl Themes]
        """
        theme_menu = tk.Menu(self)
        ui_menu = tk.Menu(theme_menu)
        mpl_menu = tk.Menu(theme_menu)
        for theme in self.ui.avail_themes['ui']:
            ui_menu.add_command(
                label=theme, command=lambda x=theme: self.ui.set_ui_theme(x))
        theme_menu.add_cascade(label='Window', menu=ui_menu)

        for theme in self.ui.avail_themes['mpl']:
            mpl_menu.add_command(
                label=theme, command=lambda x=theme: self.ui.set_mpl_theme(x))
        theme_menu.add_cascade(label='Plot', menu=mpl_menu)
        self.add_cascade(label='Themes', menu=theme_menu)

    def add_view_menu(self):
        view_menu = tk.Menu(self)

        dim_menu = tk.Menu(view_menu)
        dim_menu.add_command(label='2',
                             command=lambda: self.ui.refresh_plot(dim=2))
        dim_menu.add_command(label='3',
                             command=lambda: self.ui.refresh_plot(dim=3))
        view_menu.add_cascade(label='Dimensions', menu=dim_menu)

        self.scheme_menu = tk.Menu(view_menu)
        self.add_scheme_menu()
        view_menu.add_cascade(label='Scheme', menu=self.scheme_menu)

        proj_menu = tk.Menu(view_menu)
        proj_menu.add_command(label='Truncated Columns',
                              command=lambda: self.ui.plot.ui_comm.proj('raw'))
        proj_menu.add_command(
            label='Truncated Transposed Columns',
            command=lambda: self.ui.plot.ui_comm.proj('transpose'))
        proj_menu.add_command(label='PCA',
                              command=lambda: self.ui.plot.ui_comm.proj('pca'))
        proj_menu.add_command(
            label='PCA of Transpose',
            command=lambda: self.ui.plot.ui_comm.proj('transpose_pca'))
        view_menu.add_cascade(label='Projection', menu=proj_menu)
        self.add_cascade(label='View', menu=view_menu)

    def add_scheme_menu(self):
        """
        Update _scheme_menu
        """
        # create new
        for scheme in self.ui.plot.data_annot.schemes:
            self.scheme_menu.add_command(
                label=scheme,
                command=lambda x=scheme: self.ui.plot.ui_comm.apply_scheme(x))

    def update_schemes(self):
        """
        Update scheme menu cascade.
        Called after updating group schemes.
        """
        self.scheme_menu.delete(0, 'end')
        self.add_scheme_menu()

    def add_help_menu(self):
        """
        Add program help
        """
        help_menu = tk.Menu(self, name='help')
        help_menu.add_command(label=f'About {_program} {__version__}',
                              command=lambda *_: info(self.ui))
        self.add_cascade(label='Help', menu=help_menu)
