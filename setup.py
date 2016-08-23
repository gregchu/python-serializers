# Setup
try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup
from sys import version_info

import datamountaineer.schemaregistry

install_requires = []

version = '.'.join([str(datamountaineer.schemaregistry.__version__[i]) for i in range(3)])

setup(
    name = 'datamountaineer-schemaregistry',
    version = version,
    packages = ['datamountaineer',
                'datamountaineer.schemaregistry',
                'datamountaineer.schemaregistry.serializers',
                'datamountaineer.schemaregistry.client'],


    # Project uses simplejson, so ensure that it gets installed or upgraded
    # on the target machine
    install_requires = ['fastavro'],

    # metadata for upload to PyPI
    author = 'Verisign',
    author_email = 'vsrtc-dev@verisign.com',
    description = 'Confluent Schema Registry lib',
    keywords = 'datamountaineer schema registry schemaregistry',
    # extras_require = {
    #     'fastavro': ['fastavro'],
    # },
    test_requires = ['unittest2']
)
