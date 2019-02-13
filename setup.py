#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = "csvtofhir",
    version = "0.1",
    #packages = find_packages(),

    packages = ['csvtofhir'],
    package_data = {},
    entry_points={
          'console_scripts':['csvtofhir = csvtofhir.main:cli'
          ]
      },

    description = 'Code for converting radiotherapy data to fhir resources',
    license = 'BSD License',

    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: Free for Educational Use',
        'Operating System :: OS Independent',
        'Programming Language :: Python 3.6',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
    ],

    keywords = 'fhir radiotherapy oncology csv',
)