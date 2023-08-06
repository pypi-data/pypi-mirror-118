from setuptools import setup, find_packages

setup(
    name='s3db',
    description='A simple document db using s3 buckets',
    version='1.0.3',
    author='Filipe Alves',
    author_email='filipe.alvesdefernando@gmail.com',
    install_requires=[
        'asyncio',
        'boto3',
        'bson',
    ],
    packages=find_packages(),
    url='https://github.com/filipealvesdef/s3db',
    zip_zafe=False,
)
