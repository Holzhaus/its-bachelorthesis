# -*- coding: utf-8 -*-
import unittest
import unittest.mock
from .. import plugins


class TestPlugins(unittest.TestCase):
    @unittest.mock.patch('pkg_resources.iter_entry_points')
    @unittest.mock.patch.object(plugins, 'parse_docstring')
    def test_get_converters(self, pd_func, iep_func):
        mocked_desc = 'mydesc'
        mocked_name = 'myname'
        mocked_ep = unittest.mock.Mock()
        mocked_ep.name = mocked_name
        mocked_ep.load = unittest.mock.Mock()
        iep_func.return_value = [mocked_ep]
        pd_func.return_value = [mocked_desc, {}]
        retval = next(plugins.get_converters())
        iep_func.assert_called_once_with('xjcc.converters', name=None)
        self.assertIs(retval.entrypoint, mocked_ep)
        mocked_ep.load.assert_called_once()
        self.assertEqual(retval.name, mocked_name)
        self.assertEqual(retval.desc, mocked_desc)
        self.assertIsInstance(retval.meta, dict)

    @unittest.mock.patch.object(plugins, 'get_converters')
    def test_get_converter(self, gc_func):
        gc_func.iter.return_value = iter([])
        name = 'myconv'
        self.assertIsNone(plugins.get_converter(name))

        mock1 = unittest.mock.Mock()
        mock2 = unittest.mock.Mock()
        mock3 = unittest.mock.Mock()
        gc_func.return_value = iter([mock1, mock2, mock3])
        self.assertIs(plugins.get_converter(name), mock1)

    def test_parse_docstring(self):
        docstring1 = """
        Some text.
        Some more text.

        Some Key 1 = Some Value 1
        Some Key 2 = Some Value 2
        """
        desc, meta = plugins.parse_docstring(docstring1)

        self.assertEqual(desc, 'Some text.\nSome more text.')
        self.assertDictEqual(meta, {
            'Some Key 1': 'Some Value 1',
            'Some Key 2': 'Some Value 2',
        })

        docstring2 = """
        Some text.
        """
        desc, meta = plugins.parse_docstring(docstring2)

        self.assertEqual(desc, 'Some text.')
        self.assertDictEqual(meta, {})
