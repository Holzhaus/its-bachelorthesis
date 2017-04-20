# -*- coding: utf-8 -*-
import csv
import datetime
import json
import logging
import os
import sys
import concurrent.futures
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

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_to_converter = {}
        for converter in converters:
            logger.debug('Queued testing converter  \'%s\'...', converter.name)
            future = executor.submit(testing.run_tests, converter, tests)
            future_to_converter[future] = converter.name

        results = {}
        for future in concurrent.futures.as_completed(future_to_converter):
            logger.debug('Testing converter  \'%s\' done.', converter.name)
            fs_result = future.result()
            converter_name = future_to_converter[future]
            results[converter_name] = list(fs_result)

    output_dir = args.output_dir if args.write_data else None
    if output_dir:
        output_root = os.path.join(
                output_dir, 'xjcc-%s' % datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        os.mkdir(output_root)
        for converter_name, testresults in results.items():
            path = os.path.join(output_root, converter_name)
            os.mkdir(path)
            for testresult in testresults:
                if testresult.json_output is not None:
                    json_file = os.path.join(
                            path, '%s.json' % testresult.test.name)
                    with open(json_file, mode='wb') as f:
                        f.write(testresult.json_output)

                if testresult.xml_output is not None:
                    xml_file = os.path.join(
                            path, '%s.xml' % testresult.test.name)
                    with open(xml_file, mode='wb') as f:
                        f.write(testresult.xml_output)
        logger.info('Output written to \'%s\'.', output_root)

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
