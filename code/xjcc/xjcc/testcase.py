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


def canonicalize(xmldata):
    element = defusedxml.lxml.XML(xmldata)
    tree = element.getroottree()
    output = io.BytesIO()
    tree.write_c14n(output)
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
        content_type = cp[section].get('content', None)
        if content_type is not None:
            headers = {'Content-Type': content_type}

        yield (url_path, httpserver.PathInfo(content=content, status=status,
                                             headers=headers))


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
    def __init__(self, info_file):
        self._cp = configparser.ConfigParser()
        with open(info_file) as f:
            self._cp.readfp(f)

        general = self._cp['General']
        self.name = general.get('name')
        self.description = general.get('description', '')

        self.path = os.path.dirname(os.path.abspath(info_file))
        raw_name = os.path.splitext(info_file)[0]
        default_filename = os.extsep.join([raw_name, 'xml'])
        self.filename = general.get('filename', default_filename)
        self.filename = os.path.join(self.path, self.filename)
        self.basename = os.path.basename(raw_name)
        with open(self.filename) as f:
            self.content = f.read()

    def test_converters(self, converters):
        logger = logging.getLogger(__name__)

        xmldata = self.content.encode('utf-8')
        convert = functools.partial(get_conversion_data, xmldata)
        for converter in converters:
            try:
                json_output, xml_output = convert(converter.module)
            except Exception:
                passed = None
                json_output = None
                xml_output = None
                logger.debug('Error occured during conversion', exc_info=True)
            else:
                json_errors = demjson.decode(
                        json_output, strict=True, return_errors=True,
                        return_stats=False, write_errors=False)[1]
                if json_errors:
                    passed = False
                    logger.info('Erroneous JSON: %r', json_errors)
                else:
                    xmldata_c14n = canonicalize(xmldata)
                    xmloutput_c14n = canonicalize(xml_output)
                    passed = (xmldata_c14n == xmloutput_c14n)
            yield TestResult(
                test=self,
                converter=converter,
                test_passed=passed,
                json_output=json_output,
                xml_output=xml_output,
            )

    def test_all_converters(self, converters):
        return list(self.test_converters(converters))


class SecurityTestCase(ConversionTestCase):
    def __init__(self, *args):
        super().__init__(*args)
        self.files = dict(parse_files(self._cp, path=self.path))
        self.responses = dict(parse_responses(self._cp, path=self.path))

    @contextlib.contextmanager
    def create_context(self, host='localhost', port=0, requestlog=None):
        refs = {
            'magic_fsa_string': 'THIS_IS_TOP_SECRET_STUFF',
        }

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
                    server.add_path(path, status=r.status, content=data)

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
        with self.create_context(requestlog=log) as xmldata:
            for converter in converters:
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

                requests = log.get_requests()
                passed = (len(requests) == 0)
                yield TestResult(
                    test=self,
                    converter=converter,
                    test_passed=passed,
                    json_output=json_output,
                    xml_output=xml_output,
                )


CATEGORIES = {
    'conversion': ConversionTestCase,
    'denial-of-service': SecurityTestCase,
    'file-system-access': SecurityTestCase,
    'server-side-request-forgery': SecurityTestCase,
}
