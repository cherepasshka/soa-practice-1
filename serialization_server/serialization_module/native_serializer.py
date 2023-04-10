import pickle
import time
from serialization_module.base_serializer import BaseSerializer


class NativeSerializer(BaseSerializer):
    def get_serialization_method(self):
        return 'Pickle - python native'

    def serialize(self, msg: object):
        start_time = time.time()
        serialized = pickle.dumps(msg)
        execution_time = time.time() - start_time
        return serialized, execution_time

    def deserialize(self, msg: str):
        start_time = time.time()
        deserialized = pickle.loads(msg)
        execution_time = time.time() - start_time
        return deserialized, execution_time
