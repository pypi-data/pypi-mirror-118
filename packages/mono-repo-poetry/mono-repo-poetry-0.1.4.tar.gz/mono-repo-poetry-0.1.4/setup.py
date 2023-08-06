# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mono_repo_poetry']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mono-repo-poetry',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'pvasisht',
    'author_email': 'prajwal_prakashvasisht@intuit.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
