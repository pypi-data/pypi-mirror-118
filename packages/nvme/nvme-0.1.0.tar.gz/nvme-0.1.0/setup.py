# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nvme', 'nvme.cmd', 'nvme.cmd.admin', 'nvme.driver']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=4.8.1,<5.0.0']

entry_points = \
{'nvme.drivers.linux': ['linux = nvme.driver.linuxioctl:LinuxIoctlDriver']}

setup_kwargs = {
    'name': 'nvme',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Gregory C. Oakes',
    'author_email': 'gregcoakes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.0',
}


setup(**setup_kwargs)
