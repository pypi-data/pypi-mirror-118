# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['polymatheia_tools', 'polymatheia_tools.download']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=3.9.2,<4.0.0',
 'loguru>=0.5.3,<0.6.0',
 'matplotlib>=3.4.3,<4.0.0',
 'polymatheia>=0.3.1,<0.4.0',
 'progress>=1.6,<2.0']

setup_kwargs = {
    'name': 'polymatheia-tools',
    'version': '0.1.1',
    'description': 'A Python package that provides useful scripts for working with data loaded using the Polymatheia library.',
    'long_description': None,
    'author': 'Andreas Lüschow',
    'author_email': 'lueschow@sub.uni-goettingen.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
