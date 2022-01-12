#!/usr/bin/env python
import re
from setuptools import setup, find_packages


def find_version():
    with open('./janus/__init__.py', 'r') as f:
        for line in f:
            line = line.strip()
            match = re.search(r'^VERSION *= *.(\d+\.\d+\.\d+).$', line)
            if match:
                return match.group(1)


def find_install_requires(requires_list):
    with open('./requirements.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            requires_list.append(line)


VERSION = find_version()
assert VERSION


INSTALL_REQUIRES = []
find_install_requires(INSTALL_REQUIRES)


setup(name='Janus',
      version=VERSION,
      url='https://github.com/usharerose/janus.git',
      install_requires=INSTALL_REQUIRES,
      packages=['janus'],
      package_data={'janus': ['*.so']},
      entry_points={'console_scripts': ['janus=janus.cli:main']})
