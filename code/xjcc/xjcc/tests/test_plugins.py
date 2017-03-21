# -*- coding: utf-8 -*-
import io
import types
import unittest
import unittest.mock
from .. import check

c14n_input = b"""<?xml version="1.0"?>

<?xml-stylesheet   href="doc.xsl"
   type="text/xsl"   ?>

<!DOCTYPE doc SYSTEM "doc.dtd">

<doc     >Hello, world!<!-- Comment 1 --></doc

>

<?pi-without-data     ?>

<!-- Comment 2 -->

<!-- Comment 3 -->
"""
c14n_output = b"""<?xml-stylesheet href="doc.xsl"
   type="text/xsl"   ?>
<doc>Hello, world!<!-- Comment 1 --></doc>
<?pi-without-data?>
<!-- Comment 2 -->
<!-- Comment 3 -->"""


class TestChecks(unittest.TestCase):
    @unittest.mock.patch('pkg_resources.resource_listdir')
    @unittest.mock.patch('pkg_resources.resource_stream')
    def test_get_testdocs(self, rs_func, rl_func):
        mocked_names = ['doc1', 'doc2']
        mocked_content = b'<root>test</root>'
        rl_func.return_value = mocked_names
        rs_func.side_effect = lambda *x: io.BytesIO(mocked_content)
        ret = check.get_testdocs()
        self.assertIsInstance(ret, types.GeneratorType)
        docs = list(ret)
        self.assertEqual(len(docs), len(mocked_names))
        for i, doc in enumerate(docs):
            self.assertIsInstance(doc, check.TestDocument)
            self.assertEqual(mocked_names[i], doc.name)
            self.assertEqual(mocked_content, doc.content)

    def test_canonicalize(self):
        self.assertEqual(check.canonicalize(c14n_input), c14n_output)

    @unittest.mock.patch.object(check, 'canonicalize')
    def test_check_conversion(self, c14n_func):
        json_data = b'{"x": ""}'
        xml_data = b'<x  ></x>'
        c14n_xml_data = b'<x></x>'
        converter = unittest.mock.Mock()
        converter.xml_to_json.return_value = json_data
        converter.json_to_xml.return_value = xml_data
        c14n_func.return_value = c14n_xml_data

        result = check.check_conversion(converter, xml_data)
        converter.xml_to_json.assert_called_once_with(xml_data)
        converter.json_to_xml.assert_called_once_with(json_data)
        c14n_func.assert_called_with(xml_data)
        self.assertTrue(result)
