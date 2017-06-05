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
    logger = logging.getLogger(__name__)
    if category:
        category_map = [(category, testcase.CATEGORIES[category])]
    else:
        category_map = testcase.CATEGORIES.items()

    for raw_dir in DOCDIRS:
        searchdir = os.path.abspath(os.path.expanduser(raw_dir))
        logger.debug('Searching for testcases in \'%s\'...', searchdir)
        for category, category_class in category_map:
            path = os.path.join(searchdir, category)
            if not os.path.isdir(path):
                continue
            for root, dirs, files in os.walk(path):
                for filename in files:
                    name, ext = os.path.splitext(filename)
                    if ext != '.testcase':
                        continue
                    filepath = os.path.join(root, filename)
                    try:
                        tc = category_class(filepath)
                    except Exception:
                        logger.warning('Failed to instantiate testcase \'%s\'',
                                       filepath, exc_info=logger.isEnabledFor(
                                           logging.DEBUG))
                    else:
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
