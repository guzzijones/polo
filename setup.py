import os

from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='polo',
    version='0.1',
    packages=[
        'polo',
    ],
    include_package_data=True,
    description='Python Polo',
    long_description=README,
    url='https://github.com/absortium/poloniex.git',
    author='Andrey Samokhvalov',
    license='MIT',
    author_email='andrew.shvv@gmail.com',
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
            'polo_history = polo.process_historical:main',
            'polo_socket = polo.websocketsubscribe:main'
            ]
        }
)
