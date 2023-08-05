# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['defectio', 'defectio.types']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0',
 'msgpack>=1.0.2,<2.0.0',
 'orjson>=3.6.3,<4.0.0',
 'ulid-py>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'defectio',
    'version': '0.1.0a0',
    'description': '',
    'long_description': None,
    'author': 'Leon Bowie',
    'author_email': 'leon@bowie-co.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
