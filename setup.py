from setuptools import setup, find_packages

with open('README.md', encoding='UTF-8') as f:
    readme = f.read()

setup(
    name='avatarMigrate',
    version='0.1.0',
    description='Move files from one bucket to another on AWS and updates avatar URL within the database',
    long_description = readme,
    author='TJ',
    author_email='tj@mode55.co.uk',
    install_requires=['boto3','botocore','mysql-connector-python'],
    packages=find_packages('src'),
    package_dir={'':'src'},
    entry_points={
        'console_scripts':[
            'avatarMigrate=avatarMigrate.cli:main',

        ]
    }
)