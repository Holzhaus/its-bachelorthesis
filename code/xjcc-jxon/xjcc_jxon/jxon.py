# -*- coding: utf-8 -*-
"""
Implementation of Mozilla's JavaScript XML Object Notation (JXON)
https://github.com/tyrasd/jxon
"""

import atexit
import subprocess
import tempfile
import pkg_resources

atexit.register(pkg_resources.cleanup_resources)

NODE_APP = pkg_resources.resource_filename(
    pkg_resources.Requirement(__package__),
    'jxonconverter.js')


def xml_to_json(xml_data):
    with tempfile.SpooledTemporaryFile() as f:
        f.write(xml_data)
        f.seek(0)
        return subprocess.check_output(['node', NODE_APP], stdin=f)


def json_to_xml(json_data):
    with tempfile.SpooledTemporaryFile() as f:
        f.write(json_data)
        f.seek(0)
        return subprocess.check_output(['node', NODE_APP, '--decode'], stdin=f)
