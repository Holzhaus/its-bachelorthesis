# -*- coding: utf-8 -*-
import collections
import configparser
import contextlib
import functools
import io
import logging
import multiprocessing
import os
import pathlib
import re
import signal
import tempfile
import demjson
import defusedxml.lxml
from . import httpserver
from . import process


MAGIC_FSA_STRING = 'THIS_IS_TOP_SECRET_STUFF'
INFO_PATTERN = re.compile(rb'<!--;testcase(?P<info>.*?)-->', re.DOTALL)


TestResult = collections.namedtuple('TestResult', [
    'test',
    'converter',
    'test_passed',
    'json_output',
    'xml_output',
])


class FilePath(str):
    @property
    def url(self):
        return pathlib.Path(self).as_uri()

    @property
    def filename(self):
        return os.path.basename(self)


def canonicalize(xmldata, **kwargs):
    element = defusedxml.lxml.XML(xmldata)
    tree = element.getroottree()
    output = io.BytesIO()
    logger = logging.getLogger(__name__)
    logger.debug('Canonicalization with settings: %r', kwargs)
    tree.write_c14n(output, **kwargs)
    return output.getvalue()


def get_conversion_data(xml_data, converter):
    json_output = converter.xml_to_json(xml_data)
    xml_output = converter.json_to_xml(json_output)
    return (json_output, xml_output)


def parse_responses(cp, path='.'):
    for section in cp.sections():
        match = re.fullmatch(r'ServerResponse (?P<url_path>.+)', section)
        if not match:
            continue
        url_path = match.group('url_path')

        filename = cp[section].get('content', None)
        if not filename:
            content = None
        else:
            with open(os.path.join(path, filename)) as f:
                content = f.read()
        status = cp[section].get('status', None)

        headers = None
        content_type = cp[section].get('content-type', None)
        if content_type is not None:
            headers = {'Content-Type': content_type}

        log_request = cp[section].getboolean('log-request', True)

        yield (url_path, httpserver.PathInfo(
                    content=content, status=status,
                    headers=headers, log_request=log_request))


def parse_files(cp, path='.'):
    for section in cp.sections():
        match = re.fullmatch(r'File (?P<ref>[\w-]+)', section)
        if not match:
            continue
        ref = match.group('ref')

        try:
            filename = cp.get(section, 'path')
        except configparser.Error:
            continue

        with open(os.path.join(path, filename)) as f:
            content = f.read()
        yield (ref, content)


class ConversionTestCase(object):
    def __init__(self, filename):
        logger = logging.getLogger(__name__)
        logger.debug('Possible testcase found at \'%s\'', filename)
        with open(filename, mode='rb') as f:
            fcontent = f.read()
        matchobj = INFO_PATTERN.search(fcontent)
        if not matchobj:
            raise ValueError('Testcase info section not found')
        binary_content = INFO_PATTERN.sub(b'', fcontent, count=1)
        self.content = binary_content.decode('utf-8')
        logger.debug('Testcase primary file length: (%d chars / %d bytes)',
                     len(self.content), len(binary_content))

        self._cp = configparser.ConfigParser()
        self._cp.read_string(matchobj.group('info').decode())

        general = self._cp['General']
        self.name = general.get('name')
        self.description = general.get('description', '')

        self.c14n_kwargs = {
            'with_comments': self._cp.getboolean('C14N', 'with-comments',
                                                 fallback=False),
        }

        self.filename = os.path.abspath(filename)
        self.shortname = os.path.basename(os.path.splitext(self.filename)[0])

    @property
    def path(self):
        return os.path.dirname(self.filename)

    def test_converters(self, converters):
        logger = logging.getLogger(__name__)

        xmldata = self.content.encode('utf-8')
        xmldata_c14n = canonicalize(xmldata, **self.c14n_kwargs)
        for converter in converters:
            logger.info('Started testcase \'%s\' for converter \'%s\'',
                        self.name, converter.name)

            xml_output = None
            json_output = None
            logger.info('Converting XML to JSON...')
            try:
                json_output = converter.module.xml_to_json(xmldata)
            except Exception:
                passed = None
                logger.debug('Error occured during xml-to-json conversion',
                             exc_info=True)
            else:
                logger.info('Checking resulting JSON data...')
                json_data, json_errors = demjson.decode(
                        json_output,
                        strict=True,
                        return_errors=True,
                        return_stats=False,
                        write_errors=False,
                        forbid_bom=True,
                        allow_zero_byte=True,
                        allow_non_portable=True,
                    )[:2]
                if json_errors:
                    passed = False
                    logger.info('Erroneous JSON: %r', json_errors)
                else:
                    json_input = demjson.encode(json_data, strict=True,
                                                encoding='utf-8',
                                                sort_keys=demjson.SORT_SMART)
                    logger.info('Converting JSON back to XML...')
                    try:
                        xml_output = converter.module.json_to_xml(json_input)
                    except Exception:
                        passed = None
                        logger.debug('Error occured during json-to-xml ' +
                                     'conversion', exc_info=True)
                    else:
                        logger.info('Canonicalizing XML...')
                        try:
                            xmloutput_c14n = canonicalize(xml_output,
                                                          **self.c14n_kwargs)
                        except Exception:
                            logger.warning(
                                    'Failed to canonicalize xml!',
                                    exc_info=logger.isEnabledFor(
                                        logging.DEBUG))
                            passed = False
                        else:
                            passed = (xmldata_c14n == xmloutput_c14n)
            yield TestResult(
                test=self,
                converter=converter,
                test_passed=passed,
                json_output=json_output,
                xml_output=xml_output,
            )
            logger.info('Finished testcase \'%s\' for converter \'%s\'',
                        self.name, converter.name)

    def test_all_converters(self, converters):
        return list(self.test_converters(converters))


