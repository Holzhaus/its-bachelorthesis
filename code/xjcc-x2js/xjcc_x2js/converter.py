# -*- coding: utf-8 -*-
"""
https://github.com/Axinom/x2js
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
    os.path.join(__package__, 'converter.js'),
)


def get_env():
    """
    Get an environment dict and ensure that the NODE_PATH variable is set, so
    that globally installed node_modules can be found.
    """
    logger = logging.getLogger(__name__)
    env = os.environ.copy()
    if not env.get('NODE_PATH', None):
        cmd = ['npm', 'root', '--global']
        try:
            node_path = subprocess.check_output(cmd).decode().strip()
        except Exception:
            logger.warning('Unable to query the global nodejs module path! ' +
                           'Is npm installed?')
            logger.debug('Logging traceback...', exc_info=True)
            node_path = ''
        env['NODE_PATH'] = node_path
    logger.debug('NODE_PATH = \'%s\'', env.get('NODE_PATH'))
    return env


ENV = get_env()


def xml_to_json(xml_data):
    logger = logging.getLogger(__name__)
    cmd = ['node', NODE_APP]
    with tempfile.SpooledTemporaryFile() as f:
        f.write(xml_data)
        f.seek(0)
        with tempfile.SpooledTemporaryFile() as err_f:
            try:
                output = subprocess.check_output(cmd, stdin=f, stderr=err_f,
                                                 env=ENV)
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
                output = subprocess.check_output(cmd, stdin=f, stderr=err_f,
                                                 env=ENV)
            except subprocess.CalledProcessError as e:
                err_f.seek(0)
                errors = err_f.read().decode().strip()
                logger.debug('stderr contents: %s', errors)
                raise e
    return output
