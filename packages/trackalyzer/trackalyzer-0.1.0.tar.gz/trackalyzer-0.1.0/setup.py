# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trackalyzer']

package_data = \
{'': ['*']}

install_requires = \
['gpxpy>=1.4.2,<2.0.0']

entry_points = \
{'console_scripts': ['trackalyzer = trackalyzer.cli:run']}

setup_kwargs = {
    'name': 'trackalyzer',
    'version': '0.1.0',
    'description': 'identify visited points of interest in GPX tracks',
    'long_description': None,
    'author': 'khimaros',
    'author_email': 'me@khimaros.com',
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
