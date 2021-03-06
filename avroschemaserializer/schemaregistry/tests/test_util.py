import unittest

from avro import schema

from avroschemaserializer.schemaregistry.tests import data_gen

from avroschemaserializer.schemaregistry.client import Util


class TestUtil(unittest.TestCase):

    def test_schema_from_string(self):
        parsed = Util.parse_schema_from_string(data_gen.BASIC_SCHEMA)
        self.assertTrue(isinstance(parsed, schema.Schema))

    def test_schema_from_file(self):
        parsed = Util.parse_schema_from_file(data_gen.get_schema_path('adv_schema.avsc'))
        self.assertTrue(isinstance(parsed, schema.Schema))
