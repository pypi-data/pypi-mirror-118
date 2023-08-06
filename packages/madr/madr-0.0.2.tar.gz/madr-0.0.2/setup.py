# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['madr', 'madr.commands', 'madr.commands.init']

package_data = \
{'': ['*'],
 'madr.commands.init': ['template/*',
                        'template/docs/*',
                        'template/template/*',
                        'template/template/assets/*']}

entry_points = \
{'console_scripts': ['madr = madr.cli:run']}

setup_kwargs = {
    'name': 'madr',
    'version': '0.0.2',
    'description': 'A comprehensive toolset around making and managing MADRs using source control',
    'long_description': None,
    'author': 'WilliamJohns',
    'author_email': 'will@wcj.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
