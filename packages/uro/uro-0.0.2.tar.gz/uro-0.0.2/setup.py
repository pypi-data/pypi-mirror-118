#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
from setuptools import setup, find_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))
with io.open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    desc = f.read()

setup(
    name='uro',
    version=__import__('uro').__version__,
    description='declutters url lists',
    long_description=desc,
    long_description_content_type='text/markdown',
    author='Somdev Sangwan',
    author_email='s0md3v@gmail.com',
    license='Apache-2.0 License',
    url='https://github.com/s0md3v/uro',
    download_url='https://github.com/s0md3v/uro/archive/v%s.zip' % __import__('uro').__version__,
    zip_safe=False,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Operating System :: OS Independent',
        'Topic :: Security',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.4',
    ],
    entry_points = {'console_scripts': ['uro=uro.uro:main']},
    keywords=['crawling', 'fuzzing']
)
