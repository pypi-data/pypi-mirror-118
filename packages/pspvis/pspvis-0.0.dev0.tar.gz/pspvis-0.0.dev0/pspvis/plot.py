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
plot
"""

import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backend_bases import MouseEvent
from matplotlib.collections import PathCollection
from matplotlib.text import Annotation
from mpl_toolkits import mplot3d as plt3d
from psprint import print
from sklearn.decomposition import PCA

from .classes import DataAnnot
from .errors import MatchOverFlow, VisKeyError
from .read_config import load_configuration

BBOX = {'boxstyle': 'round', 'alpha': 0.4}
ARROWPROPS = {'arrowstyle': '->'}


def pca_transform(raw: pd.DataFrame, n_comp: int = 2) -> pd.DataFrame:
    """
    extract principal components of rawentration

    Args:
        raw: all x: comps' and y: phases
        n_comp: number of components to return

    """
    pca_worker = PCA(n_components=n_comp)
    principal_comps_n = pd.DataFrame(
        pca_worker.fit_transform(raw),
        columns=list(comp for comp in range(n_comp))).set_index(raw.index)
    assert isinstance(principal_comps_n, pd.DataFrame)
    col_names = {
        idx: f'explained variance: {val}'
        for idx, val in enumerate(pca_worker.explained_variance_ratio_)
    }
    return principal_comps_n.rename(columns=col_names)


class Annotation3D(Annotation):
    """
    Annotation for 3D axes

    Args:
        text: text to display as annotation
        xyz: annotation co-ordinates
        *args: passed to `matplotlib.text.Annotation`
        **kwargs: passed to `matplotlib.text.Annotation`
    """
    def __init__(self, text: str, xyz: Tuple[float, float, float], *args,
                 **kwargs):
        Annotation.__init__(self, text, xy=(0, 0), *args, **kwargs)

        # 3D position
        self._xyz = xyz

        # Hard-set 2D projection
        self._xy: Optional[Tuple[float, float]] = None

    @property
    def xy(self):
        if self._xy is not None:
            return self._xy
        *xy2d, _ = plt3d.proj3d.proj_transform(*self._xyz, self.axes.M)
        return xy2d

    @xy.setter
    def xy(self, val):

        # Hard-set
        self._xy = val

    @xy.deleter
    def xy(self):
        # Unset
        self._xy = None


def annotateND(ax: Union[plt.Axes, plt3d.axes3d.Axes3D], text: str,
               xyz: Tuple[float, float, float], *args, **kwargs):
    """
    Add annotation to 3D axes

    Args:
        ax: target (parent) axes
        text: Annotation text
        xyz: annotation co-ordinates
        *args: passed to `matplotlib.text.Annotation`
        **kwargs: passed to `matplotlib.text.Annotation`

    Returns:
        Annotation3D artist object
    """

    if isinstance(ax, plt3d.axes3d.Axes3D):
        a = Annotation3D(text, xyz, *args, **kwargs)
        ax.add_artist(a)
        return a
    return ax.annotate(text, xyz, *args, **kwargs)


class PcaVis(object):
    """
    PCA Visualization Container

    Attributes:
        ui: graphics UI, must define a function 'throw' to send errors
        dim: dimensions
        plt, fig: matplotlib plot, figure
        spot_annot: currently annotated spots
        highlight: spot-groups
        higilight_annot: group annotations
        group_vis_d: Currently annotated groups
        table: table in current view (raw or pca transformed)
        data_annot: annotation schemes
        scheme: currnet scheme
        mpl_theme: matplotlib style to use

    Args:
        ui: parent graphics ui
        dim: 2/3 dimensions
        settings: settings to inherit
    """
    def __init__(self, ui=None, **settings: Any) -> None:
        # Inherited attributes:
        self.spot_annot = settings.get('spot_annot', [])
        self.highlight = settings.get('highlight', [])  # combine with annot?
        self.highlight_annot = settings.get('highlight_annot', [])
        self.group_vis_d: Dict[Union[str, int],
                               Tuple[PathCollection,
                                     Union[Annotation, Annotation3D]]] = {}
        self._sheet: Dict[str, pd.DataFrame] = {
            'pca': pd.DataFrame(),
            'transpose': pd.DataFrame(),
            'transpose_pca': pd.DataFrame(),
            'raw': settings.get('raw_sheet', pd.DataFrame())
        }
        self.data_annot: DataAnnot = settings.get('data_annot', DataAnnot())
        self.scheme: str = settings.get('scheme', 'None')
        self.mpl_theme: str = settings.get('mpl_theme', 'classic')
        self.dim = settings.get('dim', 2)
        self.projection = settings.get('projection', 'raw')

        # Own attributes
        self.ui = ui
        self.plt = plt
        self.plt.style.use(self.mpl_theme)
        self.fig = self.plt.figure()
        self.sc_ax: Union[plt3d.axes3d.Axes3D,
                          plt.Axes] = self.fig.add_subplot(
                              projection='3d' if self.dim == 3 else None)

        self._resize_raw_sheet()
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)

        return

    def _remove_hl(self):
        """
        Remove any highlights
        """
        # remove previously highlighted spots
        for hl_group in self.highlight:
            hl_group.set_visible(False)
        for hl_annot in self.highlight_annot:
            hl_annot.set_visible(False)

        # reset highlights
        self.highlight = []
        self.highlight_annot = []

    def _resize_raw_sheet(self):
        """
        If raw sheet has less than n_dim columns, add sufficient zero columns
        """
        zero_cols = self.dim - self._sheet['raw'].shape[1]
        for zcol in range(zero_cols):
            self._sheet['raw'][f'zero_{zcol}'] = 0

    def extract_settings(self) -> Dict[str, Any]:
        """
        Extract settings for inheritance
        """
        settings = {}
        for attr in ('dim', 'data_annot', 'scheme', 'mpl_theme', 'projection'):
            settings[attr] = getattr(self, attr, None)
            settings['raw_sheet'] = self._sheet['raw']
        return settings

    def load_sheet(self, filename: Optional[Path], sep: str = None):
        """
        Load spread sheet
        Args:
            filename: load data co-ordinates from this file
            sep: spread sheet columns-separator

        """
        if filename is None:
            return
        sep = sep or ','
        sep = {'tab': '\t', '\\t': '\t'}.get(sep.lower(), sep)
        sheet = pd.read_csv(Path(filename), sep=sep, index_col=0)
        assert isinstance(sheet, pd.DataFrame)
        self._sheet['raw'] = sheet
        # flush pca transformed data
        self._sheet['pca'] = pd.DataFrame()
        self._sheet['transpose'] = pd.DataFrame()
        self._sheet['pca_transpose'] = pd.DataFrame()
        self._resize_raw_sheet()
        self.data_annot.rows += list(self._sheet['raw'].index)
        self.data_annot.cols += list(self._sheet['raw'].columns)

    def load_annot(self, filename: Optional[Path] = None):
        """
        Load annotation confituration

        Args:
            filename: Load annotations from this file
        """
        if filename is None:
            return
        self.data_annot.update(load_configuration(Path(filename)))
        # self.data_annot.filter(self._sheet['raw'])

    def transform(self):
        """
        extract principal components of columns

        """
        if self.projection == 'pca':
            self._sheet[self.projection] = pca_transform(
                self._sheet['raw'], self.dim)
            return

        if self.projection == 'transpose':
            self._sheet[self.projection] = self._sheet['raw'].transpose()
        elif self.projection == 'transpose_pca':
            self._sheet[self.projection] = pca_transform(
                self._sheet['raw'].transpose(), self.dim)
        self.scheme = 'None'

    def proj(self, projection: str = 'raw'):
        """
        Switch plot between truncated columns and PCA projection

        Args:
            pca: ?project PCA?
        """
        if projection == self.projection:
            return
        self.projection = projection
        self.refresh_scatter()

    def apply_scheme(self, scheme: str):
        """
        Apply grouping scheme
        Args:
            scheme: scheme
        """
        print(f'Updated scheme: {scheme}', mark=2)
        self.scheme = scheme
        self.refresh_scatter()

    def ui_comm(self, context: str = 'search', *args, **kwargs):
        """
        Communication pipe to UI

        Args:
            context: context conveyed from UI to determine target function
            *args: all are passed on to context function
            *kwargs: all are passed on to context function

        """
        if not args:
            return
        {
            'sheet': self.load_sheet,
            'annotate': self.load_annot,
            'scheme': self.apply_scheme,
            'search': self.search_spots,
            'proj': self.proj,
        }[context](*args, **kwargs)

    def refresh_scatter(self):
        """
        Update scatter
        """
        if 0 in self._sheet['raw'].shape:
            print('Spreadsheet is empty', mark=5)
            return

        if self.projection != 'raw' and self._sheet[self.projection].empty:
            # lazy
            self.transform()

        table = self._sheet[self.projection]

        # erase scatter
        self.sc_ax.clear()
        self.group_vis_d = {}

        grp_count = 0
        scheme = self.data_annot.schemes[self.scheme]
        for idx, group in scheme.items():
            grp_in_tbl = list(filter(lambda x: x in table.index, group))
            if not grp_in_tbl:
                continue
            group_spots = table.loc[grp_in_tbl].iloc[:, :self.dim]
            xy = zip(*group_spots.iloc[:, :self.dim].values)
            data_sc: PathCollection = self.sc_ax.scatter(
                *xy,
                c=[self.plt.cm.hsv(grp_count / len(scheme))],
                # s=1,
                alpha=0.5)
            group_annot = annotateND(self.sc_ax,
                                     idx,
                                     xy,
                                     xytext=(20, 20),
                                     textcoords='offset points',
                                     bbox=BBOX,
                                     arrowprops=ARROWPROPS)
            group_annot.set_visible(False)
            self.group_vis_d[idx] = (data_sc, group_annot)
            grp_count += 1
        self.sc_ax.set_xlabel(f'{table.columns[0]}')
        self.sc_ax.set_ylabel(f'{table.columns[1]}')
        self.sc_ax.grid(linestyle=':')
        if isinstance(self.sc_ax, plt3d.axes3d.Axes3D):
            self.sc_ax.set_zlabel(f'{table.columns[2]}')
        else:
            self.sc_ax.set_aspect('equal')
        self.fig.canvas.draw_idle()

    def on_click(self, event: MouseEvent):
        """
        Trigger update_annotate for each group under the click event
        * bind to button-press-event on figure.canvas

        Args:
            event: mouse event

        """
        if event.inaxes == self.sc_ax:

            self._remove_hl()

            show_event = False
            for idx, group_sc in self.group_vis_d.items():
                vis = group_sc[1].get_visible()
                cont, ind = group_sc[0].contains(event)
                if cont:
                    show_event = True
                    self.update_annot(ind, idx)
                    group_sc[1].set_visible(True)
                else:
                    if vis:
                        group_sc[1].set_visible(False)
            if show_event:
                for hl_group in self.highlight:
                    hl_group.set_visible(True)
                for hl_annot in self.highlight_annot:
                    hl_annot.set_visible(True)
            self.fig.canvas.draw_idle()
        return

    def update_annot(self, ind, idx: Union[str, int]) -> None:
        """
        Interactive annotation update

        - Click on a spot:
          - marks the spot's name
          - highlights group of the spot
          - marks centroid of the group

        - Click on empty space:
          - clears annotation marks

        Args:
           ind: itemlist returned by collections.PathCollection.contains(event)
           idx: group-index in current-scheme

        """
        table = self._sheet[self.projection]
        sc, annot = self.group_vis_d[idx]
        group = self.data_annot.schemes[self.scheme][idx]
        hl = table.loc[group]
        annot.xy = sc.get_offsets()[ind['ind'][0]]
        text = '\n'.join([str(group[n]) for n in ind['ind']])
        cg = table.loc[group].mean(axis=0)[:self.dim].values
        xy = zip(*hl.iloc[:, :self.dim].values)
        self.highlight.append(self.sc_ax.scatter(*xy, c='#7f7f7fff'))
        annot.set_text(text)
        annot.set_ha('center')
        if self.scheme != 'None':
            cg_handle = self.sc_ax.scatter(*cg, s=5)
            cg_annot = annotateND(self.sc_ax,
                                  f'Centroid of\n{idx}',
                                  cg,
                                  xytext=(-40, -40),
                                  textcoords='offset points',
                                  bbox=BBOX,
                                  arrowprops=ARROWPROPS)
            self.highlight.append(cg_handle)
            self.highlight_annot.append(cg_annot)
        return

    def search_spots(self, acc_str: str = ''):
        """
        Search and highlight spots with accession

        Args:
            acc_str: regular expression text (case ignored)

        """
        # remove all spot annotations
        for ann in self.spot_annot:
            ann.set_visible(False)

        if not acc_str:
            return

        self.spot_annot = []

        table = self._sheet[self.projection]

        acc_pat = re.compile(f'^{acc_str}.*', flags=re.IGNORECASE)
        acc_found = False
        matches: int = 0
        match_names_d = {}
        for idx, pos in table.iterrows():
            if len(match_names_d) > 50:
                # overflow
                if self.ui is not None:
                    self.ui.throw('Too many matching data accessions',
                                  type=MatchOverFlow)
                else:
                    print('Too many matching data accessions', mark='err')
                break
            accession = acc_pat.match(str(idx))
            if accession:
                match_names_d[idx] = pos
                matches += 1
        if matches:
            acc_found = True
            for idx, pos in match_names_d.items():
                self.spot_annot.append(self.group_vis_d[idx][1])
            for annot in self.spot_annot:
                annot.set_visible(True)

        if not acc_found:
            if self.ui is not None:
                self.ui.throw('Not Found', type=VisKeyError)
            else:
                print('Not Found', mark='err')

        self.fig.canvas.draw_idle()
        return
