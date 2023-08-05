# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['expr_calc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'expr-calc',
    'version': '0.1.0',
    'description': 'Mini language modeled after a calculator',
    'long_description': None,
    'author': 'lestherll',
    'author_email': 'ljllacuna5@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
