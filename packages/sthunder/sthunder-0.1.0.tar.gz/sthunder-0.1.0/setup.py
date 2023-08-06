# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sthunder', 'sthunder.database', 'sthunder.lulc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sthunder',
    'version': '0.1.0',
    'description': 'Self-Organizing Maps applied to thunderstorm analysis.',
    'long_description': None,
    'author': 'Adriano P. Almeida',
    'author_email': 'adriano.almeida@inpe.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
