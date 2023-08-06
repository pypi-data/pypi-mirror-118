"""Definition of driver plugin API."""

from abc import ABC, abstractmethod
from ctypes import sizeof
from typing import Any, AsyncIterator, Iterable, Optional, Union

from nvme import Cmd, IdCtrl, IdNmsp, StatusField

Buffer = Any
"""The type of a `Driver`'s buffer.

This is currently just a type alias for `Any`. If it is [ever
added][typing-buffer] to the `typing` module, then this will be a type
annotation for an object that conforms to the [buffer
protocol][buffer-protocol].

[typing-buffer]: https://github.com/python/typing/issues/593
[buffer-protocol]: https://docs.python.org/3/c-api/buffer.html#bufferobjects
"""


class Controller(ABC):
    """The expected behavior of a driver's controller objects."""

    @abstractmethod
    def close(self):
        """Close the controller and deallocate associated resources."""

    def __enter__(self) -> "Controller":
        """Open the controller so commands can be sent to it.

        Drivers may optionally return open controllers from `Driver.scan`, so this
        may or may not actually do anything.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the controller.

        Further commands sent to this controller have undefined behavior.
        """
        self.close()


class Namespace(ABC):
    """The expected behavior of a driver's namespace objects."""

    @abstractmethod
    def close(self):
        """Close the namespace and deallocate associated resources."""

    def __enter__(self) -> "Controller":
        """Open the namespace so commands can be sent to it.

        Drivers may optionally return open controllers from `Driver.scan`, so this
        may or may not actually do anything.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the namespace.

        Further commands sent to this namespace have undefined behavior.
        """
        self.close()


