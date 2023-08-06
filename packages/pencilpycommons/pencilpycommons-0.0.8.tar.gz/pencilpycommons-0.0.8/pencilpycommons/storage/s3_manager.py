import logging
import mimetypes
import os
import re
import tempfile
import uuid

from botocore.exceptions import ClientError

from pencilpycommons.storage.abstract import AbstractStorageManager
from pencilpycommons.storage.utils import delete_file, get_file_extension

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger("aws")


class S3Manager(AbstractStorageManager):

    def __init__(self, s3_client, ground_truth_bucket=None):
        self.__s3_client = s3_client
        self.__ground_truth_bucket = ground_truth_bucket

    def __get_s3_client(self):
        return self.__s3_client

    def get_objects(self, key, bucket: str, limit=1000, continuation_token=None) -> list:
        results = self.__get_objects(key, bucket, limit, continuation_token)
        if len(results) > 0:
            return results

        if not self.__ground_truth_bucket:
            return results

        # If no objects are found in requested bucket, try the ground truth bucket
        return self.__get_objects(key, self.__ground_truth_bucket, limit, continuation_token)

    def __get_objects(self, key, bucket: str, limit: int, continuation_token) -> list:
        client = self.__get_s3_client()

        if continuation_token:
            results = client.list_objects_v2(Bucket=bucket, Prefix=key, MaxKeys=limit,
                                             ContinuationToken=continuation_token)
        else:
            results = client.list_objects_v2(Bucket=bucket, Prefix=key, MaxKeys=limit)

        if not results:
            results = list()

        return results

    def upload(self, filename: str, bucket: str, key=None, public=False) -> str:
        if not os.path.exists(filename):
            raise FileNotFoundError(filename)

        content_type = mimetypes.MimeTypes().guess_type(filename)[0]
        if key is None:
            key = str(uuid.uuid4()) + get_file_extension(filename)

        extra_args = dict()
        if content_type is not None:
            extra_args['ContentType'] = content_type
        if public is True:
            extra_args['ACL'] = 'public-read'

        self.__get_s3_client().upload_file(filename, bucket, key, ExtraArgs=extra_args)
        _logger.debug("Uploaded %s to %s with key: %s", filename, bucket, key)

        return key

    def key_exists(self, bucket: str, key: str) -> bool:
        if not bucket:
            return False

        if self.__key_exists(bucket, key):
            return True

        if not self.__ground_truth_bucket:
            return False

        # If key does not exist in requested bucket, try the ground truth bucket
        return self.__key_exists(self.__ground_truth_bucket, key)

    def __key_exists(self, bucket: str, key: str) -> bool:
        try:
            self.__get_s3_client().head_object(Bucket=bucket, Key=key)
        except ClientError as e:
            _logger.debug(e, exc_info=True)
            return False
        except Exception as e:  # pylint: disable=broad-except
            _logger.debug(e, exc_info=True)
            return False

        return True

    def copy_object(self, bucket: str, key: str, new_bucket_name: str, new_key: str):
        self.__get_s3_client().copy_object(Bucket=new_bucket_name, Key=new_key, CopySource=f'{bucket}/{key}',
                                           ACL='public-read')

    def download(self, bucket: str, key: str, filename=None):
        _logger.debug("download_from_s3")
        client = self.__get_s3_client()

        if not self.key_exists(bucket, key):

            # If key does not exist in both buckets
            if not self.key_exists(self.__ground_truth_bucket, key):
                raise RuntimeError("Bucket: {0} does not contain specified key: {1}".format(
                    bucket, key
                ))

            # If key exists in ground truth bucket but not the requested bucket, copy it over
            self.copy_object(self.__ground_truth_bucket, key, bucket, key)

        suffix = key.split('.')[-1]
        if filename is None:
            if len(key.split('.')) == 1:
                filename = self.__get_temporary_filename('')
            else:
                filename = self.__get_temporary_filename(suffix='.' + suffix)

        client.download_file(bucket, key, filename)
        _logger.debug("Downloaded to: {0}".format(filename))

        return filename

    def generate_pre_signed_url(self, bucket: str, key: str) -> str:
        return self.__get_s3_client().generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': bucket,
                'Key': key
            }
        )

    def get_public_url(self, bucket: str, key: str) -> str:
        return f'https://{bucket}.s3.amazonaws.com/{key}'

    def get_key_info(self, url: str) -> dict:
        try:
            pattern = re.compile(r'https://(?P<s3_bucket>.*).s3.(?P<region>.*).*amazonaws.com/(?P<s3_key>.*)')
            match = pattern.match(url.split('?')[0])
            region = ""

            if match.group('region'):
                region = match.group('region') if match.group('region')[-1] != '.' else match.group('region')[:-1]

        except Exception as e:
            _logger.debug(f'Failed parsing s3 url: {url}; error: {str(e)}')
            return dict()

        return {
            'key': match.group('s3_key'),
            'bucket': match.group('s3_bucket'),
            'region': region
        }

    def __get_temporary_filename(self, suffix=''):
        fd, out_filename = tempfile.mkstemp(suffix=suffix)
        os.close(fd)
        delete_file(out_filename)

        return out_filename
