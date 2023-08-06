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
Shared data types
"""

from dataclasses import dataclass
from typing import Any, ItemsView, Union


@dataclass
class PlotUserVars():
    spot_size: int = 50
    hold_annot: bool = False
    mpl_theme: str = 'classic'

    def update(self, template: Union['PlotUserVars', dict] = None):
        if template is None:
            return
        for attr, val in template.items():
            setattr(self, attr, val)

    def items(self) -> ItemsView[str, Any]:
        return self.__dict__.items()
