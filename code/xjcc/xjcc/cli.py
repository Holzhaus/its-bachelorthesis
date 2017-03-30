# -*- coding: utf-8 -*-
import csv
import json
import logging
import sys
from . import check
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


def list_checks(args):
    checks = sorted(check.get_testdocs(), key=lambda x: x.name)
    if not checks:
        print('No checks available.')
        return

    for chk in checks:
        print(chk.name)


def check_conversion(args):
    logger = logging.getLogger(__name__)
    checks = sorted(check.get_testdocs(), key=lambda x: x.name)
    if not checks:
        print('No checks available.')
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
        results[converter.name] = list(check.run_checks(converter, checks))
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
            print('Converter \'%s\':' % converter.name)
            for result in resultlist:
                textresult = textresults[result.passed]
                print(fmt.format(result=textresult, name=result.check.name))
            print('')
    else:
        jsonresults = {
            converter_name: {
                result.check.name: textresult[result.passed]
                for result in resultlist
            }
            for converter_name, resultlist in results
        }
        if args.format == 'json':
            print(json.dumps(results))
        elif args.format == 'csv':
            fieldnames = ['converter'] + list(list(results.values())[0].keys())
            writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
            writer.writeheader()
            for converter, tests in results.items():
                result = {**{'converter': converter}, **tests}
                writer.writerow(result)


def canonicalize(args):
    # FIXME: We need this line due to Python Issue #14156
    # See https://bugs.python.org/issue14156 for details.
    args.file = args.file.buffer if hasattr(args.file, 'buffer') else args.file
    xml_data = args.file.read()
    print(check.canonicalize(xml_data).decode())
