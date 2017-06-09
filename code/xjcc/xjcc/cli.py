# -*- coding: utf-8 -*-
import datetime
import logging
import os
import sys
import concurrent.futures
from . import testing
from . import testcase
from . import plugins
from . import output

try:
    import blessings
except ImportError:
    blessings = None

TEXTRESULTS = {
    None: 'ERROR',
    True: 'OK',
    False: 'FAILED',
}


def get_converters(name=None):
    for converter in sorted(plugins.get_converters(), key=lambda x: x.name):
        if name is None or name == converter.name:
            yield converter


def get_testcases(name=None, category=None):
    for tc in sorted(
            testing.get_tests(category=category), key=lambda x: x.name):
        if name is None or name == tc.name:
            yield tc


def sort_testresults(row):
    return '-'.join([row['Converter'], row['Testcase']])


def list_converters(args):
    converters = list(get_converters())
    if not converters:
        print('No converters available.')
        return

    outtable = output.OutputTable(['Name', 'Description'])
    for conv in converters:
        outtable.add({'Name': conv.name, 'Description': conv.desc})

    print(outtable.output(fmt=args.format, title='Converters'))


def list_testcases(args):
    testcases = list(get_testcases(category=args.category))
    if not testcases:
        print('No testcases available.')
        return

    outtable = output.OutputTable(['Name', 'Basename', 'Description'])
    for test in testcases:
        outtable.add({
            'Name': test.name,
            'Basename': test.shortname,
            'Description': test.description,
        })

    outtable.output(fmt=args.format, title='Converters')


def test_conversion(args):
    logger = logging.getLogger(__name__)
    testcases = list(get_testcases(category=args.category))
    if not testcases:
        print('No testcases available.')
        return
    if args.testcase:
        testcases = filter(lambda x: x.shortname == args.testcase, testcases)

    converters = list(get_converters(name=args.name))
    if not converters:
        if args.name:
            print('No converter named \'%s\' found.' % args.name)
        else:
            print('No converters available.')
        return

    output_dir = args.output_dir if args.write_data else None
    if output_dir:
        output_root = os.path.join(
                output_dir, 'xjcc-%s' % (
                    datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')))
        os.mkdir(output_root)

        handler = logging.FileHandler(os.path.join(output_root, 'xjcc.log'))
        root_logger = logging.getLogger()
        root_logger.addHandler(handler)

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        futures = []
        for tc in testcases:
            logger.debug('Queued testcase  \'%s\'...', tc.name)
            future = executor.submit(tc.test_all_converters, converters)
            futures.append(future)

        outtable = output.OutputTable(['Converter', 'Testcase', 'Result'])
        for future in concurrent.futures.as_completed(futures):
            for testresult in future.result():
                resultstr = TEXTRESULTS[testresult.test_passed]
                logger.debug('Testcase  \'%s\' ended with result: %s.',
                             testresult.test.name,
                             resultstr)
                outtable.add({
                    'Converter': testresult.converter.name,
                    'Testcase': testresult.test.name,
                    'Result': resultstr,
                })
                if output_dir:
                    output.write_results(testresult, output_root)

    if output_dir:
        for fmt in ['text', 'json', 'csv']:
            outdata = outtable.output(fmt=fmt, title='Test result',
                                      sort_key=sort_testresults)
            fname = os.path.join(output_root, os.extsep.join(['results', fmt]))
            with open(fname, mode="w", encoding="utf-8") as f:
                f.write(outdata)

        logger.info('Output written to \'%s\'.', output_root)
        root_logger.removeHandler(handler)

    print(outtable.output(fmt=args.format, title='Test result',
                          sort_key=sort_testresults))


def canonicalize(args):
    # FIXME: We need this line due to Python Issue #14156
    # See https://bugs.python.org/issue14156 for details.
    args.file = args.file.buffer if hasattr(args.file, 'buffer') else args.file
    xml_data = args.file.read()
    print(testcase.canonicalize(xml_data).decode())


def convert_file(args):
    # FIXME: We need this line due to Python Issue #14156
    # See https://bugs.python.org/issue14156 for details.
    args.file = args.file.buffer if hasattr(args.file, 'buffer') else args.file
    input_data = args.file.read()

    try:
        converter = list(get_converters(name=args.converter))[0].module
    except IndexError:
        print('No converter named \'%s\' found.' % args.name)
        return

    if args.direction == 'xml-to-json':
        output = converter.xml_to_json(input_data)
    elif args.direction == 'json-to-xml':
        output = converter.json_to_xml(input_data)
    else:
        json_data = converter.xml_to_json(input_data)
        output = converter.json_to_xml(json_data)

    sys.stdout.buffer.write(output)
