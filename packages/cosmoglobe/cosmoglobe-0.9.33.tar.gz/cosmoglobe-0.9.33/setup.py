# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cosmoglobe',
 'cosmoglobe.chain',
 'cosmoglobe.plot',
 'cosmoglobe.sky',
 'cosmoglobe.utils']

package_data = \
{'': ['*'], 'cosmoglobe': ['data/*']}

install_requires = \
['astropy>=4.3.1,<5.0.0',
 'click>=8.0.1',
 'cmasher>=1.6.2,<2.0.0',
 'h5py>=3.0.0',
 'healpy>=1.15.0,<2.0.0',
 'matplotlib>=3.4.3,<4.0.0',
 'numba>=0.50.1,<0.51.0',
 'numpy>=1.19.0,<1.20.0',
 'rich>=10.9.0,<11.0.0',
 'scipy>=1.6.0',
 'tqdm>=4.62.2,<5.0.0']

entry_points = \
{'console_scripts': ['cosmoglobe = cosmoglobe.__main__:cli']}

setup_kwargs = {
    'name': 'cosmoglobe',
    'version': '0.9.33',
    'description': 'cosmoglobe is a python package that interfaces the Cosmoglobe Sky Model with commander3 outputs for the purpose of producing astrophysical sky maps.',
    'long_description': None,
    'author': 'Metin San',
    'author_email': 'metinisan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
