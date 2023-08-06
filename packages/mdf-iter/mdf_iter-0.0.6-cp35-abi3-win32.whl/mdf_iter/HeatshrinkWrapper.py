import io

from typing import Optional

from mdf_iter.IFileInterface import IFileInterface
from mdf_iter.OffsetWrapper import OffsetWrapperIFileInterface


class HeatshrinkWrapper(IFileInterface):
    def __init__(self, wrapped: IFileInterface):
        # Read the header
        header = bytearray(28)
        wrapped.seek(0)
        bytes_read = wrapped.read(header, len(header))

        if bytes_read != len(header):
            raise RuntimeError("Not enough header bytes")

        if header[:12] != b"Generic File":
            # Assume it is a plain MDF file
            self._wrapped = wrapped
        else:
            # Extract parameters
            lookahead = int.from_bytes(header[-8:-4], "big")
            window_size = int.from_bytes(header[-4:], "big")

            if window_size == 256:
                window_size = 8
            elif window_size == 512:
                window_size = 9
            elif window_size == 1024:
                window_size = 10

            # Create heatshrink file
            import heatshrink2
            self._wrapped = heatshrink2.HeatshrinkFile(OffsetWrapperIFileInterface(wrapped, 28), window_sz2=window_size, lookahead_sz2=lookahead)

            pass
        return

    def read(self, buffer: bytearray, number_of_bytes: int):
        read_data = self._wrapped.read(number_of_bytes)
        buffer[:len(read_data)] = read_data

        return len(read_data)

    def seek(self, offset: int, whence: int = 0) -> int:
        return self._wrapped.seek(offset, whence)

    pass
