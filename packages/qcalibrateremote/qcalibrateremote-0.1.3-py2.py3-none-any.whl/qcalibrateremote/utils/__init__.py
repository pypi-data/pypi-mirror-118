from typing import Union

from .buffer import QueueBuffer

def bytes_or_read_file(bytes_or_file: Union[bytes, str]) -> bytes:
    if type(bytes_or_file) is str:
        with open(bytes_or_file, 'rb') as fh:
            return fh.read()
    elif type(bytes_or_file) is bytes:
        return bytes_or_file
    else:
        raise TypeError(f'Expected bytes or string, got {type(bytes_or_file)}')

__all__ = [bytes_or_read_file, QueueBuffer]