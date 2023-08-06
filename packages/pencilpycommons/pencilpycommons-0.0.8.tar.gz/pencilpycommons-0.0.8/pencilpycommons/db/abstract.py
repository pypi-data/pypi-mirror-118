from abc import ABC, abstractmethod


class AbstractDBClient(ABC):

    @abstractmethod
    def get_connection(self, db_name: str, force_new=False):
        pass

    @abstractmethod
    def close_connection(self, db_name: str):
        pass


class AbstractDocumentDBClient(ABC):

    @abstractmethod
    def query_using_index(self, table_name: str, index_name: str, value):
        pass

    @abstractmethod
    def query_with_attribute(self, table_name: str, attr_name: str, value):
        pass

    @abstractmethod
    def query_using_attribute_and_operator(self, table_name: str, attr_name: str, operator: str, value):
        pass
