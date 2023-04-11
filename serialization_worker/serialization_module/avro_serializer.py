import avro.schema
import avro.io
import io
import time
from serialization_module.base_serializer import BaseSerializer


class AvroSerializer(BaseSerializer):
    def __init__(self) -> None:
        super().__init__()
        with open("serialization_module/schemas/avro_schema.avsc", "rb") as f:
            self.schema = avro.schema.parse(f.read())

    def get_serialization_method(self):
        return 'Avro'

    def serialize(self, msg: object):
        writer = avro.io.DatumWriter(self.schema)
        bytes_writer = io.BytesIO()
        encoder = avro.io.BinaryEncoder(bytes_writer)
        start_time = time.time()
        writer.write(msg, encoder)
        serialized = bytes_writer.getvalue()
        execution_time = time.time() - start_time
        return serialized, execution_time

    def deserialize(self, msg: str):
        reader = avro.io.DatumReader(self.schema)
        bytes_reader = io.BytesIO(msg)
        start_time = time.time()
        decoder = avro.io.BinaryDecoder(bytes_reader)
        deserialized = reader.read(decoder)  # produces dict
        execution_time = time.time() - start_time
        keys_to_romove = []
        for key in deserialized.keys():
            if deserialized[key] is None:
                keys_to_romove.append(key)
        for key in keys_to_romove:
            del deserialized[key]
        return deserialized, execution_time
