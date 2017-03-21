# -*- coding: utf-8 -*-
from . import plugins


def list_converters(args):
    converters = sorted(plugins.get_converters(), key=lambda x: x.name)
    if not converters:
        print('No converters available.')
        return

    for conv in converters:
        mod = conv.load()
        desc = ' '.join(mod.__doc__.strip().split())
        print(conv.name, desc)
