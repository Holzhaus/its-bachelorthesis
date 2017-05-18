# -*- coding: utf-8 -*-
import logging
import os
from . import testcase

DOCDIRS = [
    '/usr/share/xjcc/test-documents',
    '/etc/xjcc/test-documents',
    '~/.xjcc/test-documents',
    '~/.local/share/xjcc/test-documents',
]


def get_tests(category=None):
    if category:
        category_map = [(category, testcase.CATEGORIES[category])]
    else:
        category_map = testcase.CATEGORIES.items()

    for searchdir in DOCDIRS:
        for category, category_class in category_map:
            path = os.path.join(os.path.expanduser(searchdir), category)
            if not os.path.isdir(path):
                continue
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
