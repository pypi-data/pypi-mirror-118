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
Frontend ttkinter UI

"""
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk
from typing import Any, Callable

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from psprint import print
from ttkthemes import ThemedTk

from . import __version__, _program
from .interaction import PlotProgress
from .menu import PlotMenu
from .plot import PcaVis

ANNOT_FILES = (('yaml files', '*.yml *.yaml'), ('toml files', '*.toml'),
               ('conf files', '*.conf *.cfg'))
SHEET_FILES = (('spreadsheet files', '*.csv *.tsv'), )


class SearchBar(ttk.Frame):
    """
    Search Bar
    Contains:
    - a TextLine Field to insert text
    - a search button to trigger search

    Args:
        comm: communication callable, sent arguments: 'search', search_text
        *args: all are passed to QWidget init
        *kwargs: all are passed to QWidget init

    Attributes:
        comm: communication callable
        search_field: search text line
        search_btn: trigger button
    """
    def __init__(self, master, comm: Callable, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._re = tk.IntVar(value=0)
        self.comm = comm

        # objects
        self.search_field = tk.Text(self, height=1)
        re_check = ttk.Checkbutton(self, text='regexp', variable=self._re)
        search_btn = ttk.Button(self,
                                text='Search',
                                command=lambda *_: self.search())
        clear_ann = ttk.Button(self,
                               text='× Clear Annotations',
                               command=lambda *_: self.comm.clear_annot())
        spacer = ttk.Separator(master=self, orient=tk.VERTICAL)

        # Place
        self.search_field.grid(sticky=tk.EW, row=1, column=0)
        re_check.grid(sticky=tk.EW, row=1, column=1)
        search_btn.grid(sticky=tk.EW, row=1, column=2)
        spacer.grid(sticky=tk.EW, row=1, column=3)
        clear_ann.grid(sticky=tk.EW, row=1, column=4)
        self.grid_columnconfigure(0, weight=10)
        self.grid_columnconfigure(3, weight=1)

    def search(self):
        """
        Trigger communication with plot
        sends (rstripped) search-text
        - if re is checked, send raw, else:
        - * is converted to .* for regexp
        - .* is appended to acc_str for regexp
        search text entered: ``A*BCD``
        search text sent: ``A.*BCD.*``

        """
        search_text = self.search_field.get("1.0", "end-1c").rstrip()
        if search_text:
            if self._re.get() == 0:
                # create re from entered text
                special_characters = ('?', '.', '+', '(', ')', '[', ']', '{',
                                      '}', '^', '$', '\\')
                for char in special_characters:
                    search_text = search_text.replace(char, '\\' + char)
                search_text = search_text.replace('*', '.*') + '.*'
            self.comm.search_spots(search_text)
            self.search_field.delete("1.0", "end-1c")


class MPLWidget(ttk.Frame):
    """
    Central Matplotlib widget, embeded with:
    - FigureCanvasTTKAgg (matplotlib figure canvas)
    - NavigationToolbar2TTK (matplotlib toolbar)

    Args:
        fig: matplotlab.Figure
        *args: all are passed to QWidget init
        *kwargs: all are passed to QWidget init
    Attributes:
        mpl_fig: mpl figure canvas
        mpl_tools: Navigation Toolbar
    """
    def __init__(self, fig, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.mpl_fig = FigureCanvasTkAgg(fig, self)
        self.mpl_fig.draw()
        self.mpl_tools = NavigationToolbar2Tk(self.mpl_fig, self)
        self.mpl_tools.update()
        self.mpl_fig.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


class TkUI(ThemedTk):
    """
    UI wrapping around matplotlib

    Args:
        *args: all are passed to QWidget init
        *kwargs: all are passed to QWidget init

    Attributes:
        central: Central Widget wrapper
        avail_themes: discovered avail_themes: ui, mpl
        plot: matplotlib plot
        search_bar: SearchBar
        mpl_display: MPLWidget (stretched)

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # init objects
        self.style = ttk.Style(self)
        self.title(_program)
        self.scatter_mod = {}
        self.set_plot()
        self._collect_themes()
        self.option_add('*tearOff', False)
        self.menu = PlotMenu(self)
        self['menu'] = self.menu
        self._set_shortcuts()
        self.set_ui_theme()

    def _collect_themes(self):
        """
        Collect avail_themes from 'avail_themes' folder and mpl's API
        """
        self.avail_themes = {
            'ui': {
                'default': ''
            },
            'mpl': {
                'default': 'classic'
            }
        }

        for theme in self.style.theme_names():
            self.avail_themes['ui'][theme] = theme

        for theme in self.plot.plt.style.available:
            self.avail_themes['mpl'][theme] = theme

        for theme in (Path(__file__).parent /
                      'avail_themes').glob('*.mplstyle'):
            self.avail_themes['mpl'][theme.stem] = str(theme)

    def update_schemes(self):
        """
        Update scheme menu cascade.
        Called after updating group schemes.
        """
        self.menu.scheme_menu.delete(0, 'end')
        self.menu.refresh_scheme_menu()

    def set_ui_theme(self, theme: str = 'default'):
        """
        Set theme for ui

        Args:
            theme: theme-name
        """
        self.style.theme_use(theme)

    def set_mpl_theme(self, theme: str = 'default'):
        """
        Set style for matplotlib.style.use

        Args:
            theme: theme-name
        """
        self.refresh_central(mpl_theme=self.avail_themes['mpl'][theme])

    def set_plot(self, **settings: Any):
        """
        Draw plot, optionally inheriting some data

        Args:
            dim: plot dimensions
            settings: inheritance settings for PcaVisualization
            **kwargs: update settings
        """
        self.plot = PcaVis(ui=self, **settings)
        # Possibly Long calculation
        print("Threading out plot scatter")
        progress = PlotProgress(self)
        progress.busy()
        threading.Thread(target=self.plot.refresh_scatter,
                         kwargs=self.scatter_mod,
                         daemon=True).start()
        progress.done()
        progress.destroy()
        self.search_bar = SearchBar(self, self.plot.ui_comm)
        self.mpl_display = MPLWidget(self.plot.fig, self)
        self.search_bar.grid(row=1, column=0, sticky=tk.NSEW)
        self.mpl_display.grid(row=10, column=0, sticky=tk.NSEW)
        self.grid_rowconfigure(10, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def refresh_central(self, **kwargs):
        """
        Refresh central widget
        Args:
            dim: plot dimensions
            **kwargs: passed to set_plot
        """
        settings = self.plot.extract_settings()
        settings.update(kwargs)
        for frame in self.winfo_children():
            if frame is not self.menu:
                frame.destroy()
        self.set_plot(**settings)

    def load_sheet(self, filepath: Path = None, annotation: bool = True):
        """
        Select a data-csv spreadsheet file to load data.
        If an annotation file with the same name-stem is found, offer to use it

        Args:
            filepath: load from filepath (else select from Dialog)
            annotation: look if annotation file is available.

        """
        if filepath is None:
            query = filedialog.askopenfilename(title='Load spreadsheet',
                                               parent=self,
                                               filetypes=SHEET_FILES)
            if not query:
                return
            filepath = Path(query)
        if not filepath.is_file():
            print(f"couldn't locate {filepath}")
            return

        sep = {'.tsv': '\\t', '.csv': ','}.get(filepath.suffix, '')

        sep = simpledialog.askstring(parent=self,
                                     title='spreadsheet column separator',
                                     prompt='separator',
                                     initialvalue=sep)
        progress = PlotProgress(self)
        progress.busy()
        print("Threading out load sheet")

        threading.Thread(target=self.plot.ui_comm.load_sheet,
                         args=(filepath, sep),
                         daemon=True).start()
        progress.done()
        if annotation:
            for conf_file_suffix in ('.yml', '.yaml', '.toml', '.conf',
                                     '.cfg'):
                found_annot = filepath.with_suffix(conf_file_suffix)
                if found_annot.is_file():
                    reply = messagebox.askyesno(
                        parent=self,
                        title='Found Annotation',
                        message=f'Load annotation {found_annot}?')
                    if reply:
                        self.load_annot(found_annot, sheet=False)
                        break
        progress = PlotProgress(self)
        progress.busy()
        threading.Thread(target=self.plot.refresh_scatter,
                         kwargs=self.scatter_mod,
                         daemon=True).start()
        progress.done()

    def load_annot(self, filepath: Path = None, sheet: bool = True):
        """
        Select a data-csv spread sheet file to load data.
        If a sheet file with the same name-stem is found, offer to use it.

        Args:
            filepath: load from filepath (else select from Dialog)
            sheet: look if sheet file is available.

        """
        if filepath is None:
            query = filedialog.askopenfilename(parent=self,
                                               title='Load Annotation',
                                               filetypes=ANNOT_FILES)
            if not query:
                return None
            filepath = Path(query[0])
        if not filepath.is_file():
            return None
        if sheet and self.plot._sheet['raw'].empty:
            for sheet_file_suffix in ('.csv', '.tsv'):
                found_sheet = filepath.with_suffix(sheet_file_suffix)
                if found_sheet.is_file():
                    reply = messagebox.askyesno(
                        parent=self,
                        title='Found spreadsheet',
                        message=f'Load data {found_sheet}?')
                    if reply:
                        self.load_sheet(found_sheet, annotation=False)
                        break
        self.plot.ui_comm.load_annot(filepath)
        self.update_schemes()

    def _set_shortcuts(self):
        """
        Bind shortcuts
        """
        self.bind('<Return>', lambda *_: self.search_bar.search())
        self.protocol("WM_DELETE_WINDOW", self.quit)

    def throw(self, message, type):
        """
        Throw errors sent by plot as Error Message Box
        """
        messagebox.showerror(title=type, message=message, parent=self)
