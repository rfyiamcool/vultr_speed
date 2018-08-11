# coding: utf-8

import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
        name = "vultr_speed",
        version = "0.5",
        author = "ruifengyun",
        author_email = "rfyiamcool@163.com",
        description = "get fast vultr node for you",
        license = "MIT",
        keywords = ["vultr","fengyun"],
        url = "https://github.com/rfyiamcool/vultr_speed",
        long_description = read('README.md'),
        install_requires=['bs4','requests'],
        packages = ['vultr_speed'],
        entry_points={
        'console_scripts': [
            'vultr_speed = vultr_speed.main:main',
            ]
        },
        classifiers = [
             'Development Status :: 2 - Pre-Alpha',
             'Intended Audience :: Developers',
             'License :: OSI Approved :: MIT License',
             'Programming Language :: Python :: 2.7',
             'Programming Language :: Python :: 3.4',
             'Topic :: Software Development :: Libraries :: Python Modules',
        ]
)

