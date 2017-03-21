# -*- coding: utf-8 -*-
import argparse
import logging
from . import cli


def main(args=None):
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

    # list-checks
    parser_listchecks = subparsers.add_parser(
        'list-checks',
        help='list checks'
    )
    parser_listchecks.set_defaults(func=cli.list_checks)

    # check-conversion
    parser_checkconversion = subparsers.add_parser(
        'check-conversion',
        help='check conversion'
    )
    parser_checkconversion.add_argument('name')
    parser_checkconversion.set_defaults(func=cli.check_conversion)

    # Parse arguments and execute code
    p_args = parser.parse_args(args)
    logging.basicConfig(level=p_args.loglevel)
    p_args.func(p_args)
