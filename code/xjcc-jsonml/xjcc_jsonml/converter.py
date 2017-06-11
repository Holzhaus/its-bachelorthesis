# -*- coding: utf-8 -*-
from xjcc.plugins import NodejsConverterPlugin


class JsonMLPlugin(NodejsConverterPlugin):
    """
    JsonML-related tools for losslessly converting between XML/HTML and JSON,
    including mixed-mode XML.
    http://jsonml.org
    https://github.com/mckamey/jsonml
    """
    pass


class JsonMLPatchedPlugin(NodejsConverterPlugin):
    """
    JsonML-related tools for losslessly converting between XML/HTML and JSON,
    including mixed-mode XML. (Patched Version)
    http://jsonml.org
    https://github.com/mckamey/jsonml
    """
    ENCODE_ARGS = NodejsConverterPlugin.ENCODE_ARGS + ['--patched']
    DECODE_ARGS = NodejsConverterPlugin.DECODE_ARGS + ['--patched']
