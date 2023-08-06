# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quack_cli']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0', 'typer[all]>=0.4,<0.5']

entry_points = \
{'console_scripts': ['quack = quack_cli.main:app']}

setup_kwargs = {
    'name': 'quack-cli',
    'version': '0.2.1',
    'description': 'A CLI for the Quackstack API',
    'long_description': '# Quack CLI\n\nA simple CLI for interacting with Quackstack.\n\n## Usage\n\n```sh\nquack --help\n```',
    'author': 'Kronifer',
    'author_email': '44979306+Kronifer@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
