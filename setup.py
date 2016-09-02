# Setup
try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

setup(
    name = 'datamountaineer-schemaregistry',
    version = '0.2',
    packages = ['datamountaineer',
                'datamountaineer.schemaregistry',
                'datamountaineer.schemaregistry.serializers',
                'datamountaineer.schemaregistry.client'],

    url = 'https://github.com/datamountaineer/python-serializers',
    download_url='https://github.com/datamountaineer/python-serializers/archive/0.2.tar.gz',

    install_requires = ['fastavro', 'avro-python3'],

    # metadata for upload to PyPI
    author = 'DataMountaineer',
    author_email = 'andrew@datamountaineer.com',
    description = 'DataMountaineer Python 3.5 Confluent Schema Registry Client',
    keywords = 'datamountaineer schema registry schemaregistry confluent avro',
    test_requires = ['unittest2', 'mock']
)
