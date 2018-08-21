from setuptools import setup


def version():
    with open('VERSION') as f:
        return f.read().strip()


def reqs():
    return [
        line.strip() for line in open('requirements.txt') if not line.startswith('#')
    ]


setup(
    name             = 'avroschemaserializer',
    description      = 'Python 3 Confluent Schema Registry Client',
    version          = version(),
    license          = 'Apache 2.0',
    author           = 'avroschemaserializer',
    author_email     = 'gregory.h.chu@gmail.com',
    keywords         = 'avroschemaserializer schema registry schemaregistry confluent avro',
    install_requires = reqs(),
    tests_require    = ['mock'],
    url              = 'https://github.com/gregchu/python-serializers',
    classifiers      = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],
    packages         = [
        'avroschemaserializer',
        'avroschemaserializer.schemaregistry',
        'avroschemaserializer.schemaregistry.serializers',
        'avroschemaserializer.schemaregistry.client',
        'avroschemaserializer.schemaregistry.tests'
    ],
)
