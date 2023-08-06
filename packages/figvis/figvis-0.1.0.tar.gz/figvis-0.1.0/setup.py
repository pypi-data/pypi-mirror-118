# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['figvis', 'figvis.cli', 'figvis.data', 'figvis.figment', 'figvis.transform']

package_data = \
{'': ['*'], 'figvis': ['templates/base/*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0',
 'h5py>=3.4.0,<4.0.0',
 'lxml>=4.6.3,<5.0.0',
 'numpy>=1.21.2,<2.0.0',
 'selenium>=4.0.0.b4',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['figvis = figvis.cli.main:app']}

setup_kwargs = {
    'name': 'figvis',
    'version': '0.1.0',
    'description': 'Figment Visualization is a framework to visualize data using templates',
    'long_description': 'figvis\n======\n\nFigment Visualization is a framework to visualize data using templates\n\nRequirements\n++++++++++++\n\nInstallation\n++++++++++++\n\nUsage\n+++++\n\nCommand line\n------------\n\nProgrammatic\n------------\n\nExample\n-------',
    'author': 'Umesh Mohan',
    'author_email': 'moh@nume.sh',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://u-m.gitlab.io/figvis/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
