"""Completion queue data structures.

Reference: NVM Express Revision 1.4c, Section 4.6
"""

from ctypes import LittleEndianStructure, c_uint16, c_uint32


class StatusField(c_uint16):
    """The completion status of a NVMe command.

    Reference: NVM Express Revision 1.4c, Section 4.6.1
    """

    @property
    def p(self):
        """Return the phase tag."""
        return self.value & 0x01

    @property
    def sc(self):
        """Return status code."""
        return (self.value >> 1) & 0xFF

    @property
    def sct(self):
        """Return the status code type."""
        return (self.value >> 25) & 0x07

    @property
    def crd(self):
        """Return the command relay delay."""
        return (self.value >> 28) & 0x03

    @property
    def m(self):
        """Return the more flag."""
        return (self.value >> 30) & 0x01

    @property
    def dnr(self):
        """Return the do not retry flag."""
        return (self.value >> 31) & 0x01


class CompletionQueueEntry(LittleEndianStructure):
    """An entry in the completion queue.

    Reference: NVM Express Revision 1.4c, Section 4.6
    """

    _pack_ = 1
    _fields_ = [
        ("dw0", c_uint32),
        ("dw1", c_uint32),
        ("sqhd", c_uint16),
        ("sqid", c_uint16),
        ("cid", c_uint16),
        ("sf", StatusField),
    ]
