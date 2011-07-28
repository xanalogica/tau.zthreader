#############################################################################
#
# Copyright (c) 2011 Tau Productions Inc.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
"""

EGGNAME = 'tau.zthreader'
EGGVERS = '1.0'

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))  # the directory containing this setup.py file

setup(
    # Basic Identification of Distribution
    name=EGGNAME,
    version=EGGVERS,

    # Descriptions for Potential Users of Distribution
    description="A BTree based implementation for Zope 2's OFS.",
    long_description=(
        open('README.txt').read()
        + '\n' + '-'*60 + '\n\n' +
        "Download\n========"
    ),

    # Contact and Ownership Info
    author = 'Jeff Rush',
    author_email="jeff@taupro.com",
    url="http://www.zeomega.com/",
    license='ZPL 2.1',

    # Egg Classification Info
    classifiers=[ # python setup.py register --list-classifiers
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Zope2",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: Zope Public License',
        "Natural Language :: English",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Python :: 2.6",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    keywords='web application server zope zope2 threading',

    # Location of Stuff Within Distribution
    packages=find_packages('src'),
    namespace_packages=['tau'],
    include_package_data=True,
    zip_safe=False,
    package_dir={
        '': 'src',
    },

    # Dependencies on Other Eggs
    install_requires=[
        'setuptools',
        'Zope2 >= 2.12.1',
        'z3c.autoinclude',  # for automatic-slugs-generation of my dependencies
    ],
)
