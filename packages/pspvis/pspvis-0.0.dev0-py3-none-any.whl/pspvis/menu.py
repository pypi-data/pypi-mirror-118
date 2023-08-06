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

from pathlib import Path
from typing import Dict, Tuple

from PySide2.QtWidgets import QMenu, QMenuBar


class PlotMenu(QMenuBar):
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
    def __init__(self, parent: 'QtUI', *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.ui: 'QtUI' = parent
        self.scheme_menu: QMenu
        self.add_file_menu()
        self.add_view_menu()
        self.add_theme_menu()

    def add_file_menu(self):
        """
        File menu
        File  >> Load Sheet/Load Annotation/Redraw plot/Exit
        """
        file_menu = self.addMenu('File')
        file_menu.addAction('Load csv Spreadsheet', self.ui.load_sheet)
        file_menu.addAction('Load Annotation', self.ui.load_annot)
        file_menu.addAction('Redraw plot', self.ui.plot.refresh_scatter)
        file_menu.addAction('Exit', self.ui.close)

    def add_theme_menu(self):
        """
        File menu
        Themes >> Window >> [UI Themes]
        Themes >> Plot >> [mpl Themes]
        """
        theme_menu = self.addMenu('Themes')
        ui_menu = theme_menu.addMenu('Window')
        mpl_menu = theme_menu.addMenu('Plot')
        for theme in self.ui.themes['ui']:
            ui_menu.addAction(theme, lambda x=theme: self.ui.set_ui_theme(x))

        for theme in self.ui.themes['mpl']:
            mpl_menu.addAction(theme, lambda x=theme: self.ui.set_mpl_theme(x))

    def add_view_menu(self):
        view_menu = self.addMenu('View')

        dim_menu = view_menu.addMenu('Dimensions')
        dim_menu.addAction('2', lambda: self.ui.refresh_central(dim=2))
        dim_menu.addAction('3', lambda: self.ui.refresh_central(dim=3))

        self.scheme_menu = view_menu.addMenu('Scheme')
        self.refresh_scheme_menu()

        proj_menu = view_menu.addMenu('Projection')
        proj_menu.addAction('Truncated Columns',
                            lambda: self.ui.plot.ui_comm('proj', 'raw'))
        proj_menu.addAction('Truncated Transposed Columns',
                            lambda: self.ui.plot.ui_comm('proj', 'transpose'))
        proj_menu.addAction('PCA', lambda: self.ui.plot.ui_comm('proj', 'pca'))
        proj_menu.addAction(
            'PCA of Transpose',
            lambda: self.ui.plot.ui_comm('proj', 'transpose_pca'))

    def refresh_scheme_menu(self):
        """
        Update _scheme_menu
        """
        # create new
        for scheme in self.ui.plot.data_annot.schemes:
            self.scheme_menu.addAction(
                scheme, lambda x=scheme: self.ui.plot.ui_comm('scheme', x))
