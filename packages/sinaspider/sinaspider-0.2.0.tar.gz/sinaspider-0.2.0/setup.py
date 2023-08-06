# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sinaspider']

package_data = \
{'': ['*']}

install_requires = \
['PyExifTool>=0.4.11,<0.5.0',
 'dataset>=1.5.0,<2.0.0',
 'loguru>=0.5.3,<0.6.0',
 'lxml>=4.6.3,<5.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'psycopg2>=2.9.1,<3.0.0',
 'python-baseconv>=1.2.2,<2.0.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'sinaspider',
    'version': '0.2.0',
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
