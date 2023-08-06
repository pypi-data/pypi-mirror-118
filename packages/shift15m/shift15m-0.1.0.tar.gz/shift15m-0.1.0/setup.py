# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shift15m', 'shift15m.datasets']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=4.0.2,<5.0.0',
 'furo>=2021.6.24-beta.37,<2022.0.0',
 'matplotlib>=3.4.2,<4.0.0',
 'pandas>=1.2.4,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'seaborn>=0.11.1,<0.12.0',
 'sklearn>=0.0,<0.1',
 'tqdm>=4.62.0,<5.0.0']

extras_require = \
{'pytorch': ['torch==1.9.0']}

setup_kwargs = {
    'name': 'shift15m',
    'version': '0.1.0',
    'description': 'Large-scale multiobective dataset with dataset shift.',
    'long_description': None,
    'author': 'Masanari Kimura',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
