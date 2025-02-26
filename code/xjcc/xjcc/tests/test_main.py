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

    def test_list_testcases(self):
        self.command_test('list-testcases')

    def test_check_conversion(self):
        args = self.command_test('test-conversion', 'myconv')
        self.assertEqual(args.name, 'myconv')

    def test_canonicalize(self):
        args = self.command_test('canonicalize', '-')
        self.assertIs(args.file, sys.stdin)


class TestMain(unittest.TestCase):
    @unittest.mock.patch.object(main, 'parse_args')
    def test_main(self, pa_func):
        mocked_loglevel = 123
        mocked_retval = 2
        mocked_args = ['foo']
        mocked_pargs = unittest.mock.Mock()
        mocked_pargs.loglevel = mocked_loglevel
        mocked_pargs.func.return_value = mocked_retval
        pa_func.return_value = mocked_pargs

        retval = main.main(args=mocked_args)
        pa_func.assert_called_once_with(mocked_args)
        mocked_pargs.func.assert_called_once_with(mocked_pargs)
        self.assertEqual(retval, mocked_retval)
