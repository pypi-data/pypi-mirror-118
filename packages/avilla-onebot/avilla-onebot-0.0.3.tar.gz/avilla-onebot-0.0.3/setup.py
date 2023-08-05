# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['onebot']

package_data = \
{'': ['*']}

install_requires = \
['avilla-core>=0.0.8,<0.0.9', 'immutables>=0.15,<0.16']

setup_kwargs = {
    'name': 'avilla-onebot',
    'version': '0.0.3',
    'description': '',
    'long_description': None,
    'author': 'GreyElaina',
    'author_email': 'GreyElaina@outlook.com',
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
