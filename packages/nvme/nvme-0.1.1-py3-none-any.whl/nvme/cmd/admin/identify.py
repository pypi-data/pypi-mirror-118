"""Identify command datastructures.

Reference: NVM Express 1.4c, Section 5.15.2
"""

from ctypes import (
    LittleEndianStructure,
    c_bool,
    c_char,
    c_uint8,
    c_uint16,
    c_uint32,
    c_uint64,
)

from nvme.util import c_uint128


class PowerState(LittleEndianStructure):
    """The power state descriptor data structure.

    Reference: NVM Express Revision 1.4c, Section 5.15.2.2, Figure 252
    """

    _pack_ = 1
    _fields_ = [
        ("mp", c_uint16, 16),
        ("_rsvd1", c_uint8, 8),
        ("mxps", c_bool, 1),
        ("nops", c_bool, 1),
        ("_rsvd2", c_uint8, 6),
        ("enlat", c_uint32, 32),
        ("exlat", c_uint32, 32),
        ("rrt", c_uint8, 5),
        ("_rsvd3", c_uint8, 3),
        ("rrl", c_uint8, 5),
        ("_rsvd4", c_uint8, 3),
        ("rwt", c_uint8, 5),
        ("_rsvd5", c_uint8, 3),
        ("rwl", c_uint8, 5),
        ("_rsvd6", c_uint8, 3),
        ("idlp", c_uint8, 5),
        ("_rsvd7", c_uint8, 3),
        ("ips", c_uint16, 16),
        ("_rsvd8", c_uint8, 8),
        ("actp", c_uint16, 16),
        ("apw", c_uint8, 3),
        ("_rsvd9", c_uint8, 3),
        ("aps", c_uint8, 2),
        ("_rsvd10", c_uint8 * 9),
    ]


class IdCtrl(LittleEndianStructure):
    """The identify controller data structure.

    Reference: NVM Express Revision 1.4c, Section 5.15.2.2, Figure 251
    """

    _pack_ = 1
    _fields_ = [
        ("vid", c_uint16),
        ("ssvid", c_uint16),
        ("sn", c_char * 20),
        ("mn", c_char * 40),
        ("fr", c_char * 8),
        ("rab", c_uint8),
        ("ieee", c_uint8 * 3),
        ("cmic", c_uint8),
        ("mdts", c_uint8),
        ("cntlid", c_uint16),
        ("ver", c_uint32),
        ("rtd3r", c_uint32),
        ("rtd3e", c_uint32),
        ("oaes", c_uint32),
        ("ctratt", c_uint32),
        ("rrls", c_uint16),
        ("_rsvd102", c_uint8 * 9),
        ("cntrltype", c_uint8),
        ("fguid", c_uint128),
        ("crdts", c_uint16 * 3),
        ("_rsvd134", c_uint8 * 106),
        ("_rsvd240", c_uint8 * 13),
        ("nvmsr", c_uint8),
        ("vwci", c_uint8),
        ("mec", c_uint8),
        ("oacs", c_uint16),
        ("acl", c_uint8),
        ("aerl", c_uint8),
        ("frmw", c_uint8),
        ("lpa", c_uint8),
        ("elpe", c_uint8),
        ("npss", c_uint8),
        ("avscc", c_uint8),
        ("apsta", c_uint8),
        ("wctemp", c_uint16),
        ("cctemp", c_uint16),
        ("mtfa", c_uint16),
        ("hmpre", c_uint32),
        ("hmmin", c_uint32),
        ("tnvmcap", c_uint128),
        ("unvmcap", c_uint128),
        ("rpmbs", c_uint32),
        ("edst", c_uint16),
        ("dsto", c_uint8),
        ("fwug", c_uint8),
        ("kas", c_uint16),
        ("hctma", c_uint16),
        ("mntma", c_uint16),
        ("mxtmt", c_uint16),
        ("sanicap", c_uint32),
        ("hmminds", c_uint32),
        ("hmmaxd", c_uint16),
        ("nsetidmax", c_uint16),
        ("endgidmax", c_uint16),
        ("anatt", c_uint8),
        ("anacap", c_uint8),
        ("anagrpmax", c_uint32),
        ("nanagrpid", c_uint32),
        ("pels", c_uint32),
        ("_rsvd356", c_uint8 * 156),
        ("sqes", c_uint8),
        ("cqes", c_uint8),
        ("maxcmd", c_uint16),
        ("nn", c_uint32),
        ("oncs", c_uint16),
        ("fuses", c_uint16),
        ("fna", c_uint8),
        ("vwc", c_uint8),
        ("awun", c_uint16),
        ("awupf", c_uint16),
        ("nvscc", c_uint8),
        ("nwpc", c_uint8),
        ("acwu", c_uint16),
        ("_rsvd534", c_uint8 * 2),
        ("sgls", c_uint32),
        ("mnan", c_uint32),
        ("_rsvd544", c_uint8 * 224),
        ("subnqn", c_char * 256),
        ("_rsvd1024", c_uint8 * 768),
        ("_rsvd1792", c_uint8 * 256),
        ("psds", PowerState * 32),
        ("_rsvd3072", c_uint8 * 1024),
    ]


class LbaFormat(LittleEndianStructure):
    """The LBA format data structure.

    Reference: NVM Express Revision 1.4c, Section 5.15.2.1, Figure 250
    """

    _pack_ = 1
    _fields_ = [
        ("ms", c_uint16, 16),
        ("lbads", c_uint8, 8),
        ("rp", c_uint8, 2),
        ("_rsvd", c_uint8, 6),
    ]


class IdNmsp(LittleEndianStructure):
    """The identify namespace data structure.

    Reference: NVM Express Revision 1.4c, Section 5.15.2.1, Figure 249
    """

    _pack_ = 1
    _fields_ = [
        ("nsze", c_uint64),
        ("ncap", c_uint64),
        ("nuse", c_uint64),
        ("nsfeat", c_uint8),
        ("nlbaf", c_uint8),
        ("flbas", c_uint8),
        ("mc", c_uint8),
        ("dpc", c_uint8),
        ("dps", c_uint8),
        ("nmic", c_uint8),
        ("rescap", c_uint8),
        ("fpi", c_uint8),
        ("dlfeat", c_uint8),
        ("nawun", c_uint16),
        ("nawupf", c_uint16),
        ("nacwu", c_uint16),
        ("nabsn", c_uint16),
        ("nabo", c_uint16),
        ("nabspf", c_uint16),
        ("noiob", c_uint16),
        ("nvmcap", c_uint128),
        ("npwg", c_uint16),
        ("npwa", c_uint16),
        ("npdg", c_uint16),
        ("npda", c_uint16),
        ("nows", c_uint16),
        ("_rsvd74", c_uint8 * 18),
        ("anagrpid", c_uint32),
        ("_rsvd96", c_uint8 * 3),
        ("nsattr", c_uint8),
        ("nvmsetid", c_uint16),
        ("endgid", c_uint16),
        ("nguid", c_uint128),
        ("eui64", c_uint64),
        ("lbafs", LbaFormat * 16),
        ("_rsvd192", c_uint8 * 192),
        ("vendor_specific", c_uint8 * 3712),
    ]
