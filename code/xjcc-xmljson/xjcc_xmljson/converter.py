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
    KWARGS = {}

    @property
    def convention(self):
        return self.CONVENTION(dict_type=collections.OrderedDict)

    def xml_to_json(self, xml_data):
        data = self.convention.data(defusedxml.lxml.XML(xml_data),
                                    **self.KWARGS)
        return json.dumps(data).encode('utf-8')

    def json_to_xml(self, json_data):
        json_str = json_data.decode('utf-8')
        data = json.loads(json_str, object_pairs_hook=collections.OrderedDict)
        tree = self.convention.etree(data)[0]
        return defusedxml.ElementTree.tostring(tree, encoding='utf-8')


class XmlJsonAbderaPlugin(XmlJsonBasePlugin):
    """
    Converts XML into JSON/Python dicts/arrays and vice-versa
    (Abdera convention)
    """
    CONVENTION = xmljson.Abdera


class XmlJsonBadgerfishPlugin(XmlJsonBasePlugin):
    """
    Converts XML into JSON/Python dicts/arrays and vice-versa
    (Badgerfish convention)
    """
    CONVENTION = xmljson.BadgerFish


class XmlJsonCobraPlugin(XmlJsonBasePlugin):
    """
    Converts XML into JSON/Python dicts/arrays and vice-versa
    (Cobra convention)
    """
    CONVENTION = xmljson.Cobra


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
    KWARGS = {'preserve_root': True}
