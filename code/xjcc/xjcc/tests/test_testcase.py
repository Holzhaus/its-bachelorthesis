# -*- coding: utf-8 -*-
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


class TestTestcase(unittest.TestCase):
    def test_canonicalize(self):
        self.assertEqual(testcase.canonicalize(c14n_input), c14n_output)
