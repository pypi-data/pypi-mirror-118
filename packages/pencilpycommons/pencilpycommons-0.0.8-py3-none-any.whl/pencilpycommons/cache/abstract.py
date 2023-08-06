from abc import abstractmethod, ABC
from typing import List


class AbstractCacheClient(ABC):

    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def set(self, key: str, value, ttl=None):
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        pass

    @abstractmethod
    def delete(self, key: str):
        pass

    @abstractmethod
    def keys(self, pattern: str) -> List[str]:
        pass

    @abstractmethod
    def set_if_not_exists(self, key: str, value):
        pass

    @abstractmethod
    def set_ttl(self, key: str, ttl):
        pass

    @abstractmethod
    def increment_value_by(self, key: str, amount: int) -> int:
        pass

    @abstractmethod
    def decrement_value_by(self, key: str, amount: int) -> int:
        pass

    @abstractmethod
    def push_to_list_head(self, key: str, *values):
        pass

    @abstractmethod
    def push_to_list_end(self, key: str, *values):
        pass

    @abstractmethod
    def pop_from_list_end(self, key: str):
        pass

    @abstractmethod
    def pop_from_list_head(self, key: str):
        pass
