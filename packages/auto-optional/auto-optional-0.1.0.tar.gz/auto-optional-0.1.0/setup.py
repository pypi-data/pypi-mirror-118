# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['auto_optional']

package_data = \
{'': ['*']}

install_requires = \
['libcst>=0.3.20,<0.4.0', 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['auto-optional = auto_optional.main:app']}

setup_kwargs = {
    'name': 'auto-optional',
    'version': '0.1.0',
    'description': 'Makes typed arguments Optional when the default argument is None',
    'long_description': None,
    'author': 'Luttik',
    'author_email': 'dtluttik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>3.7,<4.0',
}


setup(**setup_kwargs)
