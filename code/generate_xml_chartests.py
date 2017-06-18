#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import lxml.etree

CHAR_RANGES = [
    [    0x20,     0x7E, 'ASCII printable'],
    [    0x7F,     0x84, 'Discouraged'],
    [    0x85,     0x85, 'NEL Control Char'],
    [    0x86,     0x9F, 'Discouraged'],
    [    0xA0,    0xFFF, 'BMP plane I'],
    [  0x1000,   0x1FFF, 'BMP plane II'],
    [  0x2000,   0x2FFF, 'BMP plane III'],
    [  0x3000,   0x3FFF, 'BMP plane IV'],
    [  0x4000,   0x4FFF, 'BMP plane V'],
    [  0x5000,   0x5FFF, 'BMP plane VI'],
    [  0x6000,   0x6FFF, 'BMP plane VII'],
    [  0x7000,   0x7FFF, 'BMP plane VIII'],
    [  0x8000,   0x8FFF, 'BMP plane IX'],
    [  0x9000,   0x9FFF, 'BMP plane X'],
    [  0xA000,   0xAFFF, 'BMP plane XI'],
    [  0xB000,   0xBFFF, 'BMP plane XII'],
    [  0xC000,   0xCFFF, 'BMP plane XIII'],
    [  0xD000,   0xD7FF, 'BMP plane XIV'],
    [  0xE000,   0xEFFF, 'BMP plane XV'],
    [  0xF000,   0xFDCF, 'BMP plane XVI'],
    [  0xFDD0,   0xFDEF, 'BMP plane Discouraged'],
    [  0xFDF0,   0xFFFD, 'BMP plane XVII'],
    [ 0x10000,  0x1FFFD, 'SMP plane'],
    [ 0x1FFFE,  0x1FFFF, 'SMP plane Discouraged'],
    [ 0x20000,  0x2FFFD, 'SIP plane'],
    [ 0x2FFFE,  0x2FFFF, 'SIP plane Discouraged'],
    [ 0x30000,  0x3FFFD, 'Unassigned plane 3'],
    [ 0x3FFFE,  0x3FFFF, 'Plane 3 Discouraged'],
    [ 0x40000,  0x4FFFD, 'Unassigned plane 4'],
    [ 0x4FFFE,  0x4FFFF, 'Plane 4 Discouraged'],
    [ 0x50000,  0x5FFFD, 'Unassigned plane 5'],
    [ 0x5FFFE,  0x5FFFF, 'Plane 5 Discouraged'],
    [ 0x60000,  0x6FFFD, 'Unassigned plane 6'],
    [ 0x6FFFE,  0x6FFFF, 'Plane 6 Discouraged'],
    [ 0x70000,  0x7FFFD, 'Unassigned plane 7'],
    [ 0x7FFFE,  0x7FFFF, 'Plane 7 Discouraged'],
    [ 0x80000,  0x8FFFD, 'Unassigned plane 8'],
    [ 0x8FFFE,  0x8FFFF, 'Plane 8 Discouraged'],
    [ 0x90000,  0x9FFFD, 'Unassigned plane 9'],
    [ 0x9FFFE,  0x9FFFF, 'Plane 9 Discouraged'],
    [ 0xA0000,  0xAFFFD, 'Unassigned plane 10'],
    [ 0xAFFFE,  0xAFFFF, 'Plane 10 Discouraged'],
    [ 0xB0000,  0xBFFFD, 'Unassigned plane 11'],
    [ 0xBFFFE,  0xBFFFF, 'Plane 11 Discouraged'],
    [ 0xC0000,  0xCFFFD, 'Unassigned plane 12'],
    [ 0xCFFFE,  0xCFFFF, 'Plane 12 Discouraged'],
    [ 0xD0000,  0xDFFFD, 'Unassigned plane 13'],
    [ 0xDFFFE,  0xDFFFF, 'Plane 13 Discouraged'],
    [ 0xE0000,  0xEFFFD, 'SSP plane'],
    [ 0xEFFFE,  0xEFFFF, 'SSP plane Discouraged'],
    [ 0xF0000,  0xFFFFD, 'SPUA-A plane'],
    [ 0xFFFFE,  0xFFFFF, 'SPUA-A plane Discouraged'],
    [0x100000, 0x10FFFD, 'SPUA-B plane'],
    [0x10FFFE, 0x10FFFF, 'SPUA-B plane Discouraged'],
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
    decimal_width = math.floor(math.log(max([start, end]), 10)) + 1
    if (end - start) > 0x1000:
        # Only use single element for huge char ranges
        el_chars = lxml.etree.SubElement(el_root, 'chars')
        el_chars.text = ''.join(chr(char) for char in range(start, end))
    else:
        for char in range(start, end):
            el_char = lxml.etree.SubElement(el_root, 'ud{char:0{w}d}'.format(
                w=decimal_width,
                char=char,
            ))
            el_char.text = chr(char)

    comment_text = COMMENT_TEMPLATE.format(start=start, end=end, w=width,
                                           desc=desc)
    el_root.addprevious(lxml.etree.Comment(comment_text))
    tree = lxml.etree.ElementTree(el_root)
    with open(filename, mode='wb') as f:
        tree.write(f, pretty_print=False, xml_declaration=True,
                   encoding='UTF-8')
