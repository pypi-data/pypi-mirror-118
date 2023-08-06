# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['altest']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==5.3.1',
 'aiobotocore==1.3.3',
 'aiosqlite==0.16.0',
 'databases==0.4.2',
 'httpx==0.18.2',
 'pycryptodome==3.10.1',
 'pydantic==1.7.3',
 'sqlalchemy==1.3.23',
 'structlog==20.1.0',
 'websockets==9.1']

extras_require = \
{'all': ['pyjwt==2.0.1',
         'fastapi==0.63.0',
         'spacy==3.0.6',
         'pyduckling-native==0.1.0',
         'discord.py==1.6.0',
         'emoji==1.2.0',
         'matrix-nio==0.18.6'],
 'auth': ['pyjwt==2.0.1', 'fastapi==0.63.0'],
 'chatdsl': ['discord.py==1.6.0', 'emoji==1.2.0', 'matrix-nio==0.18.6'],
 'parser': ['spacy==3.0.6', 'pyduckling-native==0.1.0']}

setup_kwargs = {
    'name': 'altest',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
