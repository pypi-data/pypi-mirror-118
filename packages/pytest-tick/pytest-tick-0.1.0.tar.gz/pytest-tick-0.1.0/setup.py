# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pytest_tick']
install_requires = \
['playsound>=1.3.0,<2.0.0', 'pytest>=6.2.5,<7.0.0']

entry_points = \
{'pytest11': ['pytest-tick = pytest_tick']}

setup_kwargs = {
    'name': 'pytest-tick',
    'version': '0.1.0',
    'description': 'Ticking on tests',
    'long_description': None,
    'author': 'Platonov Anatoliy',
    'author_email': 'p4m.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/platonoff-dev/pytest-tick',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
