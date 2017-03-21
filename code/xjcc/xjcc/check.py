# -*- coding: utf-8 -*-
import collections
import os
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
