import struct
import unittest

from avroschemaserializer.schemaregistry.tests import data_gen
from avroschemaserializer.schemaregistry.client import SchemaRegistryClient
from avroschemaserializer.schemaregistry.serializers import (MessageSerializer,
                                                        Util,
                                                        SerializerError)

from mock import MagicMock


class TestMessageSerializer(unittest.TestCase):

    def setUp(self):
        self.subject = 'test_adv'
        self.schema = Util.parse_schema_from_string(data_gen.ADVANCED_SCHEMA)

        self.client = SchemaRegistryClient('http://127.0.0.1:9001')
        self.client.register = MagicMock(return_value=1)
        self.client.get_by_id = MagicMock(retrun_value=self.schema)
        self.client.get_latest_schema = MagicMock(return_value=(1, self.schema, 1))
        self.client.get_version = MagicMock(return_value=1)
        self.ms = MessageSerializer(self.client, fast_avro=True)
        self.msslow = MessageSerializer(self.client, fast_avro=False)
        self.ms.get_schema = MagicMock(return_value=self.schema)
        self.msslow.get_schema = MagicMock(return_value=self.schema)

    def assertMessageIsSame(self, message, expected, schema_id):
        self.assertTrue(message)
        self.assertTrue(len(message) > 5)
        magic, sid = struct.unpack('>bI', message[0:5])
        self.assertEqual(magic, 0)
        self.assertEqual(sid, schema_id)
        decoded = self.ms.decode_message(message)
        self.assertTrue(decoded)
        self.assertEqual(decoded, expected)
        decoded = self.msslow.decode_message(message)
        self.assertTrue(decoded)
        self.assertEqual(decoded, expected)

    def test_encode_with_schema_id(self):
        adv_schema_id = self.client.register(self.subject, self.schema)
        records = data_gen.ADVANCED_ITEMS
        for record in records:
            message = self.ms.encode_record_with_schema_id(adv_schema_id, self.schema, record)
            self.assertMessageIsSame(message, record, adv_schema_id)
            message = self.msslow.encode_record_with_schema_id(adv_schema_id, self.schema, record)
            self.assertMessageIsSame(message, record, adv_schema_id)

    def test_encode_record_for_topic(self):
        schema_id = self.client.register(self.subject, self.schema)
        records = data_gen.ADVANCED_ITEMS
        for record in records:
            message = self.ms.encode_record_for_topic(self.subject, record)
            self.assertMessageIsSame(message, record, schema_id)
            message = self.msslow.encode_record_for_topic(self.subject, record)
            self.assertMessageIsSame(message, record, schema_id)

    def test_encode_record_with_schema(self):
        schema_id = self.client.register(self.subject, self.schema)
        records = data_gen.ADVANCED_ITEMS
        for record in records:
            message = self.ms.encode_record_with_schema(self.subject, self.schema, record)
            self.assertMessageIsSame(message, record, schema_id)
            message = self.msslow.encode_record_with_schema(self.subject, self.schema, record)
            self.assertMessageIsSame(message, record, schema_id)

    def test_decode_record(self):
        records = data_gen.ADVANCED_ITEMS
        for record in records:
            encoded = self.ms.encode_record_with_schema(self.subject, self.schema, record)
            decoded = self.ms.decode_message(encoded)
            self.assertEqual(decoded, record)
            encoded = self.msslow.encode_record_with_schema(self.subject, self.schema, record)
            decoded = self.msslow.decode_message(encoded)
            self.assertEqual(decoded, record)

    def test_bad_input(self):
        adv_schema_id = self.client.register(self.subject, self.schema)

        with self.assertRaises(SerializerError):
            self.ms.encode_record_with_schema_id(adv_schema_id, self.schema, 'notadict')

        with self.assertRaises(SerializerError):
            self.ms.encode_record_with_schema_id(adv_schema_id, self.schema, ['notadict'])

        with self.assertRaises(SerializerError):
            self.ms.encode_record_for_topic(self.subject, 'notadict')

        with self.assertRaises(SerializerError):
            self.ms.encode_record_for_topic(self.subject, ['notadict'])

        with self.assertRaises(SerializerError):
            self.ms.encode_record_with_schema(self.subject, self.schema, 'notadict')

        with self.assertRaises(SerializerError):
            self.ms.encode_record_with_schema(self.subject, self.schema, ['notadict'])
