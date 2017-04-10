# -*- coding: utf-8 -*-
import argparse
import logging
import os
from . import cli


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

    # list-converters
    parser_list = subparsers.add_parser(
        'list-converters',
        help='list database contents'
    )
    parser_list.set_defaults(func=cli.list_converters)

    # list-tests
    parser_listtestcases = subparsers.add_parser(
        'list-testcases',
        help='list tests'
    )
    parser_listtestcases.set_defaults(func=cli.list_testcases)

    # test-conversion
    parser_testconversion = subparsers.add_parser(
        'test-conversion',
        help='test conversion'
    )
    parser_testconversion.add_argument('-f', '--format', choices=[
        'json',
        'csv',
        'text',
    ], default='text')
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
