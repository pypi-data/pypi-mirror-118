import logging
import os
import re
import traceback
from http import HTTPStatus

import requests

from pencilpycommons.storage.exceptions import FileDownloadException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("storage")


def get_file_extension(filename: str):
    return os.path.splitext(filename)[1]


def delete_file(file_path: str):
    try:
        os.remove(file_path)
    except OSError:
        logger.warning("file {} does not exist. Cannot delete.".format(file_path))


def get_cloudfront_key(url: str):
    try:
        match = re.search('^https?://([^.]+).cloudfront.net/(.*?)$', url.split('?')[0])
    except Exception as e:
        logger.warning(f'Failed parsing s3 url: {url}; error: {str(e)}')
        return None

    return {
        "cloudfrontKey": match.group(1),
        "s3Key": match.group(2)
    }


def download_file(url: str, file_path: str):
    try:
        r = requests.get(url, allow_redirects=True)
    except Exception:
        raise FileDownloadException("error downloading file from url {}: {}".format(url, traceback.format_exc()), 0)

    if r.status_code != HTTPStatus.OK:
        raise FileDownloadException(r.content, r.status_code)

    with open(file_path, 'wb') as file:
        file.write(r.content)
        file.close()
