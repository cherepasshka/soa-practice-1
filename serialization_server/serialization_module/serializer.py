from serialization_module.msgpack_serializer import MessagePackSerializer
from serialization_module.json_serializer import JsonSerializer
from serialization_module.base_serializer import BaseSerializer


def create_serializer(serialization_method: str) -> BaseSerializer:
    return mapping[serialization_method]()


mapping = {
    'JSON': JsonSerializer,
    'MessagePack': MessagePackSerializer,
}
