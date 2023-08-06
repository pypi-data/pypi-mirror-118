# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openlist_server']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['openlist-server = openlist_server.cli:run']}

setup_kwargs = {
    'name': 'openlist-server',
    'version': '0.0.1',
    'description': 'OpenList backend server API.',
    'long_description': '# openlist-server\nOpenList backend\n',
    'author': 'gruvw',
    'author_email': 'gruvw.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gruvw/openlist-server',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
