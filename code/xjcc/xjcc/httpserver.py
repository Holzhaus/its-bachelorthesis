# -*- coding: utf-8 -*-
import collections
import contextlib
import logging
import queue
import threading
import http.server

PathInfo = collections.namedtuple('PathInfo', 'content status headers')


def first(iterable, default=None):
    return next((el for el in iterable if el is not None), None)


class RequestLog(queue.Queue):
    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(__name__)

    def clear(self):
        with self.mutex:
            self.queue.clear()
        self._logger.debug('RequestLog cleared')

    def put_request(self, request):
        self._logger.debug('Logging request %r', request)
        self.put_nowait(request)

    def get_requests(self):
        items = []
        while True:
            try:
                item = self.get_nowait()
            except queue.Empty:
                break
            else:
                items.append(item)
        self._logger.debug('Logged %d requests', len(items))
        return items


class HTTPServer(http.server.HTTPServer):
    def __init__(self, server_address, default_status=200,
                 default_headers={'Content-Type': 'text/plain'},
                 default_content=b'It\'s a TRAP!',
                 requestlog=None):
        super().__init__(server_address, HTTPRequestHandler)

        self.default_status = default_status
        self.default_headers = default_headers
        self.default_content = default_content

        self._requestlog = requestlog
        self._logger = logging.getLogger(__name__)
        self.paths = {}

    def add_path(self, path, content, status=None, headers=None):
        self.paths[path] = PathInfo(content, status, headers)


class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        return self.do_all()

    def do_POST(self):
        return self.do_all()

    def do_HEAD(self):
        return self.do_all(output=False)

    def do_all(self, output=True):
        if self.server.requestlog is not None:
            self.server.requestlog.put_request(self.requestline)

        pathinfo = self.server.paths.get(self.path, PathInfo(None, None, None))
        self.send_response(first(pathinfo.status, self.server.default_status))

        headers = first(pathinfo.headers, self.server.default_headers)
        for item in headers.items():
            self.send_header(*item)
        self.end_headers()

        if output:
            message = first(pathinfo.content, self.server.default_content)
            self.wfile.write(message)


@contextlib.contextmanager
def run(server_address, *args, **kwargs):
    logger = logging.getLogger(__name__)
    with HTTPServer(server_address, *args, **kwargs) as httpd:
        try:
            t = threading.Thread(target=httpd.serve_forever, daemon=True)
            t.start()
            logger.debug('Started HTTP server on %s:%d...',
                         *httpd.server_address)
            yield httpd
        finally:
            httpd.shutdown()
            logger.debug('HTTP server on %s:%d shut down.',
                         *httpd.server_address)
