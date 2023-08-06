# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pieoffice']

package_data = \
{'': ['*']}

install_requires = \
['betacode>=1.0,<2.0', 'docopt>=0.6.2,<0.7.0']

setup_kwargs = {
    'name': 'pieoffice',
    'version': '1.3.0',
    'description': 'A terminal based script converter for ancient (Proto-)Indo-European languages.',
    'long_description': None,
    'author': 'Caio Geraldes',
    'author_email': 'caio.geraldes@usp.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
