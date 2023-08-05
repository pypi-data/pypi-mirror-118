# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['olympia']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'olympia',
    'version': '0.1.0',
    'description': 'olympia',
    'long_description': '# Lumos\n',
    'author': 'Luke Miloszewski',
    'author_email': 'lukemiloszewski@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.9,<4.0.0',
}


setup(**setup_kwargs)
