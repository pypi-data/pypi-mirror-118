# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starflow']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'starflow',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Michael Calamera',
    'author_email': 'michael.calamera@morningstar.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
