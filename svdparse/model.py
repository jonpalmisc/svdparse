#
#  Copyright (c) 2024 Jon Palmisciano. All rights reserved.
#
#  Use of this source code is governed by the BSD 3-Clause license; a full
#  copy of the license can be found in the LICENSE.txt file.
#

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Interrupt:
    name: str
    description: str
    index: int


@dataclass
class Register:
    name: str
    description: str
    offset: int
    size: int


@dataclass
class Peripheral:
    name: str
    base_address: int
    size: int
    interrupts: List[Interrupt]
    registers: List[Register]
    derived_from: Optional[str] = None


@dataclass
class System:
    peripherals: List[Peripheral]
