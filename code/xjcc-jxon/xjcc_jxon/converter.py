# -*- coding: utf-8 -*-
"""
Implementation of Mozilla's JavaScript XML Object Notation (JXON)
https://github.com/tyrasd/jxon
"""
import atexit
import logging
import os
import subprocess
import tempfile
import pkg_resources

atexit.register(pkg_resources.cleanup_resources)

NODE_APP = pkg_resources.resource_filename(
    pkg_resources.Requirement(__package__),
    os.path.join(__package__, 'jxonconverter.js'),
)


def xml_to_json(xml_data):
    logger = logging.getLogger(__name__)
    cmd = ['node', NODE_APP]
    with tempfile.SpooledTemporaryFile() as f:
        f.write(xml_data)
        f.seek(0)
        with tempfile.SpooledTemporaryFile() as err_f:
            try:
                output = subprocess.check_output(cmd, stdin=f, stderr=err_f)
            except subprocess.CalledProcessError as e:
                err_f.seek(0)
                errors = err_f.read().decode().strip()
                logger.debug('stderr contents: %s', errors)
                raise e
    return output


def json_to_xml(json_data):
    logger = logging.getLogger(__name__)
    cmd = ['node', NODE_APP, '--decode']
    with tempfile.SpooledTemporaryFile() as f:
        f.write(json_data)
        f.seek(0)
        with tempfile.SpooledTemporaryFile() as err_f:
            try:
                output = subprocess.check_output(cmd, stdin=f, stderr=err_f)
            except subprocess.CalledProcessError as e:
                err_f.seek(0)
                errors = err_f.read().decode().strip()
                logger.debug('stderr contents: %s', errors)
                raise e
    return output
