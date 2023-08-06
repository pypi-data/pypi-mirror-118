# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snowowl']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'snowowl',
    'version': '0.0.2',
    'description': 'A collection of common data structures',
    'long_description': '# snowowl\nA collection of common data structures\n',
    'author': 'ABHIJIT SINHA',
    'author_email': 'grey.shell@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/greyshell/snowowl',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
