import os

from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='exchangeapi',
    version='0.1',
    packages=[
        'exchangeapi',
        'exchangeapi.interface'
    ],
    include_package_data=True,
    description='Python Polo',
    long_description=README,
    author='ajonen',
    license='MIT',
    author_email='ajonen@mailcan.com',
    install_requires=[
        'sqlalchemy',
        'psycopg2-binary',
        'websocket-client'
    ],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
    ],
    entry_points={
        'console_scripts':[
            'polo_history = exchangeapi.poloprocess_historical:main',
            'polo_socket = exchangeapi.polowebsocketsubscribe:main'
            ]
        },
    zip_safe=False
)
