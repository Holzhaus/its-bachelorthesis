# -*- coding: utf-8 -*-
import abc
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
            plugin_class = entrypoint.load()
            plugin = plugin_class(entrypoint.module_name)
        except Exception as e:
            logger.info('Unable to load entrypoint \'%s\'', entrypoint.name)
            logger.debug('Error occured!', exc_info=True)
        else:
            logger.info('Entrypoint \'%s\' loaded.', entrypoint.name)
            desc, metadata = parse_docstring(plugin_class.__doc__)
            yield Plugin(entrypoint.name, plugin, entrypoint, desc, metadata)


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


class ConverterPlugin(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name):
        self.name = name

    def get_package_name(self):
        return self.name.rpartition('.')[0] if '.' in self.name else self.name

    def get_package_filename(self, filename):
        pkg = self.get_package_name()
        return pkg_resources.resource_filename(
            pkg_resources.Requirement(pkg),
            os.path.join(pkg, filename),
        )

    def run_command(self, cmd, data, env=None):
        logger = logging.getLogger(__name__)
        with tempfile.SpooledTemporaryFile() as f:
            f.write(data)
            f.seek(0)
            with tempfile.SpooledTemporaryFile() as out_f:
                logger.debug('Invoking: %s', subprocess.list2cmdline(cmd))
                with subprocess.Popen(cmd, stdin=f, stdout=out_f,
                                      stderr=subprocess.PIPE, env=env) as proc:

                    errors = []
                    for line in iter(proc.stderr.readline, b''):
                        errmsg = line.decode().strip()
                        errors.append(errmsg)
                        logger.debug(errmsg)

                    returncode = proc.wait()
                    logger.debug('Process ended with status %d', returncode)

                    out_f.seek(0)
                    output = out_f.read()

                    if returncode != 0:
                        e = subprocess.CalledProcessError(returncode, cmd,
                                                          output=output)
                        e.stderr = errors
                        raise e
        return output

    @abc.abstractmethod
    def xml_to_json(self, data):
        pass

    @abc.abstractmethod
    def json_to_xml(self, data):
        pass


class NodejsConverterPlugin(ConverterPlugin):
    ENCODE_ARGS = []
    DECODE_ARGS = ['--decode']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.node_app = self.get_package_filename('converter.js')
        self.node_env = self.get_env()

    def get_env(self):
        """
        Get an environment dict and ensure that the NODE_PATH variable is set,
        so that globally installed node_modules can be found.
        """
        logger = logging.getLogger(self.name)
        env = os.environ.copy()
        if not env.get('NODE_PATH', None):
            cmd = ['npm', 'root', '--global']
            try:
                node_path = subprocess.check_output(cmd).decode().strip()
            except Exception:
                logger.warning('Unable to query the global nodejs module ' +
                               'path! Is npm installed?')
                logger.debug('Logging traceback...', exc_info=True)
                node_path = ''
            env['NODE_PATH'] = node_path
        logger.debug('NODE_PATH = \'%s\'', env.get('NODE_PATH'))
        return env

    def xml_to_json(self, xml_data):
        cmd = ['node', self.node_app]
        cmd.extend(self.ENCODE_ARGS)
        return self.run_command(cmd, xml_data, env=self.node_env)

    def json_to_xml(self, json_data):
        cmd = ['node', self.node_app]
        cmd.extend(self.DECODE_ARGS)
        return self.run_command(cmd, json_data, env=self.node_env)
