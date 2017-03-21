#!/usr/bin/env python3
import unittest
import unittest.mock
import sys
from .. import main


class TestArgParse(unittest.TestCase):
    def command_test(self, command, *args):
        args = main.parse_args(args=[command, *args])
        self.assertEqual(args.command, command)
        return args

    def test_list_converters(self):
        self.command_test('list-converters')

    def test_list_checks(self):
        self.command_test('list-checks')

    def test_check_conversion(self):
        args = self.command_test('check-conversion', 'myconv')
        self.assertEqual(args.name, 'myconv')

    def test_canonicalize(self):
        args = self.command_test('canonicalize', '-')
        self.assertIs(args.file, sys.stdin)


class TestMain(unittest.TestCase):
    @unittest.mock.patch.object(main, 'parse_args')
    @unittest.mock.patch('logging.basicConfig')
    def test_main(self, bc_func, pa_func):
        mocked_loglevel = 123
        mocked_retval = 2
        mocked_args = ['foo']
        mocked_pargs = unittest.mock.Mock()
        mocked_pargs.loglevel = mocked_loglevel
        mocked_pargs.func.return_value = mocked_retval
        bc_func.return_value = None
        pa_func.return_value = mocked_pargs

        retval = main.main(args=mocked_args)
        pa_func.assert_called_once_with(mocked_args)
        bc_func.assert_called_once_with(level=mocked_loglevel)
        mocked_pargs.func.assert_called_once_with(mocked_pargs)
        self.assertEqual(retval, mocked_retval)
