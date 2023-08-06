# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['CloudConfig', 'CloudConfig.lib']

package_data = \
{'': ['*']}

install_requires = \
['orjson>=3.6.3,<4.0.0',
 'pathlib2>=2.3.6,<3.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'rsa>=4.7.2,<5.0.0',
 'yarl>=1.6.3,<2.0.0']

setup_kwargs = {
    'name': 'cloudconfig',
    'version': '0.2.2',
    'description': '',
    'long_description': None,
    'author': 'Anton Rastyazhenko',
    'author_email': 'rastyazhenko.anton@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Albus/CloudConfig',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
