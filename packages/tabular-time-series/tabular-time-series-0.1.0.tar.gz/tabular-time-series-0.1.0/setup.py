# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tabular_time_series']

package_data = \
{'': ['*'],
 'tabular_time_series': ['.pytest_cache/*', '.pytest_cache/v/cache/*']}

install_requires = \
['pandas>=1.3.2,<2.0.0']

setup_kwargs = {
    'name': 'tabular-time-series',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Felipe Whitaker',
    'author_email': 'felipewhitaker@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
