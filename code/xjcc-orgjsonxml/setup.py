#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import distutils
import os
import setuptools
import setuptools.command.build_py
import subprocess


class BuildJarCommand(setuptools.Command):
    description = 'Build JAR file using maven'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        self.finalized = True
        pass

    def run(self):
        cmd = ['mvn', 'package']
        oldroot = os.getcwd()
        buildroot = os.path.join(os.path.dirname(__file__),
                                 'xjcc_orgjsonxml', 'orgjsonxml')

        infiles = [
            os.path.join(buildroot, filename)
            for filename in [
                'pom.xml',
                'src/main/java/de/rub/xjcc/orgjsonxml/App.java',
                'src/test/java/de/rub/xjcc/orgjsonxml/AppTest.java',
            ]
        ]
        outfile = os.path.join(buildroot, 'target/orgjsonxml.jar')
        self.announce('packaging jar file using maven',
                      level=distutils.log.INFO)
        self.make_file(infiles, outfile, self.run_maven, [
            cmd,
            buildroot,
            oldroot
        ])
        self.announce('jar file is at \'%s\'' % outfile,
                      level=distutils.log.INFO)

    def run_maven(self, cmd, buildroot, oldroot):
        os.chdir(buildroot)
        self.announce('running command %r' % cmd,
                      level=distutils.log.INFO)
        try:
            subprocess.call(cmd)
        finally:
            os.chdir(oldroot)


class BuildPyCommand(setuptools.command.build_py.build_py):
    def run(self):
        self.run_command('build_jar'),
        super().run()


setuptools.setup(
    name='xjcc_orgjsonxml',
    version='0.1.0',
    description='JSON-lib converter for xjcc',
    author='Jan Holthuis',
    author_email='jan.holthuis@ruhr-uni-bochum.de',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='xml json jxon conversion translation algorithm lossless security',
    packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests']),
    include_package_data=True,
    package_data={
        'xjcc_orgjsonxml': ['orgjsonxml/target/orgjsonxml.jar'],
    },
    entry_points={
        'xjcc.converters': [
            'orgjsonxml = xjcc_orgjsonxml:OrgJsonXMLPlugin',
        ],
    },
    cmdclass={
        'build_jar': BuildJarCommand,
        'build_py': BuildPyCommand,
    },
)
