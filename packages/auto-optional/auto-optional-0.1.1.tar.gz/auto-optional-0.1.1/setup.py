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
    'version': '0.1.1',
    'description': 'Makes typed arguments Optional when the default argument is None',
    'long_description': '# auto-optional\nMakes typed arguments Optional when the default argument is None.\n\nFor example:\n```py\ndef foo(bar: str = None):\n    ...\n```\n\nWould turn into\n\n```py\nfrom typing import Optional\ndef foo(bar: Optional[str] = None):\n    ...\n```\n\n## Install\nInstall with `pip install auto-optional`.\n\n## run\nYou can run this with `auto-optional [path]` (path is an optional argument).\n\n## Properties\n\n- Existing imports are reused.\n- \n- `import as` statements are properly handled.\n\n## Things of note\n\nFor all these points I welcome pull-requests.\n\n- There is no exclude (path patterns) option yet\n- There is no ignore (code line) option yet\n- Code is aways read and written as `UTF-8` (which is accurate most of the time).\n',
    'author': 'Luttik',
    'author_email': 'dtluttik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Luttik/auto-optional',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>3.7,<4.0',
}


setup(**setup_kwargs)
