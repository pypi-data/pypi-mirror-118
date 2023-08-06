from setuptools import find_packages, setup, os
import pandas
import boto3

with open('README.rst') as f:
    long_description = f.read()

if __name__ == "__main__":

    s3 = boto3.resource('s3')

    if os.path.exists('dist'):
        for filename in os.listdir('dist'):
            os.remove(f'dist/{filename}')
            print(f'{filename} is removed.')

    if os.path.exists('eQmaster/config'):
        for _file in os.listdir('eQmaster/config'):
            if os.path.isfile(f'eQmaster/config/{_file}'):
                obj = s3.Object(
                    bucket_name='ephod-tech.trading-advisor.auto-trade.configuration',
                    key=f'query-master/{_file}'
                ).upload_file(
                    f'eQmaster/config/{_file}'                    
                )
                print(f'[UPLOADED] {_file}')

    setup(
        name='eQmaster',
        packages=find_packages(where='./'),
        version='0.0.68',
        description='Query interface to retrieve data from destinated s3 location with proper authentication',
        author='ava.chen',
        author_email='ava.chen@ephodtech.com',
        license='MIT',
        long_description=long_description,
        long_description_type='text/markdown',
        install_requires=['pandas', 'botocore', 'pyarrow', 'boto3==1.16.1', 'pysolace==0.9.8', 'shioaji', 'ewarrant', 'cryptography', 'fsspec', 's3fs', 'numpy>=1.19.5'],
        setup_requires=['pytest-runner'],
        tests_require=['pytest==4.4.1'],
        test_suite='tests',
        url='https://github.com/avachen2005/ephodtech_query_master'
    )
