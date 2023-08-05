# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['phae', 'phae.discord']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'phae',
    'version': '0.0.1',
    'description': 'A Python library for the Phae project',
    'long_description': None,
    'author': 'pyxiis',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
