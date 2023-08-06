# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dabapush', 'dabapush.Reader', 'dabapush.Writer']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'SQLAlchemy>=1.4.22,<2.0.0',
 'click>=8.0.0,<9.0.0',
 'loguru>=0.5.3,<0.6.0',
 'pandas>=1.3.1,<2.0.0']

entry_points = \
{'console_scripts': ['dabapush = dabapush.dabapush:run']}

setup_kwargs = {
    'name': 'dabapush',
    'version': '0.1.2',
    'description': '',
    'long_description': "# dabapush\n\nData Base pusher for social media data (Twitter for the beginning) – pre-alpha version\n\n## Developer Install\n\n1. Install [poetry](https://python-poetry.org/docs/#installation)\n2. Clone repository\n3. In the cloned repository's root directory run `poetry install`\n4. Run `poetry shell` to start development virtualenv\n5. Run `twacapic` to enter API keys. Ignore the IndexError.\n6. Run `pytest` to run all tests\n",
    'author': 'Felix Victor Münch',
    'author_email': 'f.muench@leibniz-hbi.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Leibniz-HBI/dabapush',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
