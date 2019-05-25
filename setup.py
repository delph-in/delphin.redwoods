#!/usr/bin/env python3

import os
from setuptools import setup

base_dir = os.path.dirname(__file__)
with open(os.path.join(base_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='delphin.redwoods',
    version='0.1.0',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/delph-in/delphin.redwoods',
    author='',
    author_email='',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Utilities'
    ],
    keywords='nlp semantics hpsg delph-in linguistics',
    packages=[
    ],
    install_requires=[
        'pydelphin >= 1.0.0',
        'svn >= 0.3.46 ',
    ],
    extras_require={
    },
    entry_points={
    },
)
