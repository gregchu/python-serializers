from setuptools import setup


def version():
    with open('VERSION') as f:
        return f.read().strip()


def readme():
    with open('README.md') as f:
        return f.read()


def reqs():
    return [
        line.strip() for line in open('requirements.txt') if not line.startswith('#')
    ]


setup(
    name             = 'datamountaineer-schemaregistry',
    description      = 'DataMountaineer Python 3 Confluent Schema Registry Client',
    long_description = readme(),
    version          = version(),
    license          = 'Apache 2.0',
    author           = 'DataMountaineer',
    author_email     = 'andrew@datamountaineer.com',
    keywords         = 'datamountaineer schema registry schemaregistry confluent avro',
    install_requires = reqs(),
    tests_require    = ['mock'],
    url              = 'https://github.com/datamountaineer/python-serializers',
    classifiers      = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],
    packages         = [
        'datamountaineer',
        'datamountaineer.schemaregistry',
        'datamountaineer.schemaregistry.serializers',
        'datamountaineer.schemaregistry.client',
        'datamountaineer.schemaregistry.tests'
    ],
)
