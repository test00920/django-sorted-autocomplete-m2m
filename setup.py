# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='django-sorted-autocomplete-m2m',
    packages=['sorted-autocomplete-m2m'],
    version='1.0.0',
    author='Simon Lessnick',
    author_email='simon@nixa.ca',
    license='MIT',
    description='ManyToMany widget with autocomplete and sortable items.',
    keywords=['django', 'manytomany', 'm2m', 'auto complete', 'autocomplete', 'sort', 'sorted', 'widget'],
    install_requires=['django', 'django-sortedm2m'],
    url='https://nixa.ca/',
    download_url='https://github.com/nixaio/django-sorted-autocomplete-m2m/tarball/1.0.0',
)