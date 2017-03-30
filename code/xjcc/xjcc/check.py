# -*- coding: utf-8 -*-
import collections
import io
import logging
import os
import defusedxml.lxml
import pkg_resources

DOCDIR = 'testdocs'

TestDocument = collections.namedtuple('TestDocument', ['name', 'content'])
TestResult = collections.namedtuple('TestResult', [
    'check',
    'passed',
    'json_output',
    'xml_output',
])


def get_testdocs():
    req = pkg_resources.Requirement(__package__)
    docdir = os.path.join(__package__, DOCDIR)
    for filename in pkg_resources.resource_listdir(req, docdir):
        name, ext = os.path.splitext(filename)
        if ext != '.xml':
            continue
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


def get_conversion_data(converter, xml_data):
    json_data = converter.xml_to_json(xml_data)
    new_xml_data = converter.json_to_xml(json_data)
    return (json_data, new_xml_data)


def run_check(converter, chk):
    logger = logging.getLogger(__name__)
    try:
        json_output, xml_output = get_conversion_data(converter.module,
                                                      chk.content)
    except Exception:
        passed = None
        json_output = None
        xml_output = None
        logger.debug('Error occured during conversion', exc_info=True)
    else:
        passed = (canonicalize(chk.content) == canonicalize(xml_output))
    return TestResult(
        check=chk,
        passed=passed,
        json_output=json_output,
        xml_output=xml_output,
    )


def run_checks(converter, checks):
    logger = logging.getLogger(__name__)
    checks_passed = 0
    for chk in checks:
        result = run_check(converter, chk)
        if result.passed:
            checks_passed += 1
        yield result
    logger.info('Converter \'%s\' passed %d out of %d checks',
                converter.name, checks_passed, len(checks))

