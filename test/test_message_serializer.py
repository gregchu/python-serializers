import unittest2 as unittest
import data_gen
import struct
import mock_registry
import setup_test_path
from datamountaineer.schemaregistry.serializers import MessageSerializer, Util
from datamountaineer.schemaregistry.client import CachedSchemaRegistryClient

class TestMessageSerializer(unittest.TestCase):

    def setUp(self):
        self.server = mock_registry.ServerThread(9001)
        self.server.start()
        # need to set up the serializer
        self.client = CachedSchemaRegistryClient('http://127.0.0.1:9001')
        self.ms = MessageSerializer(self.client)

    def tearDown(self):
        self.server.shutdown()
        self.server.join()

    def assertMessageIsSame(self, message, expected, schema_id):
        self.assertTrue(message)
        self.assertTrue(len(message) > 5)
        magic,sid = struct.unpack('>bI',message[0:5])
        self.assertEqual(magic, 0)
        self.assertEqual(sid, schema_id)
        decoded = self.ms.decode_message(message)
        self.assertTrue(decoded)
        self.assertEqual(decoded, expected)

    def test_encode_with_schema_id(self):
        adv = Util.parse_schema_from_string(data_gen.ADVANCED_SCHEMA)
        subject = 'test_adv'
        adv_schema_id = self.client.register(subject, adv)
        records = data_gen.ADVANCED_ITEMS
        for record in records:
            message = self.ms.encode_record_with_schema_id(adv_schema_id, adv, record)
            self.assertMessageIsSame(message, record, adv_schema_id)

    def test_encode_record_for_topic(self):
        basic = Util.parse_schema_from_string(data_gen.BASIC_SCHEMA)
        subject = 'test'
        schema_id = self.client.register(subject, basic)

        records = data_gen.BASIC_ITEMS
        for record in records:
            message = self.ms.encode_record_for_topic(subject, record)
            self.assertMessageIsSame(message, record ,schema_id)

    def test_encode_record_with_schema(self):
        basic = Util.parse_schema_from_string(data_gen.BASIC_SCHEMA)
        subject = 'test'
        schema_id = self.client.register(subject, basic)
        records = data_gen.BASIC_ITEMS
        for record in records:
            message = self.ms.encode_record_with_schema(subject, basic, record)
            self.assertMessageIsSame(message, record ,schema_id)

    def test_decode_record(self):
        basic = Util.parse_schema_from_string(data_gen.BASIC_SCHEMA)
        subject = 'test'
        # schema_id = self.client.register(subject, basic)
        records = data_gen.BASIC_ITEMS
        for record in records:
            encoded = self.ms.encode_record_with_schema(subject, basic, record)
            decoded = self.ms.decode_message(encoded)
            self.assertEqual(decoded, record)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestMessageSerializer)
