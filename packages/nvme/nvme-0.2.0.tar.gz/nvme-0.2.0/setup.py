# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nvme', 'nvme.cmd', 'nvme.cmd.admin', 'nvme.driver']

package_data = \
{'': ['*']}

extras_require = \
{':python_version >= "3.6" and python_version < "3.8"': ['importlib-metadata>=4.8.1,<5.0.0']}

entry_points = \
{'nvme.drivers.linux': ['linux = nvme.driver.linuxioctl:LinuxIoctlDriver']}

setup_kwargs = {
    'name': 'nvme',
    'version': '0.2.0',
    'description': '',
    'long_description': "# pynvme\n\nA pure python implementation of the NVMe spec's data structures, and a plugin\ninfrastructure for driver specific accessors to devices.\n\n## Driver Plugins\n\nDrive implementations are concrete subclasses of `nvme.Driver`. This abstract class\ndefines the bare minimum behavior necessary to send NVMe commands to a device. In order\nfor the plugin to be recognized by this module, they must expose the class as a\n[setuptools entry point][setuptools-entry], or if you are using the Poetry build system,\nas a [plugin][poetry-plugins].\n\n[setuptools-entry]: https://setuptools.readthedocs.io/en/latest/userguide/entry_point.html\n[poetry-plugins]: https://python-poetry.org/docs/pyproject#plugins\n\n## Versioning\n\nThis package follows semantic versioning. Every minor change before 1.0 may contain\nbreaking changes in addition to feature additions.",
    'author': 'Gregory C. Oakes',
    'author_email': 'gregcoakes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.0,<4.0.0',
}


setup(**setup_kwargs)
