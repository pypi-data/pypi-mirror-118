# pynvme

A pure python implementation of the NVMe spec's data structures, and a plugin
infrastructure for driver specific accessors to devices.

## Driver Plugins

Drive implementations are concrete subclasses of `nvme.Driver`. This abstract class
defines the bare minimum behavior necessary to send NVMe commands to a device. In order
for the plugin to be recognized by this module, they must expose the class as a
[setuptools entry point][setuptools-entry], or if you are using the Poetry build system,
as a [plugin][poetry-plugins].

[setuptools-entry]: https://setuptools.readthedocs.io/en/latest/userguide/entry_point.html
[poetry-plugins]: https://python-poetry.org/docs/pyproject#plugins

## Versioning

This package follows semantic versioning. Every minor change before 1.0 may contain
breaking changes in addition to feature additions.