# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minerl_wrappers',
 'minerl_wrappers.core',
 'minerl_wrappers.pfrl',
 'minerl_wrappers.pfrl.wrappers']

package_data = \
{'': ['*'], 'minerl_wrappers': ['data/*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'gym>=0.18.3,<0.19.0',
 'minerl==0.4.1',
 'numpy>=1.21.0,<2.0.0',
 'opencv-python>=4.5.3,<5.0.0']

setup_kwargs = {
    'name': 'minerl-wrappers',
    'version': '0.1.2',
    'description': 'minerl-wrappers compiles common wrappers and standardizes code for reproducibility in the MineRL environment!',
    'long_description': None,
    'author': 'Julius Frost',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
