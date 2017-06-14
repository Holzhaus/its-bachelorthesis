# -*- coding: utf-8 -*-
import logging
import os
import subprocess
import xjcc.plugins


class GreenCapeXmlPlugin(xjcc.plugins.ConverterPlugin):
    """
    A PHP XML parser class that provides an easy way to convert XML into native PHP arrays and back again.
    https://github.com/GreenCape/xml-converter
    """
    PHP_PATH = 'converter.php'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.php_app = self.get_package_filename(self.PHP_PATH)
        self.php_env = self.get_env()

    def get_env(self):
        """
        Get an environment dict and ensure that the COMPOSER_HOME variable is
        set, so that globally installed composer packages can be found.
        """
        logger = logging.getLogger(self.name)
        env = os.environ.copy()
        if not env.get('COMPOSER_HOME', None):
            cmd = ['composer', 'config', 'home']
            try:
                composer_path = subprocess.check_output(cmd).decode().strip()
            except Exception:
                logger.warning('Unable to query the global composer ' +
                               'path! Is composer installed?')
                logger.debug('Logging traceback...', exc_info=True)
                composer_path = ''
            env['COMPOSER_HOME'] = composer_path
        logger.debug('COMPOSER_HOME = \'%s\'', env.get('COMPOSER_HOME'))
        return env

    def xml_to_json(self, xml_data):
        cmd = ['php', self.php_app]
        return self.run_command(cmd, xml_data, env=self.php_env)

    def json_to_xml(self, json_data):
        cmd = ['php', self.php_app, '--decode']
        return self.run_command(cmd, json_data, env=self.php_env)
