# -*- coding: utf-8 -*-
import collections
import io
import os
import defusedxml.lxml
import pkg_resources

DOCDIR = 'testdocs'

TestDocument = collections.namedtuple('TestDocument', ['name', 'content'])


def get_testdocs():
    req = pkg_resources.Requirement(__package__)
    docdir = os.path.join(__package__, DOCDIR)
    for filename in pkg_resources.resource_listdir(req, docdir):
        name, ext = os.path.splitext(filename)
        f = pkg_resources.resource_stream(req, os.path.join(docdir, filename))
        content = f.read()
        f.close()
        yield TestDocument(name, content)


def canonicalize(xml_data):
    element = defusedxml.lxml.XML(xml_data)
    tree = element.getroottree()
    output = io.BytesIO()
    tree.write_c14n(output)
    return output.getvalue()


def check_conversion(converter, xml_data):
    json_data = converter.xml_to_json(xml_data)
    new_xml_data = converter.json_to_xml(json_data)
    return (canonicalize(xml_data) == canonicalize(new_xml_data))
