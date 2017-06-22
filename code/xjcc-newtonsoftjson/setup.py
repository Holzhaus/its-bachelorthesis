#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import distutils
import os
import setuptools
import setuptools.command.build_py
import subprocess


class BuildExeCommand(setuptools.Command):
    description = 'Build EXE file using mcs'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        self.finalized = True
        pass

    def run(self):
        cmd = ['mcs', '-lib:/usr/lib/mono/NewtonsoftJson',
               '-r:Newtonsoft.Json.dll', 'converter.cs']
        oldroot = os.getcwd()
        buildroot = os.path.join(os.path.dirname(__file__),
                                 'xjcc_newtonsoftjson')

        infiles = [os.path.join(buildroot, 'converter.cs')]
        outfile = os.path.join(buildroot, 'converter.exe')
        self.announce('compiling mono exe file using mcs',
                      level=distutils.log.INFO)
        self.make_file(infiles, outfile, self.run_mcs, [
            cmd,
            buildroot,
            oldroot
        ])
        self.announce('exe file is at \'%s\'' % outfile,
                      level=distutils.log.INFO)

    def run_mcs(self, cmd, buildroot, oldroot):
        os.chdir(buildroot)
        self.announce('running command %r' % cmd,
                      level=distutils.log.INFO)
        try:
            subprocess.call(cmd)
        finally:
            os.chdir(oldroot)


class BuildPyCommand(setuptools.command.build_py.build_py):
    def run(self):
        self.run_command('build_exe'),
        super().run()


setuptools.setup(
    name='xjcc_newtonsoftjson',
    version='0.1.0',
    description='Newtonsoft JSON.NET converter for xjcc',
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
        'xjcc_newtonsoftjson': ['converter.exe'],
    },
    entry_points={
        'xjcc.converters': [
            'newtonsoftjson = xjcc_newtonsoftjson:NewtonsoftJsonPlugin',
        ],
    },
    cmdclass={
        'build_exe': BuildExeCommand,
        'build_py': BuildPyCommand,
    },
)
