#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
if sys.version_info < (3, 11):
    sys.exit("Sorry, amplimap requires at least Python 3.11")

from setuptools import setup, find_packages, Extension

#load version number (can't just import the package since we might miss requirements)
filename = 'amplimap/version.py'
exec(compile(open(filename, "rb").read(), filename, 'exec')) #python2/3 compatible replacement for execfile()

#load long description from readme
import codecs
with codecs.open('README.rst', 'r', 'utf-8') as f:
    long_description = f.read()

setup(
    name = __title__,
    version = __version__,

    packages = find_packages(),
    #these files will be added to the package directory
    package_data={ '': ['parse_reads_cy.pyx', 'Snakefile', 'config_default.yaml'] },

    # metadata for upload to PyPI
    author = "Nils Koelling",
    author_email = "git@nk.gl",
    description = "amplicon/smMIP mapping and analysis pipeline",
    long_description = long_description,
    license = "Apache License, Version 2.0",
    keywords = "amplimap amplicon smmip mapping analysis pipeline",
    url = "https://github.com/koelling/amplimap/",
    download_url="https://github.com/koelling/amplimap/archive/v%s.tar.gz" % __version__,
    platforms=["any"],
    entry_points={
        'console_scripts': [
            'amplimap = amplimap.run:main',
            'amplimap_merge = amplimap.merge_folders:main',
            'amplimap_setup = amplimap.run_setup:main',
            #'amplimap_pileup = amplimap.pileup:main',
        ]
    },

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
    ],

    python_requires='>=3.11',

    install_requires=[
        'snakemake>=8.6,<10',
        'snakemake-executor-plugin-cluster-generic>=1,<2',
        'snakemake-executor-plugin-cluster-sync>=0.1,<1',
        'pyyaml>=6,<7',
        'numpy>=1.26,<2',
        'biopython>=1.84,<2',
        'pandas>=2.1,<3',
        'interlap>=0.2.5',
        'pysam>=0.22,<0.23',
        'pyfaidx>=0.8,<1',
        'distance>=0.1.3',
        'umi_tools>=1.1.5,<2',
    ],

    setup_requires=[
        'setuptools>=18.0',
        'cython',
    ],

    ext_modules = [Extension("amplimap.parse_reads_cy", ["amplimap/parse_reads_cy.pyx"])]
)
