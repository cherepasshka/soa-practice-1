import yaml
import time
from serialization_module.base_serializer import BaseSerializer


class YamlSerializer(BaseSerializer):
    def get_serialization_method(self):
        return 'YAML'

    def serialize(self, msg: object):
        start_time = time.time()
        serialized = yaml.dump(msg)
        execution_time = time.time() - start_time
        return serialized, execution_time

    def deserialize(self, msg: str):
        start_time = time.time()
        deserialized = yaml.load(msg, Loader=yaml.FullLoader)
        execution_time = time.time() - start_time
        return deserialized, execution_time
