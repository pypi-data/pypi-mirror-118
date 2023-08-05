# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['messages']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.21,<3.0', 'validus>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'messages',
    'version': '0.7.0',
    'description': 'Easy and efficient messaging.',
    'long_description': None,
    'author': 'Tim Phillips',
    'author_email': 'phillipstr@gmail.com',
    'url': 'https://github.com/trp07/messages',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
