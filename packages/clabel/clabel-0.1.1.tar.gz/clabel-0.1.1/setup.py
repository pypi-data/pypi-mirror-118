# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['clabel']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=8.12.1,<9.0.0',
 'pandas>=1.3.2,<2.0.0',
 'questionary>=1.10.0,<2.0.0',
 'rich>=10.7.0,<11.0.0']

entry_points = \
{'console_scripts': ['clabel = clabel.main:main']}

setup_kwargs = {
    'name': 'clabel',
    'version': '0.1.1',
    'description': 'A utility for labeling clusters of text data.',
    'long_description': '# CLabel\n\nCLabel is a terminal-based cluster labeling tool that allows you to explore text data interactively and label clusters based on reviewing that data.\n\n## Install & Quickstart\n\n```\npip install clabel\n```\n\nType `clabel` to run. Everything should happen in the terminal from there.\n\n## Screenshots\n\n![](https://i.ibb.co/5hQ6CL6/Screen-Shot-2021-08-30-at-4-41-14-PM.png)\n![](https://i.ibb.co/YPfJ49w/Screen-Shot-2021-08-30-at-4-41-49-PM.png)\n![](https://i.ibb.co/wBvN5mY/Screen-Shot-2021-08-30-at-4-42-11-PM.png)\n',
    'author': 'Peter B',
    'author_email': '5107405+pmbaumgartner@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pmbaumgartner/clabel',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
