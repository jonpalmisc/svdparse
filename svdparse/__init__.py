#
#  Copyright (c) 2024 Jon Palmisciano. All rights reserved.
#
#  Use of this source code is governed by the BSD 3-Clause license; a full
#  copy of the license can be found in the LICENSE.txt file.
#

from . import model, parse


def parse_file(path: str) -> model.System:
    from xml.etree import ElementTree

    return parse._parse_system(ElementTree.parse(path))
