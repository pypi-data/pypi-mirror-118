import logging
from typing import IO, Union

import requests

from .enums import FileType

logger = logging.getLogger(__name__)


def download(url: str, file: 'IO'):
    """
    Download file.

    Args:
        url:
            URL

        file:
            IO object
    """
    res = requests.get(url, stream=True)
    res.raise_for_status()
    file.write(res.content)


def upload(file: Union[IO, str], url: str, filetype: 'FileType'):
    """
    Upload file.

    Args:
        file:
            IO object or path to file

        url:
            URL
    """
    file_object: IO
    if isinstance(file, str):
        file_object = open(file, 'rb')
    else:
        file_object = file
    headers = {
        "Content-Type": filetype.value,
    }
    res = requests.put(url, headers=headers, data=file_object)
    res.raise_for_status()
