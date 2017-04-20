# -*- coding: utf-8 -*-
import contextlib
import logging
import queue
import threading
import http.server


class RequestLoggerHTTPServer(http.server.HTTPServer):
    def __init__(self, server_address):
        super().__init__(server_address, RequestLoggerHTTPRequestHandler)
        self._request_log = queue.Queue()
        self._logger = logging.getLogger(__name__)

    def put_request(self, request):
        self._logger.debug('Logging request %r', request)
        self._request_log.put_nowait(request)

    def get_requests(self):
        items = []
        while True:
            try:
                item = self._request_log.get_nowait()
            except queue.Empty:
                break
            else:
                items.append(item)
        self._logger.debug('Logged %d requests', len(items))
        return items


class RequestLoggerHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        return self.do_all()

    def do_POST(self):
        return self.do_all()

    def do_HEAD(self):
        return self.do_all(output=False)

    def do_all(self, output=True):
        self.server.put_request(self.requestline)
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        if output:
            message = 'You are a nasty little script... Shame on you!'
            self.wfile.write(message.encode('utf-8'))


@contextlib.contextmanager
def run(server_address):
    logger = logging.getLogger(__name__)
    with RequestLoggerHTTPServer(server_address) as httpd:
        try:
            t = threading.Thread(target=httpd.serve_forever, daemon=True)
            t.start()
            logger.debug('Started HTTP server on %s:%d...', *server_address)
            yield httpd
        finally:
            httpd.shutdown()
            logger.debug('HTTP server on %s:%d shut down.', *server_address)
