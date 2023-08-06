# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['portfolio_analyzer']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'scipy>=1.7.1,<2.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'yfinance>=0.1.63,<0.2.0']

entry_points = \
{'console_scripts': ['portfolio = portfolio_analyzer.cli:main']}

setup_kwargs = {
    'name': 'portfolio-analyzer',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Tapan Pandita',
    'author_email': 'tapan.pandita@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
