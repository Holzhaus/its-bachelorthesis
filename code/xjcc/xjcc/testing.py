# -*- coding: utf-8 -*-
import collections
import io
import logging
import os
import defusedxml.lxml
import pkg_resources

DOCDIR = 'testdocs'

TestResult = collections.namedtuple('TestResult', [
    'test',
    'test_passed',
    'json_output',
    'xml_output',
])


class TestCase(object):
    def __init__(self, name, xml_data):
        self.name = name
        self.xml_data = xml_data

    def get_conversion_data(self, converter):
        json_output = converter.xml_to_json(self.xml_data)
        xml_output = converter.json_to_xml(json_output)
        return (json_output, xml_output)

    def run(self, converter):
        logger = logging.getLogger(__name__)
        try:
            json_output, xml_output = self.get_conversion_data(converter.module)
            passed = (canonicalize(self.xml_data) == canonicalize(xml_output))
        except Exception:
            passed = None
            json_output = None
            xml_output = None
            logger.debug('Error occured during conversion', exc_info=True)
        return TestResult(
            test=self,
            test_passed=passed,
            json_output=json_output,
            xml_output=xml_output,
        )


def get_tests():
    req = pkg_resources.Requirement(__package__)
    docdir = os.path.join(__package__, DOCDIR)
    for filename in pkg_resources.resource_listdir(req, docdir):
        name, ext = os.path.splitext(filename)
        if ext != '.xml':
            continue
        f = pkg_resources.resource_stream(req, os.path.join(docdir, filename))
        content = f.read()
        f.close()
        yield TestCase(name, content)


def canonicalize(xml_data):
    element = defusedxml.lxml.XML(xml_data)
    tree = element.getroottree()
    output = io.BytesIO()
    tree.write_c14n(output)
    return output.getvalue()


def run_tests(converter, tests):
    logger = logging.getLogger(__name__)
    tests_passed = 0
    for test in tests:
        result = test.run(converter)
        if result.test_passed:
            tests_passed += 1
        yield result
    logger.info('Converter \'%s\' passed %d out of %d tests',
                converter.name, tests_passed, len(tests))

