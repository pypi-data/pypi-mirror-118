#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='telegramlog',
    version='0.0.3',
    author='dean',
    author_email='deanzhou56@gmail.com',
    url='https://github.com/deanzhou69/telegram_log',
    description=u'基于flylog的telegram日志发送',
    packages=find_packages(''),
    # urllib3 应该要依赖
    install_requires=['supervisor', 'flylog'],
)

