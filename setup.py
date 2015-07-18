#!/usr/bin/env python

"""
Flask-Sockets
-------------

Elegant WebSockets for your Flask apps.
"""
from setuptools import setup


setup(
    name='Flask-Sockets-Tornado',
    version='0.1',
    url='https://github.com/winkidney/flask-sockets',
    license='See License',
    author='winkidney',
    author_email='winkidney@gmail.com',
    description='Elegant WebSockets for your Flask apps.Tornado style app included',
    long_description=__doc__,
    py_modules=['flask_sockets'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'gevent>=1.0.0',
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