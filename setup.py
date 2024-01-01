#!/usr/bin/env python3

from os import path
from setuptools import setup, find_packages

__folder__ = path.abspath(path.dirname(__file__))

with open(path.join(__folder__, 'README.md')) as readme_file:
    long_description = readme_file.read()

about = {}
with open(path.join(__folder__, 'requests_raw', '__version__.py')) as about_file:
    exec(about_file.read(), about)

with open(path.join(__folder__, 'requirements.txt')) as req_file:
    install_requires = req_file.readlines()

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__author_email__'],
    packages=find_packages(exclude=['examples', 'tests']),
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    install_requires=install_requires,
    license=about['__license__'],
    platforms='any',
    url='https://github.com/realgam3/requests-raw',
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    extras_require={
        'security': ['pyOpenSSL >= 0.14', 'cryptography>=1.3.4'],
        'socks': ['PySocks>=1.5.6, !=1.5.7'],
        'socks:sys_platform == "win32" and python_version == "2.7"': ['win_inet_pton'],
    },
    project_urls={
        'Source': 'https://github.com/realgam3/requests-raw',
    },
)
