# -*- coding: utf-8 -*-
import collections
import tempfile
import urllib.request
import unittest
import unittest.mock
from .. import testcase

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

DummyConverter = collections.namedtuple('DummyConverter', 'name module')
dummyconv = DummyConverter('dummy', None)

dummytc = b"""<?xml version="1.0"?>
<!--;testcase
[General]
name: Dummy Testcase
-->
ADDR:{server_address}
STR:{magic_fsa_string}"""


class TestTestcase(unittest.TestCase):
    def test_canonicalize(self):
        self.assertEqual(testcase.canonicalize(c14n_input), c14n_output)

    @unittest.mock.patch('%s.process.execute' % testcase.__name__)
    def test_fsa(self, exc_func):
        with tempfile.NamedTemporaryFile() as f:
            f.write(dummytc)
            f.flush()
            tc = testcase.SecurityTestCase(f.name)

        def custom_exc_func_json(partialfunc, ctx):
            xmldata = partialfunc.args[0]
            return 0, (xmldata, xmldata)

        exc_func.side_effect = custom_exc_func_json
        result = next(tc.test_converters([dummyconv]))
        self.assertIs(result.test_passed, False)

        def custom_exc_func_xml(partialfunc, ctx):
            xmldata = partialfunc.args[0]
            return 0, (xmldata, xmldata)

        exc_func.side_effect = custom_exc_func_xml
        result = next(tc.test_converters([dummyconv]))
        self.assertIs(result.test_passed, False)

    @unittest.mock.patch('%s.process.execute' % testcase.__name__)
    def test_ssrf(self, exc_func):
        with tempfile.NamedTemporaryFile() as f:
            f.write(dummytc)
            f.flush()
            tc = testcase.SecurityTestCase(f.name)

        def custom_exc_func(partialfunc, ctx):
            xmldata = partialfunc.args[0]
            for line in xmldata.decode().splitlines():
                if ':' in line:
                    name, d, value = line.partition(':')
                    if name == 'ADDR':
                        break
            else:
                raise RuntimeError

            url = 'http://%s/file.txt' % value
            try:
                r = urllib.request.urlopen(url)
            except Exception:
                pass

            return 0, (b'x', b'x')

        exc_func.side_effect = custom_exc_func
        result = next(tc.test_converters([dummyconv]))
        self.assertIs(result.test_passed, False)
