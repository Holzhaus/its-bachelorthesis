# -*- coding: utf-8 -*-
import atexit
import itertools
import logging
import os
import collections
import re
import subprocess
import tempfile
import pkg_resources

atexit.register(pkg_resources.cleanup_resources)

Plugin = collections.namedtuple('Plugin', [
    'name',
    'module',
    'entrypoint',
    'desc',
    'meta'
])

GROUP = 'xjcc.converters'


def get_converters(name=None):
    logger = logging.getLogger(__name__)
    for entrypoint in pkg_resources.iter_entry_points(GROUP, name=name):
        logger.debug('Trying to load entrypoint \'%s\'...', entrypoint.name)
        try:
            module = entrypoint.load()
        except Exception as e:
            logger.info('Unable to load entrypoint \'%s\'', entrypoint.name)
            logger.debug('Error occured!', exc_info=True)
        else:
            logger.info('Entrypoint \'%s\' loaded.', entrypoint.name)
            desc, metadata = parse_docstring(module.__doc__)
            yield Plugin(entrypoint.name, module, entrypoint, desc, metadata)


def get_converter(name):
    converters = get_converters(name=name)
    try:
        converter = list(itertools.islice(converters, 1))[0]
    except IndexError:
        return None
    else:
        return converter


def parse_docstring(docstring):
    desc, sep, metadatastring = docstring.strip().partition('\n\n')
    desc = re.sub(r'\s*\n\s*', '\n', desc)
    metadata = {}
    for line in metadatastring.splitlines():
        key, value = (value.strip() for value in line.partition('=')[::2])
        if key:
            metadata[key] = value
    return (desc, metadata)


def get_package_name(name):
    return name.rpartition('.')[0]


def get_package_filename(modulename, filename):
    pkg = get_package_name(modulename)
    return pkg_resources.resource_filename(
        pkg_resources.Requirement(pkg),
        os.path.join(pkg, filename),
    )


def run_command(cmd, data, env=None):
    logger = logging.getLogger(__name__)
    with tempfile.SpooledTemporaryFile() as f:
        f.write(data)
        f.seek(0)
        with tempfile.SpooledTemporaryFile() as err_f:
            try:
                output = subprocess.check_output(cmd, stdin=f, stderr=err_f,
                                                 env=env)
            except subprocess.CalledProcessError as e:
                err_f.seek(0)
                errors = err_f.read().decode().strip()
                logger.debug('stderr contents: %s', errors)
                raise e
    return output
