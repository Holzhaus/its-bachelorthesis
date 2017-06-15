#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import lxml.etree

CHAR_RANGES = [
    [0x20, 0x7E, 'Basic latin printable'],
    [0x80, 0x9F, 'C1 set'],
    [0xA0, 0xFFF, 'Various printable'],
    [0x1000, 0x1FFF, 'Various printable'],
    [0x2000, 0x2FFF, 'Various printable'],
    [0x3000, 0x3FFF, 'Various printable'],
    [0x4000, 0x4FFF, 'Various printable'],
    [0x5000, 0x5FFF, 'Various printable'],
    [0x6000, 0x6FFF, 'Various printable'],
    [0x7000, 0x7FFF, 'Various printable'],
    [0x8000, 0x8FFF, 'Various printable'],
    [0x9000, 0x9FFF, 'Various printable'],
    [0xA000, 0xAFFF, 'Various printable'],
    [0xB000, 0xBFFF, 'Various printable'],
    [0xC000, 0xCFFF, 'Various printable'],
    [0xD000, 0xD7FF, 'Various printable'],
    [0x7F, 0x84, 'Discouraged by XML spec'],
    [0x86, 0x9F, 'Discouraged by XML spec'],
    [0xFDD0, 0xFDEF, 'Discouraged by XML spec'],
    [0x1FFFE, 0x1FFFF, 'Discouraged by XML spec'],
    [0x2FFFE, 0x2FFFF, 'Discouraged by XML spec'],
    [0x3FFFE, 0x3FFFF, 'Discouraged by XML spec'],
    [0x4FFFE, 0x4FFFF, 'Discouraged by XML spec'],
    [0x5FFFE, 0x5FFFF, 'Discouraged by XML spec'],
    [0x6FFFE, 0x6FFFF, 'Discouraged by XML spec'],
    [0x7FFFE, 0x7FFFF, 'Discouraged by XML spec'],
    [0x8FFFE, 0x8FFFF, 'Discouraged by XML spec'],
    [0x9FFFE, 0x9FFFF, 'Discouraged by XML spec'],
    [0xAFFFE, 0xAFFFF, 'Discouraged by XML spec'],
    [0xBFFFE, 0xBFFFF, 'Discouraged by XML spec'],
    [0xCFFFE, 0xCFFFF, 'Discouraged by XML spec'],
    [0xDFFFE, 0xDFFFF, 'Discouraged by XML spec'],
    [0xEFFFE, 0xEFFFF, 'Discouraged by XML spec'],
    [0xFFFFE, 0xFFFFF, 'Discouraged by XML spec'],
    [0x10FFFE, 0x10FFFF, 'Discouraged by XML spec'],
]

COMMENT_TEMPLATE = """;testcase
[General]
name: Chars u{start:0{w}X}-{end:0{w}X} ({desc})
description: Checks if characters in the range U+{start:X} to U+{end:X} ({desc}) are handled correctly
"""

FILENAME_TEMPLATE = 'chars-u{start:0{w}X}-u{end:0{w}X}.xml.testcase'

maxnum = max(max(sublist[0:2]) for sublist in CHAR_RANGES)
width = math.floor(math.log(maxnum, 16)) + 1

for start, end, desc in CHAR_RANGES:
    filename = FILENAME_TEMPLATE.format(start=start, end=end, w=width)
    el_root = lxml.etree.Element('root')
    for char in range(start, end):
        el_char = lxml.etree.SubElement(el_root, 'ud%d' % char)
        el_char.text = chr(char)

    comment_text = COMMENT_TEMPLATE.format(start=start, end=end, w=width,
                                           desc=desc)
    el_root.addprevious(lxml.etree.Comment(comment_text))
    tree = lxml.etree.ElementTree(el_root)
    with open(filename, mode='wb') as f:
        tree.write(f, pretty_print=False, xml_declaration=True,
                   encoding='UTF-8')
