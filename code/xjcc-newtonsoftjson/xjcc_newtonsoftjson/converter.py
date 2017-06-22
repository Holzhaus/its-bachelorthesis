# -*- coding: utf-8 -*-
import xjcc.plugins


class NewtonsoftJsonPlugin(xjcc.plugins.ConverterPlugin):
    """
    Json.NET is a popular high-performance JSON framework for .NET
    http://www.newtonsoft.com/json
    """
    EXE_PATH = 'converter.exe'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mono_app = self.get_package_filename(self.EXE_PATH)

    def xml_to_json(self, xml_data):
        cmd = ['mono', self.mono_app]
        return self.run_command(cmd, xml_data)

    def json_to_xml(self, json_data):
        cmd = ['mono', self.mono_app, '--decode']
        return self.run_command(cmd, json_data)
