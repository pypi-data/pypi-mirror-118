# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mr_cli']

package_data = \
{'': ['*']}

install_requires = \
['rich>=10.8.0,<11.0.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['mr = mr_cli.__main__:main']}

setup_kwargs = {
    'name': 'mr-cli',
    'version': '0.0.3',
    'description': '',
    'long_description': None,
    'author': 'GreyElaina',
    'author_email': 'GreyElaina@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
