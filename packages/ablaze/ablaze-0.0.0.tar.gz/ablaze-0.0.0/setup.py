# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ablaze']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ablaze',
    'version': '0.0.0',
    'description': 'A Discord library to ease bot development and improve speed of development.',
    'long_description': None,
    'author': 'vcokltfre',
    'author_email': 'vcokltfre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vcokltfre/ablaze',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
