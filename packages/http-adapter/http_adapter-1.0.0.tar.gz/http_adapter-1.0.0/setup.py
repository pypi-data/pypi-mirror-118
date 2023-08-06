# -*- coding: utf-8 -*-

from __future__ import print_function
from setuptools import setup, find_packages

setup(
    name="http_adapter",
    version="1.0.0",
    author="ZhouHanLin",
    author_email="zhhlvip@sina.com",
    description="Python Framework.",
    license="MIT",
    url="",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=True,
    platforms='any',
    install_requires=[
        'requests>=2.26.0',
        'urllib3>=1.26.6'
    ],
)
