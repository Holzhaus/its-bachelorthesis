# -*- coding: utf-8 -*-
import logging
from . import check
from . import plugins


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

    converter = plugins.get_converter(args.name)
    if not converter:
        print('No converter named \'%s\' found.' % args.name)
        return

    print('Checking converter \'%s\'...' % converter.name)
    for chk in checks:
        try:
            result = check.check_converter(converter.module, chk.content)
        except Exception:
            textresult = 'Error'
            logger.debug('Error occured during conversion', exc_info=True)
        else:
            textresult = 'OK' if result else 'Failed'
        print('%s: %s' % (chk.name, textresult))


def canonicalize(args):
    # FIXME: We need this line due to Python Issue #14156
    # See https://bugs.python.org/issue14156 for details.
    args.file = args.file.buffer if hasattr(args.file, 'buffer') else args.file
    xml_data = args.file.read()
    print(check.canonicalize(xml_data).decode())
