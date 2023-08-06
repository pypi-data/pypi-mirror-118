# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['filesharing',
 'filesharing.common',
 'filesharing.db',
 'filesharing.domains',
 'filesharing.screens',
 'filesharing.utils']

package_data = \
{'': ['*'], 'filesharing': ['build/*', 'resources/*']}

install_requires = \
['Flask-RESTful>=0.3.9,<0.4.0',
 'Flask>=2.0.1,<3.0.0',
 'black>=21.7b0,<22.0',
 'colorlog>=5.0.1,<6.0.0',
 'dnspython>=2.1.0,<3.0.0',
 'pip>=21.2.4,<22.0.0',
 'pyinstaller>=4.5.1,<5.0.0',
 'pymongo>=3.12.0,<4.0.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'filesharing',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'YCipriani',
    'author_email': 'yonatancipriani@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
