from xml_marshaller import xml_marshaller
import time
from serialization_module.base_serializer import BaseSerializer


class XmlSerializer(BaseSerializer):
    def get_serialization_method(self):
        return 'XML'

    def serialize(self, msg: object):
        start_time = time.time()
        serialized = xml_marshaller.dumps(msg)
        execution_time = time.time() - start_time
        return serialized, execution_time

    def deserialize(self, msg: str):
        start_time = time.time()
        deserialized = xml_marshaller.loads(msg)
        execution_time = time.time() - start_time
        return deserialized, execution_time
