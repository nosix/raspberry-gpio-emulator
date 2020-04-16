from setuptools import setup, find_packages

from RPi import __author__, __version__, __license__

setup(
    name='RPi',
    version=__version__,
    description='RPi.GPIO emulator',
    license=__license__,
    author=__author__,
    author_email='nosix@funmake.jp',
    url='http://nosix.github.io/raspberry-gpio-emulator/',
    keywords='raspberry pi gpio emulator python3',
    packages=find_packages(),
    install_requires=[],
)
