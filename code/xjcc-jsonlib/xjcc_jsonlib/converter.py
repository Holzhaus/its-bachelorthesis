# -*- coding: utf-8 -*-
import xjcc.plugins


class JsonlibPlugin(xjcc.plugins.ConverterPlugin):
    """
    JSON-lib is a java library for transforming beans, maps, collections, java
    arrays and XML to JSON and back again to beans and DynaBeans.
    http://json-lib.sourceforge.net/
    """
    JAR_PATH = 'jsonlib/target/jsonlib.jar'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.java_app = self.get_package_filename(self.JAR_PATH)

    def xml_to_json(self, xml_data):
        cmd = ['java', '-jar', self.java_app]
        return self.run_command(cmd, xml_data)

    def json_to_xml(self, json_data):
        cmd = ['java', '-jar', self.java_app, '--decode']
        return self.run_command(cmd, json_data)
