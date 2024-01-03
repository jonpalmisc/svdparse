#
#  Copyright (c) 2024 Jon Palmisciano. All rights reserved.
#
#  Use of this source code is governed by the BSD 3-Clause license; a full
#  copy of the license can be found in the LICENSE.txt file.
#

from .model import Interrupt, Peripheral, Register, System

import re
from typing import Dict, Optional
from xml.etree import ElementTree


def _fix_whitespace(string: str) -> str:
    return re.sub("\\s+", " ", string)


def _parse_interrupt(node: ElementTree.Element) -> Interrupt:
    name = node.find("name").text  # pyright: ignore
    description = node.find("description").text  # pyright: ignore
    description = _fix_whitespace(description or "")
    index = int(node.find("value").text)  # pyright: ignore

    return Interrupt(name, description, index)


def _parse_register(node: ElementTree.Element) -> Register:
    name = node.find("name").text  # pyright: ignore
    description = node.find("description").text  # pyright: ignore
    description = _fix_whitespace(description or "")
    offset = int(node.find("addressOffset").text, 16)  # pyright: ignore
    size = int(node.find("size").text, 16)  # pyright: ignore

    return Register(name, description, offset, size)


def _parse_peripheral(node: ElementTree.Element) -> Peripheral:
    name = node.find("name").text  # pyright: ignore
    base_address = int(node.find("baseAddress").text, 16)  # pyright: ignore

    addr_block = node.find("addressBlock")
    size = int(addr_block.find("size").text, 16) if addr_block else 0  # pyright: ignore

    interrupts = [_parse_interrupt(i) for i in node.findall(".//interrupt")]
    registers = [_parse_register(r) for r in node.findall(".//register")]

    return Peripheral(
        name, base_address, size, interrupts, registers, node.attrib.get("derivedFrom")
    )


def _parse_system(root: ElementTree.Element) -> System:
    peripherals = [_parse_peripheral(p) for p in root.findall(".//peripheral")]

    # This is super dumb and obviously not optimized at all, but the SVD can
    # have peripherals that are "derived" from other peripherals, therefore
    # sharing some properties. Since the peripheral that another is derived
    # from does not necessarily appear before the derived peripheral itself in
    # the SVD, derived properties must be updated after initial parsing.
    inheritence_map = {}
    for p in peripherals:
        inheritence_map[p.name] = p
    for p in peripherals:
        if not p.derived_from:
            continue

        p.size = inheritence_map[p.derived_from].size
        p.registers = inheritence_map[p.derived_from].registers

    return System(peripherals)
