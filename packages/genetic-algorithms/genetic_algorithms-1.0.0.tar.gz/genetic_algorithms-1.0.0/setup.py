# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['genetic_algorithms', 'genetic_algorithms.examples', 'genetic_algorithms.test']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.2,<2.0.0']

setup_kwargs = {
    'name': 'genetic-algorithms',
    'version': '1.0.0',
    'description': 'This library is a wrapper for genetic algorithms to leverage in optimisation problems.',
    'long_description': None,
    'author': 'Toby',
    'author_email': 'toby@thedevlins.biz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
