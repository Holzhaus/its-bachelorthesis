# -*- coding: utf-8 -*-
import datetime
import logging
import os
import sys
import concurrent.futures
from . import testing
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
    for testcase in sorted(
            testing.get_tests(category=category), key=lambda x: x.name):
        if name is None or name == testcase.name:
            yield testcase


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

    outtable.output(fmt=args.format, title='Converters')


def list_testcases(args):
    testcases = list(get_testcases(category=args.category))
    if not testcases:
        print('No testcases available.')
        return

    outtable = output.OutputTable(['Name', 'Basename', 'Description'])
    for test in testcases:
        outtable.add({'Name': test.name, 'Basename': test.shortname, 'Description': test.description})

    outtable.output(fmt=args.format, title='Converters')

def test_conversion(args):
    logger = logging.getLogger(__name__)
    testcases = list(get_testcases(category=args.category))
    if not testcases:
        print('No testcases available.')
        return

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
                output_dir, 'xjcc-%s' % datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        os.mkdir(output_root)

        handler = logging.FileHandler(os.path.join(output_root, 'xjcc.log'))
        root_logger = logging.getLogger()
        root_logger.addHandler(handler)

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        futures = []
        for testcase in testcases:
            logger.debug('Queued testcase  \'%s\'...', testcase.name)
            future = executor.submit(testcase.test_all_converters, converters)
            futures.append(future)

        results = {}
        outtable = output.OutputTable(['Converter', 'Testcase', 'Result'])
        for future in concurrent.futures.as_completed(futures):
            for testresult in future.result():
                logger.debug('Testcase  \'%s\' done.', testresult.test.name)
                converter_name = testresult.converter.name
                if converter_name not in results:
                    results[converter_name] = []
                results[converter_name].append(testresult)
                outtable.add({
                    'Converter': converter_name,
                    'Testcase': testresult.test.name,
                    'Result': TEXTRESULTS[testresult.test_passed],
                })

    if output_dir:
        for converter_name, testresults in results.items():
            path = os.path.join(output_root, converter_name)
            os.mkdir(path)
            for testresult in testresults:
                if testresult.json_output is not None:
                    json_file = os.path.join(
                            path, '%s.json' % testresult.test.shortname)
                    with open(json_file, mode='wb') as f:
                        f.write(testresult.json_output)

                if testresult.xml_output is not None:
                    xml_file = os.path.join(
                            path, '%s.xml' % testresult.test.name)
                    with open(xml_file, mode='wb') as f:
                        f.write(testresult.xml_output)

        for fmt in ['text', 'json', 'xml']:
            outdata = outtable.output(fmt=fmt.format, title='Test result',
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
    print(testing.canonicalize(xml_data).decode())


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

