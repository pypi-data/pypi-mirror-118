# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['erroi']

package_data = \
{'': ['*']}

install_requires = \
['SoundsLike>=0.0.11,<0.0.12']

setup_kwargs = {
    'name': 'erroi',
    'version': '0.1.0',
    'description': 'ERRant Other Improver',
    'long_description': None,
    'author': 'Aneta Melisa Stal',
    'author_email': 'melisa-qordoba@writer.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
