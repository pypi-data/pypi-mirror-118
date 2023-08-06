from abc import abstractmethod, ABC


class AbstractStorageManager(ABC):

    @abstractmethod
    def get_objects(self, key, bucket: str, limit=1000, continuation_token=None) -> list:
        pass

    @abstractmethod
    def upload(self, filename: str, bucket: str, key=None, public=False) -> str:
        pass

    @abstractmethod
    def key_exists(self, bucket: str, key: str) -> bool:
        pass

    @abstractmethod
    def copy_object(self, bucket: str, key: str, new_bucket_name: str, new_key: str):
        pass

    @abstractmethod
    def download(self, bucket: str, key: str, filename=None):
        pass

    @abstractmethod
    def generate_pre_signed_url(self, bucket: str, key: str) -> str:
        pass

    @abstractmethod
    def get_public_url(self, bucket: str, key: str) -> str:
        pass

    @abstractmethod
    def get_key_info(self, url: str) -> dict:
        pass
