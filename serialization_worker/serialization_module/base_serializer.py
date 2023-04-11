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

    def convert_to_ms(self, seconds):
        return round(seconds * 1000, 3)

    def get_info(self, msg: object):
        serialized, serialization_time = self.serialize(msg)
        deserealized, deserialization_time = self.deserialize(serialized)
        return f'Method: {self.get_serialization_method()}\n' + \
            f'Original size: {self.get_message_size(msg)} bytes\n' + \
            f'Serialized size: {self.get_message_size(serialized)} bytes\n' + \
            f'Serialization time: {convert_to_ms(serialization_time)}ms\n' + \
            f'Deserialization time:{convert_to_ms(deserialization_time)}ms\n'


def convert_to_ms(seconds: float):
    return round(seconds * 1000, 3)