class Driver(ABC):
    """Abstract behavior of an NVMe driver.

    Drivers may override the async functions in order to provide an actually async
    implementation. By default, all of the async functions merely call the synchronous
    variants.
    """

    # TODO: Define AEN interface.
    # TODO: Define metadata buffer API.
    # TODO: How to model qpair's SPDK without overcomplicating the kernel drivers?

    def __init__(self, **kwargs):
        """Initialize with arbitrary kwargs as config."""
        pass

    @abstractmethod
    def scan(self) -> Iterable[Controller]:
        """Discover NVMe controllers and produce an iterator of `Controller`'s."""

    @abstractmethod
    def namespaces(self, ctrlr: Controller) -> Iterable[Namespace]:
        """Discover NVMe namespaces *attached* to the given controller."""

    @abstractmethod
    def new_buffer(self, size: int, ctrlr: Optional[Controller] = None) -> Buffer:
        """Create a buffer specific to this driver which conforms to the buffer protocol.

        If a controller is provided, then the driver should make a best effort to
        utilize controller memory for the buffer.
        """

    @abstractmethod
    def admin(
        self, ctrlr: Controller, cmd: Cmd, buffer: Optional[Buffer] = None
    ) -> StatusField:
        """Issue an admin command synchronously.

        The provided command does not need to fill in the data pointer or
        metadata pointer.
        """

    @abstractmethod
    def nvm(
        self,
        device: Union[Namespace, Controller],
        cmd: Cmd,
        buffer: Optional[Buffer] = None,
    ) -> StatusField:
        """Issue a NVM command synchronously.

        The provided command does not need to fill in the data pointer or
        metadata pointer. If `device` is a `Namespace`, then the provided
        command does not need to fill in the `Cmd.nsid` field. If `device` is a
        `Controller`, then a namespace with `cmd`'s nsid must exist and be
        attached to the controller.
        """

    # The following methods are convenience methods for issuing either admin or
    # nvm commands. Having to define both a sync and async interface to these is
    # rather verbose, but the alternative of dynamic method dispatch would be
    # more confusing for documentation. So, I'm accepting the verbosity for now.

    def write(self, nmsp: Namespace, lba: int, nlb: int, buffer: Buffer) -> StatusField:
        """Issue a NVM write command.

        Args:
            nmsp: The namespace to which to write.
            lba: The logical block address to which to write.
            nlb: 0 based number of logical blocks which should be written from
                `buffer`. Ensure this does not overflow the buffer.
            buffer: The data which should be written.
        """
        return self.nvm(nmsp, Cmd(cdw0=1, cdw11=lba, cdw12=nlb), buffer)

    def read(self, nmsp: Namespace, lba: int, nlb: int, buffer: Buffer) -> StatusField:
        """Issue a NVM read command.

        Args:
            nmsp: The namespace from which to read.
            lba: The logical block address to which to read.
            nlb: 0 based number of logical blocks which should be written from
                `buffer`. Ensure this does not overflow the buffer.
            buffer: The data which should be written.
        """
        return self.nvm(nmsp, Cmd(cdw0=2, cdw11=lba, cdw12=nlb), buffer)

    def id_ctrlr(self, ctrlr: Controller, buffer: Buffer) -> IdCtrl:
        """Iusse an identify controller command.

        This will copy the structure from the given buffer.

        Raises:
            NvmeError - The identify command returned an unsuccessful status code field.
            ValueError - The given buffer has insufficient capacity.
        """
        if sizeof(IdCtrl) > len(buffer):
            raise ValueError(f"{buffer} has insufficent capacity to contain {IdCtrl}")
        self.admin(ctrlr, Cmd(cdw0=6, cdw10=1), buffer).check()
        return IdCtrl.from_buffer_copy(buffer)

    def id_ns(self, ns: Namespace, buffer: Buffer) -> IdNmsp:
        """Issue an identify namespace command.

        This will copy the structure from the given buffer.

        Raises:
            NvmeError - The identify command returned an unsuccessful status code field.
            ValueError - The given buffer has insufficient capacity.
        """
        if sizeof(IdNmsp) > len(buffer):
            raise ValueError(f"{buffer} has insufficent capacity to contain {IdNmsp}")
        self.admin(ns, Cmd(cdw0=6), buffer).check()
        return IdNmsp.from_buffer_copy(buffer)

    async def ascan(self) -> AsyncIterator[Controller]:
        """Discover NVMe controllers and produce an iterator of `Controller`'s."""
        for ctrlr in self.scan():
            yield ctrlr

    async def anamespaces(self, ctrlr: Controller) -> AsyncIterator[Namespace]:
        """Discover NVMe namespaces *attached* to the given controller."""
        for ns in self.namespaces(ctrlr):
            yield ns

    async def aadmin(
        self, ctrlr: Controller, cmd: Cmd, buffer: Optional[Buffer] = None
    ) -> StatusField:
        """Issue an admin command."""
        return self.admin(ctrlr, cmd, buffer)

    async def anvm(
        self,
        nmsp: Union[Namespace, Controller],
        cmd: Cmd,
        buffer: Optional[Buffer] = None,
    ) -> StatusField:
        """Issue an NVM command.

        The provided command does not need to fill in the data pointer or
        metadata pointer. If `device` is a `Namespace`, then the provided
        command does not need to fill in the `Cmd.nsid` field. If `device` is a
        `Controller`, then a namespace with `cmd`'s nsid must exist and be
        attached to the controller.
        """
        return self.nvm(nmsp, cmd, buffer)

    async def awrite(
        self, nmsp: Namespace, lba: int, nlb: int, buffer: Buffer
    ) -> StatusField:
        """Issue a NVM write command.

        Args:
            nmsp: The namespace to which to write.
            lba: The logical block address to which to write.
            nlb: 0 based number of logical blocks which should be written from
                `buffer`. Ensure this does not overflow the buffer.
            buffer: The data which should be written.
        """
        return await self.anvm(nmsp, Cmd(cdw=1, cdw11=lba, cdw12=nlb), buffer)

    async def aread(
        self, nmsp: Namespace, lba: int, nlb: int, buffer: Buffer
    ) -> StatusField:
        """Issue a NVM read command.

        Args:
            nmsp: The namespace from which to read.
            lba: The logical block address to which to read.
            nlb: 0 based number of logical blocks which should be written from
                `buffer`. Ensure this does not overflow the buffer.
            buffer: The data which should be written.
        """
        return await self.anvm(nmsp, Cmd(cdw=2, cdw11=lba, cdw12=nlb), buffer)

    async def aid_ctrlr(self, ctrlr: Controller, buffer: Buffer) -> StatusField:
        """Iusse an identify controller command."""
        return await self.aadmin(ctrlr, Cmd(cdw0=6, cdw10=1), buffer)

    async def aid_ns(self, ns: Namespace, buffer: Buffer) -> StatusField:
        """Issue an identify namespace command."""
        return await self.aadmin(ns, Cmd(cdw0=6), buffer)
