"""Pure python implementation of the NVMe spec's data structures.

Each spec defined data structure is defined using `ctypes` without any platform
specific extension modules or driver specific behavior.

It also defines a `setuptools` entry point for plugins to define driver specific
behavior which allows command submission using a consistent API.
"""
__version__ = "0.1.1"

__all__ = [
    "get_driver",
    "get_driver_names",
    "Driver",
    "Cmd",
    "CompletionQueueEntry",
    "StatusField",
    "Buffer",
    "Controller",
    "Namespace",
    "IdCtrl",
    "IdNmsp",
    "LbaFormat",
    "PowerState",
    "ErrorLogEntry",
    "FwSlotLog",
    "SmartLog",
]

import sys
from typing import Set

try:
    from importlib.metadata import entry_points
except ImportError:
    from importlib_metadata import entry_points

# Re-export these structures.
from .cmd import Cmd
from .cmd.admin.identify import IdCtrl, IdNmsp, LbaFormat, PowerState
from .cmd.admin.logpage import ErrorLogEntry, FwSlotLog, SmartLog
from .cmd.completion import CompletionQueueEntry, StatusField
from .driver import Buffer, Controller, Driver, Namespace

_entry_points = entry_points()
_DRIVERS = {driver.name: driver for driver in _entry_points.get("nvme.drivers", [])}
_DRIVERS.update(
    (driver.name, driver)
    for driver in _entry_points.get(f"nvme.drivers.{sys.platform}", [])
)


def get_driver(name: str, **config) -> Driver:
    """Return the driver implmentation for `name`.

    > *NOTE*: This does not guarantee that any devices are actually bound to this
    driver. That must be handled external to initializing the driver.

    Raises:
        ValueError - No driver implementation for the given `name`.
    """
    impl = _DRIVERS.get(name)
    if impl is None:
        raise ValueError(f"Unknown driver name: {name}")
    cls = impl.load()
    return cls(**config)


def get_driver_names() -> Set[str]:
    """Return the set of available driver names.

    This only includes the drivers which are platform independent and any drivers
    specific to this platform.
    """
    return set(_DRIVERS)
