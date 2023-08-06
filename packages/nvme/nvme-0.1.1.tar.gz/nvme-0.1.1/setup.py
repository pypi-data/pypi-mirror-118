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
    'version': '0.1.1',
    'description': '',
    'long_description': "# pynvme\n\nA pure python implementation of the NVMe spec's data structures, and a plugin\ninfrastructure for driver specific accessors to devices.\n\n## Driver Plugins\n\nDrive implementations are concrete subclasses of `nvme.Driver`. This abstract\nclass defines the bare minimum behavior necessary to send NVMe commands to a\ndevice. In order for the plugin to be recognized by this module, they must\nexpose the class as a [setuptools entry point][setuptools-entry], or if you are\nusing the Poetry build system, as a [plugin][poetry-plugins].\n\n[setuptools-entry]: https://setuptools.readthedocs.io/en/latest/userguide/entry_point.html\n[poetry-plugins]: https://python-poetry.org/docs/pyproject#plugins\n\n## Versioning\n\nThis package follows semantic versioning. Until version 1.0 expect API changes\nwithout notice and expect that not everything is implemented.",
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
