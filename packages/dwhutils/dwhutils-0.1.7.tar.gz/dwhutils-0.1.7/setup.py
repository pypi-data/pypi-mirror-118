from pygments.lexer import include
from setuptools import setup, find_packages

setup(
    name='dwhutils',
    version='0.1.7',
    description='get utils for betemporal data warehousing with mariadb',
    author='PoeticDrunkenCat',
    author_email='poeticdrunkencat@gmail.com',
    packages=find_packages(include=['dwhutils']),
    include_package_data=True,
)