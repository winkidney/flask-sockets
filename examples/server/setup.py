#!/usr/bin/env python

"""
Flask-Sockets
-------------

Elegant WebSockets for your Flask apps.
"""
from setuptools import setup


setup(
    name='flask_ws',
    version='0.1',
    py_modules=['flask_ws'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
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