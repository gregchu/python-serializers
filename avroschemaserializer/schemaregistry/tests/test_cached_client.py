import time
import unittest

from avroschemaserializer.schemaregistry.tests import data_gen
from avroschemaserializer.schemaregistry.tests import mock_registry

from avroschemaserializer.schemaregistry.client import SchemaRegistryClient
from avroschemaserializer.schemaregistry.serializers import Util


class TestCacheSchemaRegistryClient(unittest.TestCase):

    def setUp(self):
        self.server = mock_registry.ServerThread(9001)
        self.server.start()
        time.sleep(1)
        self.client = SchemaRegistryClient('http://127.0.0.1:9001')

    def tearDown(self):
        self.server.shutdown()
        self.server.join()

    def assertLatest(self, meta_tuple, sid, schema, version):
        self.assertNotEqual(sid, -1)
        self.assertNotEqual(version, -1)
        self.assertEqual(meta_tuple[0], sid)
        self.assertEqual(meta_tuple[1], schema)
        self.assertEqual(meta_tuple[2], version)

    def test_register(self):
        parsed = Util.parse_schema_from_string(data_gen.BASIC_SCHEMA)
        client = self.client
        schema_id = client.register('test', parsed)
        self.assertTrue(schema_id == 1)
        self.assertEqual(len(client.id_to_schema), 1)

    def test_multi_subject_register(self):
        parsed = Util.parse_schema_from_string(data_gen.BASIC_SCHEMA)
        client = self.client
        schema_id = client.register('test', parsed)
        self.assertTrue(schema_id == 1)

        # register again under different subject
        dupe_id = client.register('other', parsed)
        self.assertEqual(schema_id, dupe_id)
        self.assertEqual(len(client.id_to_schema), 1)

    def test_dupe_register(self):
        parsed = Util.parse_schema_from_string(data_gen.BASIC_SCHEMA)
        subject = 'test'
        client = self.client
        schema_id = client.register(subject, parsed)
        self.assertTrue(schema_id == 1)
        latest = client.get_latest_schema(subject)

        # register again under same subject
        dupe_id = client.register(subject, parsed)
        self.assertEqual(schema_id, dupe_id)
        dupe_latest = client.get_latest_schema(subject)
        self.assertEqual(latest, dupe_latest)

    def test_getters(self):
        parsed = Util.parse_schema_from_string(data_gen.BASIC_SCHEMA)
        client = self.client
        subject = 'test'
        version = client.get_version(subject, parsed)
        self.assertEqual(version, 1)
        schema = client.get_by_id(1)
        # self.assertEqual(schema, parsed)
        latest = client.get_latest_schema(subject)
        self.assertEqual(latest, (1, schema, 1))

        # register
        schema_id = client.register(subject, parsed)
        latest = client.get_latest_schema(subject)
        version = client.get_version(subject, parsed)
        self.assertLatest(latest, schema_id, parsed, version)

        fetched = client.get_by_id(schema_id)
        self.assertEqual(fetched, parsed)
