# -*- coding: utf-8 -*-
import xjcc.plugins
import xml.etree
import defusedxml.ElementTree
from . import pesterfish


class PesterfishPlugin(xjcc.plugins.ConverterPlugin):
    """
    A convention for marshalling XML as JSON, based on elementtree, and
    written in reaction to badgerfish.
    """
    def xml_to_json(self, xml_data):
        element = xml.etree.ElementTree.XML(xml_data)
        return pesterfish.to_pesterfish(element).encode('utf-8')

    def json_to_xml(self, json_data):
        tree = pesterfish.from_pesterfish(json_data)
        return xml.etree.ElementTree.tostring(tree, encoding='utf-8')


class PesterfishDefusedPlugin(xjcc.plugins.ConverterPlugin):
    """
    A convention for marshalling XML as JSON, based on elementtree, and
    written in reaction to badgerfish (using defusedxml parser).
    """
    def xml_to_json(self, xml_data):
        element = defusedxml.ElementTree.XML(xml_data)
        return pesterfish.to_pesterfish(element).encode('utf-8')

    def json_to_xml(self, json_data):
        tree = pesterfish.from_pesterfish(json_data)
        return defusedxml.ElementTree.tostring(tree, encoding='utf-8')