class SecurityTestCase(ConversionTestCase):
    def __init__(self, *args):
        super().__init__(*args)
        self.files = dict(parse_files(self._cp, path=self.path))
        self.responses = dict(parse_responses(self._cp, path=self.path))

    @contextlib.contextmanager
    def create_context(self, host='localhost', port=0, requestlog=None,
                       references={}):
        refs = references.copy()

        with tempfile.TemporaryDirectory(prefix='xjcc') as tmpdir:
            # Create references
            files = {}
            for fileref, content in self.files.items():
                absolute_path = os.path.abspath(os.path.join(tmpdir, fileref))
                files[fileref] = FilePath(absolute_path)

            refs['files'] = collections.namedtuple('FileList', files.keys())(
                *files.values()
            )

            # Create "remote" files
            with httpserver.run((host, port), requestlog=requestlog) as server:
                host, port = server.server_address
                netloc = '%s:%d' % (host, port) if port != 80 else host
                refs.update({
                    'server_address': netloc,
                    'server_host': host,
                    'server_port': port,
                })

                for path, r in self.responses.items():
                    data = r.content.format_map(refs).encode('utf-8')
                    server.add_path(path, status=r.status, content=data,
                                    log_request=r.log_request)

                # Create "local" files
                for fileref, content in self.files.items():
                    filename = files[fileref]
                    filepath = os.path.join(tmpdir, filename)
                    with open(filepath, mode='w+', encoding='utf-8') as f:
                        f.write(content.format_map(refs))

                yield self.content.format_map(refs).encode('utf-8')

    def test_converters(self, converters):
        logger = logging.getLogger(__name__)

        log = httpserver.RequestLog()
        ctx = multiprocessing.get_context('spawn')
        refs = {
            'magic_fsa_string': MAGIC_FSA_STRING,
        }
        with self.create_context(requestlog=log, references=refs) as xmldata:
            for converter in converters:
                logger.info('Started testcase \'%s\' for converter \'%s\'',
                            self.name, converter.name)
                log.clear()

                convert = functools.partial(get_conversion_data, xmldata,
                                            converter.module)
                logger.info('Running in separate process...')
                exitcode, retval = process.execute(convert, ctx=ctx)
                json_output, xml_output = retval if retval else (None, None)
                if exitcode < 0:
                    # Process killed by signal
                    sig = signal.Signals(-exitcode)
                    logger.info('Process terminated, caught signal %r!', sig)
                    passed = False
                else:
                    logger.info('Process terminated with exit code %d!',
                                exitcode)
                    passed = True

                requests = log.get_requests()
                logger.info('Converter made %d HTTP requests', len(requests))

                if len(requests) > 0:
                    logger.debug('Requests were: %r', requests)
                    passed = False

                logger.debug('Checking if MAGIC_FSA_STRING is part ' +
                             'of output...')
                searchstr = MAGIC_FSA_STRING.encode('utf-8')
                if json_output and searchstr in json_output:
                    logger.info('MAGIC_FSA_STRING is part of JSON output!')
                    passed = False
                if xml_output and searchstr in xml_output:
                    logger.info('MAGIC_FSA_STRING is part of XML output!')
                    passed = False

                if passed:
                    logger.info('Converter \'%s\' passed testcase \'%s\'!',
                                converter.name, self.name)
                else:
                    logger.info('Converter \'%s\' failed testcase \'%s\'!',
                                converter.name, self.name)

                yield TestResult(
                    test=self,
                    converter=converter,
                    test_passed=passed,
                    json_output=json_output,
                    xml_output=xml_output,
                )
                logger.info('Finished testcase \'%s\' for converter \'%s\'',
                            self.name, converter.name)


CATEGORIES = {
    'basic': ConversionTestCase,
    'charsupport': ConversionTestCase,
    'complex': ConversionTestCase,
    'denial-of-service': SecurityTestCase,
    'file-system-access': SecurityTestCase,
    'server-side-request-forgery': SecurityTestCase,
}
