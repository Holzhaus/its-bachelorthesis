# -*- coding: utf-8 -*-
import abc
import collections
import io
import logging
import os
import defusedxml.lxml
import pkg_resources
import demjson
from . import requestlogger

DOCDIR = 'testdocs'

TestResult = collections.namedtuple('TestResult', [
    'test',
    'test_passed',
    'json_output',
    'xml_output',
])


class TestCase(object):
    __meta__ = abc.ABCMeta

    def __init__(self, name, xml_data):
        self.name = name
        self.xml_data = xml_data

    def get_conversion_data(self, converter):
        json_output = converter.xml_to_json(self.xml_data)
        xml_output = converter.json_to_xml(json_output)
        return (json_output, xml_output)

    @abc.abstractmethod
    def run(self, converter):
        pass


class ConversionTestCase(TestCase):
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
        else:
            json_errors = demjson.decode(json_output, strict=True, return_errors=True, return_stats=False, write_errors=False)[1]
            if json_errors:
                passed = False
                logger.info('Erroneous JSON: %r', json_errors)
        return TestResult(
            test=self,
            test_passed=passed,
            json_output=json_output,
            xml_output=xml_output,
        )


class URLInvocationTestCase(TestCase):
    def run(self, converter):
        logger = logging.getLogger(__name__)
        with requestlogger.run(server_address=('localhost', 56789)) as server:
            try:
                json_output, xml_output = self.get_conversion_data(
                        converter.module)
            except Exception:
                json_output = None
                xml_output = None
                logger.debug('Error occured during conversion', exc_info=True)
            requests = server.get_requests()
            passed = (len(requests) == 0)
        return TestResult(
            test=self,
            test_passed=passed,
            json_output=json_output,
            xml_output=xml_output,
        )


TESTCASE_CATEGORIES = {
    'conversion': ConversionTestCase,
    'urlinvocation': URLInvocationTestCase,
}


def get_tests(category=None):
    req = pkg_resources.Requirement(__package__)
    if category:
        category_map = [(category, TESTCASE_CATEGORIES[category])]
    else:
        category_map = TESTCASE_CATEGORIES.items()

    for category, category_class in category_map:
        docdir = os.path.join(__package__, DOCDIR, category)
        for filename in pkg_resources.resource_listdir(req, docdir):
            name, ext = os.path.splitext(filename)
            if ext != '.xml':
                continue
            filepath = os.path.join(docdir, filename)
            f = pkg_resources.resource_stream(req, filepath)
            content = f.read()
            f.close()
            yield category_class(name, content)


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

