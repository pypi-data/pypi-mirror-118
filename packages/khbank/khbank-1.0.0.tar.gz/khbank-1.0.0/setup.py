# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['khbank']

package_data = \
{'': ['*']}

install_requires = \
['toolz>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'khbank',
    'version': '1.0.0',
    'description': 'parse bank statement',
    'long_description': None,
    'author': 'Khalid',
    'author_email': 'khalidck@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
