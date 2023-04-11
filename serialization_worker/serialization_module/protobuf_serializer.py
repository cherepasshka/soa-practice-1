import serialization_module.schemas.proto_scheme_pb2 as scheme
import time
from serialization_module.base_serializer import BaseSerializer


class ProtobufSerializer(BaseSerializer):
    def get_serialization_method(self):
        return 'Proto'

    def __get_key(self, m: dict, key):
        if key in m.keys():
            return m[key]
        return None

    def serialize(self, msg: object):
        m = scheme.Data(int=self.__get_key(msg, 'int'),
                        float=self.__get_key(msg, 'float'),
                        list_str=self.__get_key(msg, 'list_str'),
                        list_int=self.__get_key(msg, 'list_int'),
                        list_float=self.__get_key(msg, 'list_float'),
                        dict=self.__get_key(msg, 'dict'))
        start_time = time.time()
        serialized = m.SerializeToString()
        execution_time = time.time() - start_time
        return serialized, execution_time

    def deserialize(self, msg: str):
        data = scheme.Data()
        start_time = time.time()
        data.ParseFromString(msg)
        execution_time = time.time() - start_time
        deserialized = {}
        for key in scheme.Data.__dict__.keys():
            if key.startswith('__') or key[0].isupper():
                continue
            deserialized[key] = getattr(data, key)
        return deserialized, execution_time
