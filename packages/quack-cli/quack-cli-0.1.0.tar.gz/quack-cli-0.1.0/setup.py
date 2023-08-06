# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quack_cli']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0', 'typer>=0.4,<0.5']

setup_kwargs = {
    'name': 'quack-cli',
    'version': '0.1.0',
    'description': 'A CLI for the Quackstack API',
    'long_description': None,
    'author': 'Kronifer',
    'author_email': '44979306+Kronifer@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
