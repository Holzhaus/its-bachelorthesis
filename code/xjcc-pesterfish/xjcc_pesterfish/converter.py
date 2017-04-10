# -*- coding: utf-8 -*-
import xjcc.plugins
import defusedxml.ElementTree
from . import pesterfish


class PesterfishPlugin(xjcc.plugins.ConverterPlugin):
    """
    A convention for marshalling XML as JSON, based on elementtree, and
    written in reaction to badgerfish.
    """
    def xml_to_json(self, xml_data):
        element = defusedxml.ElementTree.XML(xml_data)
        return pesterfish.to_pesterfish(element).encode('utf-8')

    def json_to_xml(self, json_data):
        tree = pesterfish.from_pesterfish(json_data)
        return defusedxml.ElementTree.tostring(tree, encoding='utf-8')
