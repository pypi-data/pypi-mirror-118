# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tfl',
 'tfl.api',
 'tfl.api.line',
 'tfl.api.line.meta',
 'tfl.api.presentation',
 'tfl.api.presentation.entities',
 'tfl.cli']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

extras_require = \
{'cli': ['typer>=0.3.2,<0.4.0']}

entry_points = \
{'console_scripts': ['tfl = tfl.__main__:app']}

setup_kwargs = {
    'name': 'mind-the-gap',
    'version': '1.0.0',
    'description': 'TFL',
    'long_description': None,
    'author': 'Antonio Feregrino',
    'author_email': 'antonio.feregrino@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
