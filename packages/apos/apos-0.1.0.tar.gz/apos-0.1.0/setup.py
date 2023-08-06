# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apos']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'apos',
    'version': '0.1.0',
    'description': 'The backbone for message-driven applications',
    'long_description': None,
    'author': 'Max Kossatz',
    'author_email': 'max@kossatzonline.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mkossatz/apos',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
