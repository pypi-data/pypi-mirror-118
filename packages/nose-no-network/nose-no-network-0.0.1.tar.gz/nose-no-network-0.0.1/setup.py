#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

with open('nosenonetwork/__init__.py') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name='nose-no-network',
    version=version,
    description='A plugin for nosetests that disables network access',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ross McFarland',
    url='https://github.com/ross/nose-no-network',
    packages=[
        'nosenonetwork',
    ],
    install_requires=[
        'nose',
    ],
    license='MIT',
    entry_points={
        'nose.plugins.0.10': [
            'nosenonetwork = nosenonetwork:NoNetworkPlugin',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
    ],
)
