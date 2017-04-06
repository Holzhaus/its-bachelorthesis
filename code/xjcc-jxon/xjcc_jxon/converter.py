# -*- coding: utf-8 -*-
"""
Implementation of Mozilla's JavaScript XML Object Notation (JXON)
https://github.com/tyrasd/jxon
"""
import logging
import os
import subprocess
import xjcc.plugins

NODE_APP = xjcc.plugins.get_package_filename(__name__, 'jxonconverter.js')


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
    cmd = ['node', NODE_APP]
    return xjcc.plugins.run_command(cmd, xml_data, env=ENV)


def json_to_xml(json_data):
    cmd = ['node', NODE_APP, '--decode']
    return xjcc.plugins.run_command(cmd, json_data, env=ENV)
