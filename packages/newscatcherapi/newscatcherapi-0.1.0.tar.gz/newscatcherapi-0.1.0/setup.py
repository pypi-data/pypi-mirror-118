# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['newscatcherapi']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=1.4,<2.0']

setup_kwargs = {
    'name': 'newscatcherapi',
    'version': '0.1.0',
    'description': 'Python SDK NewsCatcher News API',
    'long_description': None,
    'author': 'Maksym Sugonyaka',
    'author_email': 'maksym@newscatcherapi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
