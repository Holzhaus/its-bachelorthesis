#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import setuptools

setuptools.setup(
    name='xjcc_xmljson',
    version='0.1.0',
    description='xmljson converter for xjcc',
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
    entry_points={
        'xjcc.converters': [
            'xmljson-badgerfish = xjcc_xmljson:XmlJsonBadgerfishPlugin',
            'xmljson-gdata = xjcc_xmljson:XmlJsonGDataPlugin',
            'xmljson-yahoo = xjcc_xmljson:XmlJsonYahooPlugin',
            'xmljson-parker = xjcc_xmljson:XmlJsonParkerPlugin',
        ],
    },
    install_requires=[
        'xmljson>=0.1.7',
    ]
)
