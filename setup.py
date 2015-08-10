#!/usr/bin/env python

"""
Flask-Sockets
-------------

Elegant WebSockets for your Flask apps.
"""
import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


setup(
    name='Flask-Sockets-Tornado',
    version='0.1',
    url='https://github.com/winkidney/flask-sockets',
    license='See License',
    author='winkidney',
    author_email='winkidney@gmail.com',
    description='Elegant WebSockets for your Flask apps.Tornado style app included',
    long_description=__doc__,
    packages=find_packages(here, exclude=['examples']),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'gevent',
        'gevent-websocket'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)