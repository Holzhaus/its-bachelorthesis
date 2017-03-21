# -*- coding: utf-8 -*-
import collections
import pkg_resources

Plugin = collections.namedtuple('Plugin', [
    'name',
    'module',
    'entrypoint',
    'desc',
    'meta'
])


def get_converters():
    for entrypoint in pkg_resources.iter_entry_points('xjcc.converters'):
        module = entrypoint.load()
        desc, metadata = parse_docstring(module.__doc__)
        yield Plugin(entrypoint.name, module, entrypoint, desc, metadata)


def parse_docstring(docstring):
    desc, sep, metadatastring = docstring.strip().partition('\n\n')
    metadata = {}
    for line in metadatastring.splitlines():
        key, value = (value.strip() for value in line.partition('=')[::2])
        if key:
            metadata[key] = value
    return (desc, metadata)
