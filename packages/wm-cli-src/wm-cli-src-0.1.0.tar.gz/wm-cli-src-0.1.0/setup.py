# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wm_cli_src']

package_data = \
{'': ['*']}

install_requires = \
['click==8.0.0']

setup_kwargs = {
    'name': 'wm-cli-src',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'mohamedarzikiwm',
    'author_email': 'mohamed.a@wemaintain.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
