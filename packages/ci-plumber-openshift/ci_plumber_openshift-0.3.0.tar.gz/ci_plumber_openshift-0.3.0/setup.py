# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ci_plumber_openshift']

package_data = \
{'': ['*']}

install_requires = \
['ci-plumber>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'ci-plumber-openshift',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Miles Budden',
    'author_email': 'git@miles.so',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
