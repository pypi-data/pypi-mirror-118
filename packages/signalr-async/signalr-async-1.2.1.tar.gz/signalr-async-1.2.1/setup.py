# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['signalr_async', 'signalr_async.core', 'signalr_async.core.protocols']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.0,<4.0.0', 'msgpack>=1.0.2,<2.0.0', 'websockets>=8.1,<9.0']

setup_kwargs = {
    'name': 'signalr-async',
    'version': '1.2.1',
    'description': 'Python SignalR async client',
    'long_description': '',
    'author': 'Sam Mosleh',
    'author_email': 'sam.mosleh@ut.ac.ir',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sam-mosleh/signalr-async',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
