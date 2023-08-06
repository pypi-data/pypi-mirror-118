# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lib0']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lib0',
    'version': '0.5.2',
    'description': '',
    'long_description': None,
    'author': 'Tester',
    'author_email': 'tester@pbt.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
