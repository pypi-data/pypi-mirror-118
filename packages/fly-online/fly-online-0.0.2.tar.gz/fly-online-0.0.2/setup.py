# -*- coding: UTF-8 -*-
from setuptools import setup

setup(
    name='fly-online',
    version='0.0.2',
    author='QiangZiBro',
    author_email='qiangzibro@gmail.com',
    description=u'Never get offline in NBU',
    packages=['fly_online'],
    install_requires=['selenium'],
    entry_points={
        'console_scripts': [
            'fly=fly_online:fly'
        ]
    }
)
