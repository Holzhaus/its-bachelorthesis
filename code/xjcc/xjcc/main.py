# -*- coding: utf-8 -*-
import argparse
import logging
import os
from . import cli
from . import testcase


OUTPUT_FORMATS = [
    'text',
    'json',
    'csv',
]


def writable_directory(path):
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(
                'The directory {} does not exist!'.format(path))
    if not os.access(path, os.W_OK):
        raise argparse.ArgumentTypeError(
                'The directory {} is not writable!'.format(path))
    return path


def parse_args(args=None):
    parser = argparse.ArgumentParser()

    loglevel = parser.add_mutually_exclusive_group()
    loglevel.add_argument(
        '-v', '--verbose',
        dest='loglevel',
        action='store_const',
        const=logging.INFO,
        default=logging.WARNING,
        help='Be verbose',
    )
    loglevel.add_argument(
        '-vv', '--debug',
        dest='loglevel',
        action='store_const',
        const=logging.DEBUG,
        help='Even show debug messages'
    )

    loglevel.add_argument(
        '-q', '--quiet',
        dest='loglevel',
        action='store_const',
        const=100,
        help='Be quiet',
    )

    subparsers = parser.add_subparsers(
        dest='command',
        )
    subparsers.required = True

    # convert-file
    parser_convert = subparsers.add_parser(
        'convert-file',
        help='convert file'
    )
    parser_convert.add_argument('converter')
    parser_convert.add_argument('file', type=argparse.FileType('rb'))
    parser_convert_dir = parser_convert.add_mutually_exclusive_group()
    parser_convert_dir.add_argument('--xml-to-json', action='store_const',
                                    dest='direction', const='xml-to-json',
                                    default='xml-to-json')
    parser_convert_dir.add_argument('--json-to-xml', action='store_const',
                                    dest='direction', const='json-to-xml')
    parser_convert_dir.add_argument('--roundtrip', action='store_const',
                                    dest='direction', const='roundtrip')
    parser_convert.set_defaults(func=cli.convert_file)

    # list-converters
    parser_list = subparsers.add_parser(
        'list-converters',
        help='list database contents'
    )
    parser_list.add_argument('-f', '--format',
                                       choices=OUTPUT_FORMATS, default='text')
    parser_list.set_defaults(func=cli.list_converters)

    # list-tests
    parser_listtestcases = subparsers.add_parser(
        'list-testcases',
        help='list tests'
    )
    parser_listtestcases.add_argument('-c', '--category', default=None,
            action='store', choices=testcase.CATEGORIES.keys(),
            help='Only use testcases from a single category')
    parser_listtestcases.add_argument('-f', '--format',
                                       choices=OUTPUT_FORMATS, default='text')
    parser_listtestcases.set_defaults(func=cli.list_testcases)

    # test-conversion
    parser_testconversion = subparsers.add_parser(
        'test-conversion',
        help='test conversion'
    )
    parser_testconversion.add_argument('-c', '--category', default=None,
            action='store', choices=testcase.CATEGORIES.keys(),
            help='Only use testcases from a single category')
    parser_testconversion.add_argument('-f', '--format',
                                       choices=OUTPUT_FORMATS, default='text')
    parser_testconversion.add_argument('-w', '--write-data',
        action='store_true')
    parser_testconversion.add_argument('-o', '--output-dir', default='.',
        type=writable_directory)
    parser_testconversion.add_argument('name', nargs='?')
    parser_testconversion.set_defaults(func=cli.test_conversion)

    # canonicalize
    parser_canonicalize = subparsers.add_parser(
        'canonicalize',
        help='Canonicalize an XML document'
    )
    parser_canonicalize.add_argument('file', type=argparse.FileType('rb'))
    parser_canonicalize.set_defaults(func=cli.canonicalize)

    # Finally parse arguments
    return parser.parse_args(args)


def main(args=None):
    p_args = parse_args(args)
    logging.basicConfig(level=p_args.loglevel)
    return p_args.func(p_args)
