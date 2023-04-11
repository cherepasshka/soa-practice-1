from serialization_module.base_serializer import BaseSerializer
from serialization_module.msgpack_serializer import MessagePackSerializer
from serialization_module.json_serializer import JsonSerializer
from serialization_module.native_serializer import NativeSerializer
from serialization_module.yaml_serializer import YamlSerializer
from serialization_module.xml_serializer import XmlSerializer
from serialization_module.avro_serializer import AvroSerializer
from serialization_module.protobuf_serializer import ProtobufSerializer


def create_serializer(serialization_method: str) -> BaseSerializer:
    if serialization_method not in mapping.keys():
        raise NameError('Invalid serialization method', serialization_method)
    return mapping[serialization_method]()


mapping = {
    'JSON': JsonSerializer,
    'MessagePack': MessagePackSerializer,
    'Native': NativeSerializer,
    'YAML': YamlSerializer,
    'XML': XmlSerializer,
    'AVRO': AvroSerializer,
    'PROTO': ProtobufSerializer,
}
