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
    'version': '0.1.2',
    'description': 'A utility for labeling clusters of text data.',
    'long_description': "# CLabel\n\nCLabel is a terminal-based cluster labeling tool that allows you to explore text data interactively and label clusters based on reviewing that data.\n\n## Install & Quickstart\n\n```\npip install clabel\n```\n\nType `clabel` to run. Everything should happen in the terminal from there.\n\nCurrently `clabel` can only import CSV files. It expects two columns to be in your csv: a column of text (`string`) and a column of cluster labels (`int`). You'll identify these the first time you import a dataset.\n\nThe workflow is:\n1. Pick a cluster to view examples. You'll view this through a pager so you can page through examples.\n2. Come up with a name for that cluster (`Declare Name`)\n3. Repeat 1 & 2 until all your clusters have names.\n\nYou can persist any cluster labels to a `json` file when you exit, so you don't have to complete labeling in one session. Then, you can load those labels in the next time you start `clabel` by selecting that `json` file and continue labeling.\n\n## Screenshots\n\n![Pager of Examples](https://i.ibb.co/SwkPHBP/Screen-Shot-2021-08-30-at-4-41-14-PM.png)\n![Declaring name of a cluster](https://i.ibb.co/9cM9Q5G/Screen-Shot-2021-08-30-at-4-42-11-PM.png)\n![Naming Autocomplete](https://i.ibb.co/rF5qKPN/Screen-Shot-2021-08-30-at-4-41-49-PM.png)\n",
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
