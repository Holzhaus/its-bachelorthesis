# -*- coding: utf-8 -*-
import io
import os
import types
import unittest
import unittest.mock
from .. import testing

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
    def test_get_tests(self, rs_func, rl_func):
        mocked_names = ['doc1.xml', 'doc2.xml']
        mocked_xml_data = b'<root>test</root>'
        rl_func.return_value = mocked_names
        rs_func.side_effect = lambda *x: io.BytesIO(mocked_xml_data)
        ret = testing.get_tests()
        self.assertIsInstance(ret, types.GeneratorType)
        docs = list(ret)
        self.assertEqual(len(docs), len(mocked_names))
        for i, doc in enumerate(docs):
            self.assertIsInstance(doc, testing.TestCase)
            self.assertEqual(os.path.splitext(mocked_names[i])[0], doc.name)
            self.assertEqual(mocked_xml_data, doc.xml_data)

    def test_canonicalize(self):
        self.assertEqual(testing.canonicalize(c14n_input), c14n_output)
