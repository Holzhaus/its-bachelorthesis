# -*- coding: utf-8 -*-
import csv
import json
import logging
import sys
from . import testing
from . import plugins

try:
    import blessings
except ImportError:
    blessings = None


def list_converters(args):
    converters = sorted(plugins.get_converters(), key=lambda x: x.name)
    if not converters:
        print('No converters available.')
        return

    for conv in converters:
        print(conv.name, conv.desc)


def list_testcases(args):
    tests = sorted(testing.get_tests(), key=lambda x: x.name)
    if not tests:
        print('No testcases available.')
        return

    for test in tests:
        print(test.name)


def test_conversion(args):
    logger = logging.getLogger(__name__)
    tests = sorted(testing.get_tests(), key=lambda x: x.name)
    if not tests:
        print('No testcases available.')
        return

    if not args.name:
        converters = sorted(plugins.get_converters(), key=lambda x: x.name)
        if not converters:
            print('No converters available.')
            return
    else:
        converter = plugins.get_converter(args.name)
        if not converter:
            print('No converter named \'%s\' found.' % args.name)
            return
        converters = [converter]

    results = {}
    for converter in converters:
        logger.debug('Testing converter  \'%s\'...', converter.name)
        results[converter.name] = list(testing.run_tests(converter, tests))
        logger.debug('Testing converter  \'%s\' done.', converter.name)

    textresults = {
        None: 'ERROR',
        True: 'OK',
        False: 'FAILED',
    }

    if args.format == 'text':
        if blessings:
            term = blessings.Terminal()
            textresults = {
                None: term.red(textresults[None]),
                True: term.green(textresults[True]),
                False: term.yellow(textresults[False]),
            }

        width = max(len(x) for x in textresults.values()) + 2
        fmt = '  [{{result:^{width}}}] {{name}}'.format(width=width)

        for converter_name, resultlist in results.items():
            print('Converter \'%s\':' % converter_name)
            for result in resultlist:
                textresult = textresults[result.test_passed]
                print(fmt.format(result=textresult, name=result.test.name))
            print('')
    else:
        data = {
            converter_name: {
                result.test.name: textresult[result.test_passed]
                for result in resultlist
            }
            for converter_name, resultlist in results
        }
        if args.format == 'json':
            print(json.dumps(data))
        elif args.format == 'csv':
            fieldnames = ['converter'] + list(list(data.values())[0].keys())
            writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
            writer.writeheader()
            for converter, tests in data.items():
                result = {**{'converer': converter}, **tests}
                writer.writerow(result)


def canonicalize(args):
    # FIXME: We need this line due to Python Issue #14156
    # See https://bugs.python.org/issue14156 for details.
    args.file = args.file.buffer if hasattr(args.file, 'buffer') else args.file
    xml_data = args.file.read()
    print(testing.canonicalize(xml_data).decode())
