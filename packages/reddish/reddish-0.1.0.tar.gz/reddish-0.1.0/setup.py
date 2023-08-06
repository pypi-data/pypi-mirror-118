# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reddish']

package_data = \
{'': ['*']}

install_requires = \
['hiredis>=2.0.0,<3.0.0', 'pydantic>=1.8.2,<2.0.0', 'trio>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'reddish',
    'version': '0.1.0',
    'description': 'An async redis client library with a minimal api',
    'long_description': None,
    'author': 'Sascha Desch',
    'author_email': 'sascha.desch@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
