from abc import ABC, abstractmethod


class AbstractServerlessManager(ABC):

    @abstractmethod
    def invoke_function(self, function_path: str, payload: dict) -> dict:
        pass
