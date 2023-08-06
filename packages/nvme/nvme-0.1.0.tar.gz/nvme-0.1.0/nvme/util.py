"""Utility functions and classes."""

from ctypes import LittleEndianStructure, c_uint64


class c_uint128(LittleEndianStructure):
    """A 128bit wide integer."""

    _fields_ = [("lqword", c_uint64), ("uqword", c_uint64)]

    def as_int(self) -> int:
        """Return self as a python int."""
        return self.lqword | (self.uqword << 64)
