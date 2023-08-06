"""`nvme.Driver` implementation using the Linux builtin NVMe driver."""

import os
from ctypes import (
    LittleEndianStructure,
    addressof,
    c_uint8,
    c_uint16,
    c_uint32,
    c_uint64,
    create_string_buffer,
)
from dataclasses import dataclass
from fcntl import ioctl
from pathlib import Path
from typing import BinaryIO, Iterable, Iterator, Optional, Union

from nvme import Buffer, Cmd, Controller, Driver, Namespace, StatusField

NVME_IOCTL_ADMIN_CMD = 0xC0484E41
NVME_IOCTL_IO_CMD = 0xC0484E43


@dataclass
class LinuxController(Controller):
    """A controller for use with `LinuxIoctlDriver`."""

    fd: Optional[BinaryIO]
    sysfs: Path

    def close(self):
        """Close the underlying file handle."""
        if self.fd is not None:
            self.fd.close()
            self.fd = None


@dataclass
class LinuxNamespace(Namespace):
    """A namespace for use with `LinuxIoctlDriver`."""

    fd: Optional[BinaryIO]
    sysfs: Path
    nsid: int

    def close(self):
        """Close the underlying file handle."""
        if self.fd is not None:
            self.fd.close()
            self.fd = None


class LinuxIoctlDriver(Driver):
    """Issue NVMe commands using the Linux builtin NVMe driver."""

    def scan(self) -> Iterable[LinuxController]:
        """Return open `Device` objects for every viable device."""
        devs = []
        for root, dirs, files in os.walk("/sys/devices"):
            root_path = Path(root)
            if root_path.name == "nvme":
                for d in dirs:
                    fd = open(Path("/dev", d), "rb", buffering=0)
                    dev = LinuxController(fd, root_path.joinpath(d))
                    devs.append(dev)
        return devs

    def namespaces(self, ctrlr: LinuxController) -> Iterable[LinuxNamespace]:
        """Return open `Namespace` objects for every attached namespace on `device`."""
        nses = []
        for path in self._ns_sysfs(ctrlr.sysfs):
            fd = open(Path("/dev", path.name), "rb", buffering=0)
            with path.joinpath("nsid").open() as fh:
                nsid = int(fh.read().strip())
            ns = LinuxNamespace(fd, path, nsid)
            nses.append(ns)
        return nses

    def new_buffer(self, size: int, ctrlr: Optional[LinuxController] = None) -> Buffer:
        """Create a new buffer for issuing commands.

        This driver is incapable of creating buffers on controller memory, so
        device is unused.
        """
        return create_string_buffer(size)

    def admin(
        self, ctrlr: Controller, cmd: Cmd, buffer: Optional[Buffer] = None
    ) -> StatusField:
        """Issue and admin command."""
        ioctl_cmd = IoctlCmd.from_sqe(cmd, buffer)
        ioctl(ctrlr.fd, NVME_IOCTL_ADMIN_CMD, ioctl_cmd)
        return StatusField(ioctl_cmd.result)

    def nvm(
        self,
        device: Union[LinuxNamespace, LinuxController],
        cmd: Cmd,
        buffer: Optional[Buffer] = None,
    ) -> StatusField:
        """Issue an I/O command."""
        if isinstance(device, LinuxController):
            nsid_to_dev = {}
            for path in self._ns_sysfs(device.sysfs):
                with path.joinpath("nsid").open() as fh:
                    nsid = int(fh.read().strip())
                    nsid_to_dev[nsid] = Path("/dev").join(path.name)
            dev_fd = open(nsid_to_dev[cmd.nsid], "rb", buffering=0)
        else:
            dev_fd = device.fd
            cmd.nsid = device.nsid
        ioctl_cmd = IoctlCmd.from_sqe(cmd, buffer)
        ioctl(dev_fd, NVME_IOCTL_IO_CMD, ioctl_cmd)
        return StatusField(ioctl_cmd.result)

    @classmethod
    def _ns_sysfs(cls, ctrlr: Path) -> Iterator[Path]:
        for child in ctrlr.iterdir():
            if child.name.startswith(ctrlr.name):
                yield child


class IoctlCmd(LittleEndianStructure):
    """Linux nvme driver's command structure.

    This deviates slightly from the NVMe spec's submission queue structure and
    must be translated by this driver implementation.
    """

    _pack_ = 1
    _fields_ = [
        ("opcode", c_uint8),
        ("flags", c_uint8),
        ("rsvd1", c_uint16),
        ("nsid", c_uint32),
        ("cdw2", c_uint32),
        ("cdw3", c_uint32),
        ("metadata", c_uint64),
        ("addr", c_uint64),
        ("metadata_len", c_uint32),
        ("data_len", c_uint32),
        ("cdw10", c_uint32),
        ("cdw11", c_uint32),
        ("cdw12", c_uint32),
        ("cdw13", c_uint32),
        ("cdw14", c_uint32),
        ("cdw15", c_uint32),
        ("timeout_ms", c_uint32),
        ("result", c_uint32),
    ]

    @classmethod
    def from_sqe(cls, cmd: Cmd, buffer: Optional[Buffer]) -> "IoctlCmd":
        """Create an `IoctlCmd` from a `nvme.Cmd`."""
        return cls(
            opcode=cmd.cdw0 & 0xFF,
            flags=cmd.cdw0 >> 8 & 0xFF,
            rsvd1=cmd.cdw0 >> 16 & 0xFFFF,
            nsid=cmd.nsid,
            cdw2=cmd.cdw2,
            cdw3=cmd.cdw3,
            metadata=cmd.mptr,
            addr=addressof(buffer) if buffer is not None else 0,
            metadata_len=0,
            data_len=len(buffer),
            cdw10=cmd.cdw10,
            cdw11=cmd.cdw11,
            cdw12=cmd.cdw12,
            cdw13=cmd.cdw13,
            cdw14=cmd.cdw14,
            cdw15=cmd.cdw15,
            timeout_ms=0,
            result=0,
        )

    def __str__(self) -> str:
        """Print the command in the same format as nvme-cli."""
        return f"""opcode       : {self.opcode:02x}
flags        : {self.flags:02x}
rsvd1        : {self.rsvd1:04x}
nsid         : {self.nsid:08x}
cdw2         : {self.cdw2:08x}
cdw3         : {self.cdw3:08x}
data_len     : {self.data_len:08x}
metadata_len : {self.metadata_len:08x}
addr         : {self.addr:016x}
metadata     : {self.metadata:016x}
cdw10        : {self.cdw10:08x}
cdw11        : {self.cdw11:08x}
cdw12        : {self.cdw12:08x}
cdw13        : {self.cdw13:08x}
cdw14        : {self.cdw14:08x}
cdw15        : {self.cdw15:08x}
timeout_ms   : {self.timeout_ms:08x}"""
