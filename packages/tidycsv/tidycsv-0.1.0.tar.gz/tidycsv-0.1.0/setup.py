# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tidycsv', 'tidycsv.core', 'tidycsv.utils']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.4,<2.0.0']

setup_kwargs = {
    'name': 'tidycsv',
    'version': '0.1.0',
    'description': 'A minimalistic solution to messy CSV files.',
    'long_description': None,
    'author': 'Gustavo Magaña López',
    'author_email': 'gmaganna.biomed@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
