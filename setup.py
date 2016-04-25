# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = "0.0.1"

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='duc-newspaper-analysis',
    version=version,
    description="A newspaper analysis project",
    long_description=readme,
    author='Avi Ramu, Indraniel Das',
    author_email='avinash3003@yahoo.co.in, indraniel@gmail.com',
    license=license,
    install_requires=[
        'newspaper',
        'click',
    ],
    entry_points='''
        [console_scripts]
        news-ponder=newsponder.cli:cli
    ''',
    tests_require=['nose>=1.0'],
    test_suite="nose.collector",
    packages=find_packages(exclude=('tests')),
    package_data={ '': ['*.md', 'LICENSE'], },
    include_package_data=True
)
