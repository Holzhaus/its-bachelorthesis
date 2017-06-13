# -*- coding: utf-8 -*-
import xjcc.plugins


class CobraVsMongoosePlugin(xjcc.plugins.ConverterPlugin):
    """
    Translates XML to and from Ruby Hash objects, following the BadgerFish convention.
    https://rubygems.org/gems/cobravsmongoose
    """
    RB_PATH = 'converter.rb'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ruby_app = self.get_package_filename(self.RB_PATH)

    def xml_to_json(self, xml_data):
        cmd = ['ruby', self.ruby_app]
        return self.run_command(cmd, xml_data)

    def json_to_xml(self, json_data):
        cmd = ['ruby', self.ruby_app, '--decode']
        return self.run_command(cmd, json_data)
