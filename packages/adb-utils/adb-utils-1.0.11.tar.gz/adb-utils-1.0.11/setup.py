# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='adb-utils',
    version='1.0.11',
    author='hakaboom',
    author_email='1534225986@qq.com',
    license='Apache License 2.0',
    description='This is a secondary package of adb',
    inculde_package_data=True,
    url='https://github.com/hakaboom/base_image',
    packages=find_packages(),
    install_requires=["baseImage==1.0.6"],
)