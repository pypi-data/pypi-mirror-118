# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['phae', 'phae.discord']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'phae',
    'version': '0.0.3',
    'description': 'A framework for developing chatbots',
    'long_description': None,
    'author': 'pyxiis',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
