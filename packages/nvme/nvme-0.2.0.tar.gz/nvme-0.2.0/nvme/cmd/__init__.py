"""Data structures associated with submission and completion queues.

Reference: NVM Express Revision 1.4c, Section 4.2
"""

from ctypes import LittleEndianStructure, c_uint32, c_uint64

from nvme.util import c_uint128


class Cmd(LittleEndianStructure):
    """Submission queue entry command format.

    Attributes:
        cdw0 (c_uint32): Command Dword 0.
        nsid (c_uint32): Namespace ID.
        mptr (c_uint64): Metadata pointer.
        dptr (c_uint128): Data pointer.
        cdw10 (c_uint32): Command Dword 10.
        cdw11 (c_uint32): Command Dword 11.
        cdw12 (c_uint32): Command Dword 12.
        cdw13 (c_uint32): Command Dword 13.
        cdw14 (c_uint32): Command Dword 14.
        cdw15 (c_uint32): Command Dword 15.
    """

    _pack_ = 1
    _fields_ = [
        ("cdw0", c_uint32),
        ("nsid", c_uint32),
        ("cdw2", c_uint32),
        ("cdw3", c_uint32),
        ("mptr", c_uint64),
        ("dptr", c_uint128),
        ("cdw10", c_uint32),
        ("cdw11", c_uint32),
        ("cdw12", c_uint32),
        ("cdw13", c_uint32),
        ("cdw14", c_uint32),
        ("cdw15", c_uint32),
    ]
