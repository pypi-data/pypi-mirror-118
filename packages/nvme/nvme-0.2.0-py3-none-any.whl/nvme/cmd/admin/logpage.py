"""Get log page command data structures.

Reference: NVM Express Revision 1.4c, Section 5.14.1
"""

from ctypes import LittleEndianStructure, c_char, c_uint8, c_uint16, c_uint32, c_uint64

from nvme.util import c_uint128


class ParameterErrorLocation(LittleEndianStructure):
    """The parameter location of an error log entry."""

    _pack_ = 1
    _fields_ = [
        ("byte", c_uint8, 8),
        ("bit", c_uint8, 3),
        ("_rsvd", c_uint8, 5),
    ]


class ErrorLogEntry(LittleEndianStructure):
    """An error log entry.

    Reference: NVM Express Revsion 1.4c, Section 5.14.1.1, Figure 197
    """

    _pack_ = 1
    _fields_ = [
        ("err_count", c_uint64),
        ("subqid", c_uint16),
        ("cmd_id", c_uint16),
        ("status", c_uint16),
        ("location", ParameterErrorLocation),
        ("lba", c_uint64),
        ("namespace", c_uint32),
        ("vendor_specific", c_uint8),
        ("trtype", c_uint8),
        ("_rsvd30", c_uint16),
        ("cmd_specific", c_uint64),
        ("trtype_specific", c_uint16),
        ("_rsvd42", c_uint8 * 22),
    ]


class SmartLog(LittleEndianStructure):
    """The SMART / health information log.

    Reference: NVM Express Revision 1.4c, Section 5.14.1.2, Figure 198
    """

    _pack_ = 1
    _fields_ = [
        ("crit_warning", c_uint8),
        ("comp_temp", c_uint16),
        ("avail_spare", c_uint8),
        ("avail_spare_thresh", c_uint8),
        ("percent_used", c_uint8),
        ("endur_grp_crit_warning", c_uint8),
        ("_rsvd7", c_uint8 * 25),
        ("data_units_read", c_uint128),
        ("data_units_written", c_uint128),
        ("host_read_cmds", c_uint128),
        ("host_write_cmds", c_uint128),
        ("ctrl_busy_time", c_uint128),
        ("pwr_cycles", c_uint128),
        ("pwr_on_hrs", c_uint128),
        ("unsafe_shutdowns", c_uint128),
        ("mad_integrity_errs", c_uint128),
        ("num_err_log_entries", c_uint128),
        ("warning_comp_temp_time", c_uint32),
        ("crit_comp_temp_time", c_uint32),
        ("temp_sensors", c_uint16 * 8),
        ("therm_mgmt_temp_transition_cnts", c_uint32 * 2),
        ("total_time_therm_mgmt_temp", c_uint32 * 2),
        ("_rsvd232", c_uint8 * 280),
    ]


class FwSlotLog(LittleEndianStructure):
    """The firmware slot information log.

    Reference: NVM Express Revision 1.4c, Section 5.14.1.3, Figure 200
    """

    _pack_ = 1
    _fields_ = [
        ("afi", c_uint8),
        ("_rsvd1", c_uint8 * 7),
        ("frss", (c_char * 8) * 7),
        ("_rsvd64", c_uint8 * 448),
    ]
