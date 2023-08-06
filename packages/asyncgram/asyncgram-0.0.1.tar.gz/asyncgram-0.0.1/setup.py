# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['asyncgram']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv', 'requests']

setup_kwargs = {
    'name': 'asyncgram',
    'version': '0.0.1',
    'description': 'A lightweight, asynchronous telegram logging client',
    'long_description': None,
    'author': 'sumermalhotra',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.8',
}


setup(**setup_kwargs)
