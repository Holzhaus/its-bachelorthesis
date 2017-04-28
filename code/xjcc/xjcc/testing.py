# -*- coding: utf-8 -*-
import logging
import os
import pkg_resources
from . import testcase

DOCDIR = 'testdocs'


def get_tests(category=None):
    req = pkg_resources.Requirement(__package__)
    if category:
        category_map = [(category, testcase.CATEGORIES[category])]
    else:
        category_map = testcase.CATEGORIES.items()

    for category, category_class in category_map:
        docdir = os.path.join(__package__, DOCDIR, category)
        path = os.path.abspath(pkg_resources.resource_filename(req, docdir))
        for root, dirs, files in os.walk(path):
            for filename in files:
                name, ext = os.path.splitext(filename)
                if ext != '.testcase':
                    continue
                filepath = os.path.join(root, filename)
                tc = category_class(filepath)
                yield tc


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
