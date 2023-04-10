import json
import time
from serialization_module.serializer import Serializer


class JsonSerializer(Serializer):
    def get_serialization_method(self):
        return 'JSON'

    def serialize(self, msg: object):
        start_time = time.time()
        serialized = json.dumps(msg)
        execution_time = time.time() - start_time
        return serialized, execution_time

    def deserialize(self, msg: str):
        start_time = time.time()
        deserialized = json.loads(msg)
        execution_time = time.time() - start_time
        return deserialized, execution_time
