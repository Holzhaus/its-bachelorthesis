# -*- coding: utf-8 -*-
import resource
import xjcc.plugins


def get_limit():
    limits = [limit for limit in resource.getrlimit(resource.RLIMIT_AS)
              if limit != resource.RLIM_INFINITY]
    if limits:
        return min(limits)


class OrgJsonXMLPlugin(xjcc.plugins.ConverterPlugin):
    """
    This provides static methods to convert an XML text into a JSONObject, and to covert a JSONObject into an XML text.
    http://www.docjar.com/docs/api/org/json/XML.html
    """
    JAR_PATH = 'orgjsonxml/target/orgjsonxml.jar'

    # Looks like java hates being in a restricted environment. It will fail
    # with this error message when vmem is restricted.
    #     Error occurred during initialization of VM
    #     Could not allocate metaspace: 1073741824 bytes
    #
    # See this bug report: http://bugs.java.com/view_bug.do?bug_id=8043516
    # We need to set a bunch args to make it work, but hey, the JAVA devs
    # closed it as WONTFIX. Whatever.

    JAVA_ARGS = [
        '-Xms50m',
        '-Xmx50m',
        '-XX:MaxHeapSize=50m',
        '-XX:CompressedClassSpaceSize=10m',
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.java_app = self.get_package_filename(self.JAR_PATH)

    def xml_to_json(self, xml_data):
        cmd = ['java']
        if get_limit():
            cmd.extend(self.JAVA_ARGS)
        cmd.extend(['-jar', self.java_app])
        return self.run_command(cmd, xml_data)

    def json_to_xml(self, json_data):
        cmd = ['java']
        if get_limit():
            cmd.extend(self.JAVA_ARGS)
        cmd.extend(['-jar', self.java_app, '--decode'])
        return self.run_command(cmd, json_data)
