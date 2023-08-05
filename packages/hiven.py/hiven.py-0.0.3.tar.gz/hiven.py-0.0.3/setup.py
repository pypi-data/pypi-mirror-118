# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hiven', 'hiven.errors', 'hiven.gateway', 'hiven.types']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'hiven.py',
    'version': '0.0.3',
    'description': "📦 Opensource Python wrapper for Hiven's HTTP and WebSocket API",
    'long_description': None,
    'author': 'Kevin Thomas',
    'author_email': 'kevin.jt2007@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/trustedmercury/hiven.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
