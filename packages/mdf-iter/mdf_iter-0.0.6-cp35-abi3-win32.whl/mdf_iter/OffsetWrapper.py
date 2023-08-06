import io

from typing import Optional

from mdf_iter.IFileInterface import IFileInterface


class OffsetWrapperIFileInterface(io.RawIOBase):
    def __init__(self, wrapped: IFileInterface, offset: int):
        self._wrapped = wrapped
        self._offset = offset
        self.seek(0)
        return

    def read(self, size: int = 0) -> Optional[bytes]:
        buffer = bytearray(size)

        bytes_read = self._wrapped.read(buffer, size)

        if bytes_read == 0:
            buffer = None
        else:
            buffer = bytes(buffer[:bytes_read])

        return buffer

    def seek(self, offset: int, whence: int = 0) -> int:
        return self._wrapped.seek(offset + self._offset, whence)

    def tell(self) -> int:
        return self._wrapped.tell() - self._offset

    def readable(self) -> bool:
        return True

    def seekable(self) -> bool:
        return True

    pass
