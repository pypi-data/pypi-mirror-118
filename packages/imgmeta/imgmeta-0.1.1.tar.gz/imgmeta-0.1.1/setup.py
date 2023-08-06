# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imgmeta']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'geopy>=2.2.0,<3.0.0',
 'loguru>=0.5.3,<0.6.0',
 'osxphotos>=0.42.80,<0.43.0',
 'photoscript>=0.1.4,<0.2.0',
 'pymongo>=3.12.0,<4.0.0',
 'sinaspider>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'imgmeta',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Bao Hengtao',
    'author_email': 'baohengtao@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
