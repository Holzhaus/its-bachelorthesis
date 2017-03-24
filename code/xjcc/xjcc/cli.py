# -*- coding: utf-8 -*-
import logging
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

    textresults = {
        None: 'ERROR',
        True: 'OK',
        False: 'FAILED',
    }

    if blessings:
        term = blessings.Terminal()
        textresults = {
            None: term.red('ERROR'),
            True: term.green('OK'),
            False: term.yellow('FAILED'),
        }

    width = max(len(x) for x in textresults.values()) + 2
    fmt = '  [{{result:^{width}}}] {{name}}'.format(width=width)

    for converter in converters:
        print('Converter \'%s\':' % converter.name)
        for chk, result in run_checks(checks, converter):
            textresult = textresults[result]
            print(fmt.format(result=textresult, name=chk.name))
        print('')


def run_checks(checks, converter):
        logger = logging.getLogger(__name__)
        checks_passed = 0
        for chk in checks:
            try:
                result = check.check_conversion(converter.module, chk.content)
            except Exception:
                result = None
                logger.debug('Error occured during conversion', exc_info=True)
            else:
                if result:
                    checks_passed += 1
            yield (chk, result)
        logger.info('Converter \'%s\' passed %d out of %d checks',
                    checks_passed, len(checks))


def canonicalize(args):
    # FIXME: We need this line due to Python Issue #14156
    # See https://bugs.python.org/issue14156 for details.
    args.file = args.file.buffer if hasattr(args.file, 'buffer') else args.file
    xml_data = args.file.read()
    print(check.canonicalize(xml_data).decode())
