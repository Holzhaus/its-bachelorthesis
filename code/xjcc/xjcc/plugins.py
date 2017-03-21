# -*- coding: utf-8 -*-
import itertools
import collections
import re
import pkg_resources

Plugin = collections.namedtuple('Plugin', [
    'name',
    'module',
    'entrypoint',
    'desc',
    'meta'
])

GROUP = 'xjcc.converters'


def get_converters(name=None):
    for entrypoint in pkg_resources.iter_entry_points(GROUP, name=name):
        module = entrypoint.load()
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
