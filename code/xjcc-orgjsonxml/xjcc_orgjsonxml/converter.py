# -*- coding: utf-8 -*-
import xjcc.plugins


class OrgJsonXMLPlugin(xjcc.plugins.ConverterPlugin):
    """
    This provides static methods to convert an XML text into a JSONObject, and to covert a JSONObject into an XML text.
    http://www.docjar.com/docs/api/org/json/XML.html
    """
    JAR_PATH = 'orgjsonxml/target/orgjsonxml.jar'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.java_app = self.get_package_filename(self.JAR_PATH)

    def xml_to_json(self, xml_data):
        cmd = ['java', '-jar', self.java_app]
        return self.run_command(cmd, xml_data)

    def json_to_xml(self, json_data):
        cmd = ['java', '-jar', self.java_app, '--decode']
        return self.run_command(cmd, json_data)
