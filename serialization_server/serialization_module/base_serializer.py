from abc import ABC, abstractmethod
import sys


class BaseSerializer(ABC):
    @abstractmethod
    def get_serialization_method(self):
        pass

    @abstractmethod
    def serialize(self, msg: object):
        pass

    @abstractmethod
    def deserialize(self, msg: object):
        pass

    def get_message_size(self, msg: str):
        return sys.getsizeof(msg)

    def get_info(self, msg: object):
        serialized, serialization_time = self.serialize(msg)
        deserealized, deserialization_time = self.deserialize(serialized)
        assert (deserealized == msg)
        return f'Method: {self.get_serialization_method()}\n' + \
            f'Size: {self.get_message_size(msg)} bytes\n' + \
            f'Serialization time: {serialization_time}\n' + \
            f'Deserialization time:{deserialization_time}\n'
