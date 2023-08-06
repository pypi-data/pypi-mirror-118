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
Frontend qtinter UI

"""
import sys
from pathlib import Path
from typing import Any, Callable

from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg,
                                                NavigationToolbar2QT)
from psprint import print
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import (QApplication, QErrorMessage, QFileDialog,
                               QHBoxLayout, QInputDialog, QLineEdit,
                               QMainWindow, QMessageBox, QPushButton,
                               QShortcut, QVBoxLayout, QWidget)

from .menu import PlotMenu
from .plot import PcaVis

ANNOT_FILES = '*.yml *.yaml *.toml *.conf *.cfg'
SHEET_FILES = '*.csv *.tsv'


class SearchBar(QWidget):
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
    def __init__(self, comm: Callable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.comm = comm
        self.search_field = QLineEdit(self)
        self.search_btn = QPushButton('Search', self)
        self.search_btn.clicked.connect(self.search)
        self.setLayout(QHBoxLayout(self))
        self.layout().addWidget(self.search_field)
        self.layout().addWidget(self.search_btn)

    def search(self):
        """
        Trigger communication with plot
        sends (rstripped) search-text
        - * is converted to .* for regexp
        - .* is appended to acc_str for regexp
        search text entered: ``A*BCD``
        search text sent: ``A.*BCD.*``

        """
        search_text = self.search_field.text().rstrip()
        # create re from entered text
        search_text = search_text.replace('*', '.*')
        self.search_field.setText('')
        self.comm('search', search_text)


class MPLWidget(QWidget):
    """
    Central Matplotlib widget, embeded with:
    - FigureCanvasQTAgg (matplotlib figure canvas)
    - NavigationToolbar2QT (matplotlib toolbar)

    Args:
        fig: matplotlab.Figure
        *args: all are passed to QWidget init
        *kwargs: all are passed to QWidget init

    Attributes:
        mpl_fig: matplotlib's Figure canvas
        mpl_tools: matplotlib's NavigationToolbar

    """
    def __init__(self, fig, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mpl_fig = FigureCanvasQTAgg(fig)
        self.mpl_tools = NavigationToolbar2QT(self.mpl_fig, self)
        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(self.mpl_fig)
        self.layout().addWidget(self.mpl_tools)


class QtUI(QMainWindow):
    """
    UI wrapping around matplotlib

    Args:
        *args: all are passed to QWidget init
        *kwargs: all are passed to QWidget init

    Attributes:
        central: Central Widget wrapper
        themes: discovered themes: ui, mpl
        plot: matplotlib plot
        search_bar: SearchBar
        mpl_display: MPLWidget (stretched)

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # init objects
        self.setWindowTitle('pspvis')
        self.central = QWidget(self)
        self.central.setLayout(QVBoxLayout(self.central))
        self.setCentralWidget(self.central)
        self.set_plot()
        self._collect_themes()
        self.setMenuBar(PlotMenu(self))
        self._set_shortcuts()
        self.set_ui_theme()

    def _collect_themes(self):
        """
        Collect themes from 'themes' folder and mpl's API
        """
        self.themes = {'ui': {'default': ''}, 'mpl': {'default': 'classic'}}
        for theme in (Path(__file__).parent / 'themes').glob('*.qss'):
            self.themes['ui'][theme.stem] = theme.read_text()

        for theme in self.plot.plt.style.available:
            self.themes['mpl'][theme] = theme

        for theme in (Path(__file__).parent / 'themes').glob('*.mplstyle'):
            self.themes['mpl'][theme.stem] = str(theme)

    def update_schemes(self):
        """
        Update scheme menu cascade.
        Called after updating group schemes.
        """
        menubar: PlotMenu = self.menuBar()  # type: ignore
        menubar.scheme_menu.clear()
        menubar.refresh_scheme_menu()

    def set_ui_theme(self, theme: str = 'default'):
        """
        Set theme for ui

        Args:
            theme: theme-name
        """
        self.setStyleSheet(self.themes['ui'][theme])

    def set_mpl_theme(self, theme: str = 'default'):
        """
        Set style for matplotlib.style.use

        Args:
            theme: theme-name
        """
        self.refresh_central(mpl_theme=self.themes['mpl'][theme])

    def set_plot(self, **settings: Any):
        """
        Draw plot, optionally inheriting some data

        Args:
            dim: plot dimensions
            settings: inheritance settings for PcaVisualization
            **kwargs: update settings
        """
        self.plot = PcaVis(ui=self, **settings)
        self.plot.refresh_scatter()
        self.mpl_display = MPLWidget(self.plot.fig)
        self.search_bar = SearchBar(self.plot.ui_comm)
        layout = self.central.layout()
        layout.addWidget(self.search_bar)
        layout.addWidget(self.mpl_display)
        layout.setStretch(1, 1)

    def refresh_central(self, **kwargs):
        """
        Refresh central widget
        Args:
            dim: plot dimensions
            **kwargs: passed to set_plot
        """
        settings = self.plot.extract_settings()
        settings.update(kwargs)
        self.central.layout().takeAt(0).widget().deleteLater()
        self.central.layout().takeAt(0).widget().deleteLater()
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
            query = QFileDialog.getOpenFileName(self,
                                                'Load spreadsheet',
                                                filter=SHEET_FILES)
            if not query:
                return
            filepath = Path(query[0])
        if not filepath.is_file():
            print(f"couldn't locate {filepath}")
            return

        sep = {'.tsv': '\\t', '.csv': ','}.get(filepath.suffix, '')

        self.plot.ui_comm(
            'sheet', filepath,
            QInputDialog.getText(self,
                                 'spreadsheet column separator',
                                 'separator',
                                 text=sep)[0])
        if annotation:
            for conf_file_suffix in ('.yml', '.yaml', '.toml', '.conf',
                                     '.cfg'):
                found_annot = filepath.with_suffix(conf_file_suffix)
                if found_annot.is_file():
                    reply = QMessageBox.question(
                        self, 'Found Annotation',
                        f'Load annotation {found_annot}?', QMessageBox.Yes,
                        QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        self.load_annot(found_annot, sheet=False)
                        break
        self.plot.refresh_scatter()

    def load_annot(self, filepath: Path = None, sheet: bool = True):
        """
        Select a data-csv spread sheet file to load data.
        If a sheet file with the same name-stem is found, offer to use it.

        Args:
            filepath: load from filepath (else select from Dialog)
            sheet: look if sheet file is available.

        """
        if filepath is None:
            query = QFileDialog.getOpenFileName(self,
                                                'Load Annotation',
                                                filter=ANNOT_FILES)
            if not query:
                return None
            filepath = Path(query[0])
        if not filepath.is_file():
            return None
        if sheet and self.plot._sheet['raw'].empty:
            for sheet_file_suffix in ('.csv', '.tsv'):
                found_sheet = filepath.with_suffix(sheet_file_suffix)
                if found_sheet.is_file():
                    reply = QMessageBox.question(self, 'Found spreadsheet',
                                                 f'Load data {found_sheet}?',
                                                 QMessageBox.Yes,
                                                 QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        self.load_sheet(found_sheet, annotation=False)
                        break
        self.plot.ui_comm('annotate', filepath)
        self.update_schemes()

    def _set_shortcuts(self):
        """
        Bind shortcuts
        """
        QShortcut(QKeySequence('Return'), self, self.search_bar.search)

    def throw(self, message, type):
        """
        Throw errors sent by plot as Error Message Box
        """
        QErrorMessage(self).showMessage(message, str(type))


APP = QApplication(sys.argv)
WINDOW = QtUI()
