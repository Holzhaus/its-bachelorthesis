# -*- coding: utf-8 -*-
"""
A convention for marshalling XML as JSON, based on elementtree, and
written in reaction to badgerfish.
"""
from . import pesterfish
import defusedxml.ElementTree


def xml_to_json(xml_data):
    element = defusedxml.ElementTree.XML(xml_data)
    return pesterfish.to_pesterfish(element)


def json_to_xml(json_data):
    tree = pesterfish.from_pesterfish(json_data)
    return defusedxml.ElementTree.tostring(tree, encoding='utf-8')
