# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_needs_extensions']

package_data = \
{'': ['*']}

install_requires = \
['sphinxcontrib-needs>=0.7,<0.8']

setup_kwargs = {
    'name': 'sphinx-needs-extensions',
    'version': '0.1.0',
    'description': 'Core package to provide core functionalities to all Sphinx-Needs extensions',
    'long_description': None,
    'author': 'team useblocks',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
