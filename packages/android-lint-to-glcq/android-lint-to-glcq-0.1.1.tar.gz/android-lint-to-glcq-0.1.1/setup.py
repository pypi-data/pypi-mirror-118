#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open("README.md").read()

setup(
    name="android-lint-to-glcq",
    version="0.1.1",
    description="Convert android gradle lint outputs to a GitLab valid json code quality result file",
    long_description=readme,
    long_description_content_type='text/markdown',
    author="Vlad Onishchenko",
    author_email="me@vladonishchenko.ru",
    url="https://github.com/STFBEE/android-lint-to-glcq",
    packages=["androidllinttoglqc"],
    package_dir={"android-lint-to-glcq": "androidllinttoglqc"},
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "android-lint-to-glcq = androidllinttoglqc.androidllinttoglqc:main"
        ]
    },
    install_requires=[],
    license="MIT",
    zip_safe=False,
    keywords=["android", "lint", "gitlab", "report", "gradle"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
