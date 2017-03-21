#!/usr/bin/env python3
import contextlib
import io
import unittest
import unittest.mock
from .. import cli


class TestCli(unittest.TestCase):
    @unittest.mock.patch.object(cli.plugins, 'get_converters')
    def test_list_converters(self, gc_func):
        gc_func.return_value = []
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            cli.list_converters(None)
            self.assertEqual(stdout.getvalue(), 'No converters available.\n')

        m = unittest.mock.Mock()
        m.name = 'foo'
        m.desc = 'bar'
        gc_func.return_value = [m]
        with unittest.mock.patch('builtins.print') as p_func:
            cli.list_converters(None)
            p_func.assert_called()

    @unittest.mock.patch.object(cli.check, 'get_testdocs')
    def test_list_checks(self, gt_func):
        gt_func.return_value = []
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            cli.list_checks(None)
            self.assertEqual(stdout.getvalue(), 'No checks available.\n')

        m = unittest.mock.Mock()
        m.name = 'foo'
        gt_func.return_value = [m]
        with unittest.mock.patch('builtins.print') as p_func:
            cli.list_checks(None)
            p_func.assert_called()

    @unittest.mock.patch.object(cli.check, 'canonicalize')
    def test_canonicalize(self, c14n_func):
        c14n_func.side_effect = lambda x: x
        xml_data = b'<x></x>'
        mocked_args = unittest.mock.Mock(file=io.BytesIO(xml_data))
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            cli.canonicalize(mocked_args)
            self.assertEqual(stdout.getvalue().strip().encode(), xml_data)
