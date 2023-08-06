# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['roborabbit']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'aio-pika>=6.8.0,<7.0.0', 'click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['roborabbit = run:config_rmq']}

setup_kwargs = {
    'name': 'roborabbit',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Skyler Lewis',
    'author_email': 'skyler@hivewire.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
