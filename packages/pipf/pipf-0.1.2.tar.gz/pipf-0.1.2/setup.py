# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipf', 'pipf.fzf', 'pipf.fzf.packages_list', 'pipf.fzf.preview']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0', 'shools>=0.1.2,<0.2.0']

entry_points = \
{'console_scripts': ['pipf = pipf.fzf:main']}

setup_kwargs = {
    'name': 'pipf',
    'version': '0.1.2',
    'description': 'Simple CLI PyPI packages finder inside Fuzzy Finder.',
    'long_description': None,
    'author': 'samedamci',
    'author_email': 'samedamci@disroot.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/samedamci/pipf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
