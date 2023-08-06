# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sisifo', 'sisifo.namespaces', 'sisifo.namespaces.common', 'sisifo.utils']

package_data = \
{'': ['*']}

extras_require = \
{'yaml': ['pyyaml>=5.4.1,<6.0.0']}

setup_kwargs = {
    'name': 'sisifo',
    'version': '0.1.0',
    'description': 'Generic framework for running tasks',
    'long_description': "![Sisyphus silhouette](./logo/logo.png)\n\n\n# Sísifo - Task runner\n\nSísifo is the Spanish form of Sisyphus, in ancient Greek: Σίσυφος. This poor\nguy was punished for his self-aggrandizing craftiness and deceitfulness by\nbeing forced to roll an immense boulder up a hill only for it to roll down\nevery time it neared the top, repeating this action for eternity. More\ninformation in [Wikipedia](https://en.wikipedia.org/wiki/Sisyphus).\n\nThis poor library is doomed to an eternity of performing tasks with no other\npurpose in its pitiful and miserable life. I hope you didn't make fun of this\ninsignificant library, our existence is not much more encouraging...\n\n\n# How does it work?\n\nEssentially, Sísifo is just a library that allows you to run tasks on a data\ncollection. Therefore, the most important classes of the library are:\n\n* `sisifo.DataCollection`. See a DataCollection like a dictionary. Use a key to\nstore/retrieve any kind of value from a data collection. The values stored in a\ndata collection are called **entities**.\n* `sisifo.Task`. A task is an action that, usually, modifies the entities in a\ndata collection.\n",
    'author': 'guiferviz',
    'author_email': 'guiferviz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/guiferviz/sisifo',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
