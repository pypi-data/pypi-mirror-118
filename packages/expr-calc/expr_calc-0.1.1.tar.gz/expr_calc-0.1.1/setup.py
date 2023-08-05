# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['expr_calc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'expr-calc',
    'version': '0.1.1',
    'description': 'Mini language modeled after a calculator',
    'long_description': '# Calc Interpreter\n[![Python package](https://github.com/lestherll/calc/actions/workflows/main.yml/badge.svg)](https://github.com/lestherll/calc/actions/workflows/main.yml)\n[![Python Version](https://img.shields.io/badge/python-3.7%20%7c%203.8%20%7c%203.9%20%7c%203.10-blue)](https://www.python.org/downloads/)\n\n\nA mini-language modeled after a calculator implemented in Python 3.\nThe program currently only lexes basic mathematical expressions. It\nsupports infix (*using Shunting Yard Algorithm*) and postfix \n(*Reverse Polish Notation*).\n\n## Usage\nThe best way to run the program currently is to execute the REPL and\ncan be done in a python file or through your terminal.\n\nAssuming your present working directory is inside the cloned repo, you\ncan run the following command without the comment.\n```shell\n# inside /clone_path/expr_calc/\npython -m expr_calc\n```\n\nEnabling postfix expression mode is also possible. Using infix expressions\nin postfix mode is currently undefined and so is using postfix expressions\nin infix mode.\n```shell\npython -m expr_calc --postfix\n```\n\n## Features\n- Infix expressions\n- Postfix expressions\n- Basic operators such as `+, -, *, /, %, ^`\n- Tokens created from an expression can also be fetched if one wanted to do so\n',
    'author': 'lestherll',
    'author_email': 'ljllacuna5@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lestherll/expr_calc',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
