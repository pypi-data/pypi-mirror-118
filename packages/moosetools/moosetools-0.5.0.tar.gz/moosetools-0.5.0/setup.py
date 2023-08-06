# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moosetools', 'moosetools.test']

package_data = \
{'': ['*']}

install_requires = \
['requests-toolbelt>=0.9,<0.10', 'requests>=2,<3']

setup_kwargs = {
    'name': 'moosetools',
    'version': '0.5.0',
    'description': 'Moose Tools',
    'long_description': '',
    'author': 'Chuck Mo',
    'author_email': 'chuck@moosejudge.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://moosetools.moosejudge.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
