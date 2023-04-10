import msgpack
import time
from serialization_module.base_serializer import BaseSerializer


class MessagePackSerializer(BaseSerializer):
    def get_serialization_method(self):
        return 'MessagePack'

    def serialize(self, msg: object):
        start_time = time.time()
        serialized = msgpack.packb(msg)
        execution_time = time.time() - start_time
        return serialized, execution_time

    def deserialize(self, msg: str):
        start_time = time.time()
        deserialized = msgpack.unpackb(msg)
        execution_time = time.time() - start_time
        return deserialized, execution_time
