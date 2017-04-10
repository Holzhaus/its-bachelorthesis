# -*- coding: utf-8 -*-
import collections
import json
import xmljson
import defusedxml.lxml
import defusedxml.ElementTree
import xjcc.plugins


class XmlJsonBasePlugin(xjcc.plugins.ConverterPlugin):
    """
    Converts XML into JSON/Python dicts/arrays and vice-versa.
    Base class.
    """
    CONVENTION = None

    @property
    def convention(self):
        return self.CONVENTION(dict_type=collections.OrderedDict)

    def xml_to_json(self, xml_data):
        data = self.convention.data(defusedxml.lxml.XML(xml_data))
        return json.dumps(data)

    def json_to_xml(self, json_data):
        data = json.loads(json_data, object_pairs_hook=collections.OrderedDict)
        tree = self.convention.etree(data)[0]
        return defusedxml.ElementTree.tostring(tree, encoding='utf-8')


class XmlJsonBadgerfishPlugin(XmlJsonBasePlugin):
    """
    Converts XML into JSON/Python dicts/arrays and vice-versa
    (Badgerfish convention)
    """
    CONVENTION = xmljson.BadgerFish


class XmlJsonGDataPlugin(XmlJsonBasePlugin):
    """
    Converts XML into JSON/Python dicts/arrays and vice-versa
    (GData convention)
    """
    CONVENTION = xmljson.GData


class XmlJsonYahooPlugin(XmlJsonBasePlugin):
    """
    Converts XML into JSON/Python dicts/arrays and vice-versa
    (Yahoo convention)
    """
    CONVENTION = xmljson.Yahoo


class XmlJsonParkerPlugin(XmlJsonBasePlugin):
    """
    Converts XML into JSON/Python dicts/arrays and vice-versa
    (Parker convention)
    """
    CONVENTION = xmljson.Parker
