#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='tap-darkskyapi',
      version='0.1',
      description='Singer.io tap for extracting historical weather data from the Dark Sky API',
      author='Patrick Tyler Haas',
      url='https://github.com/haaspt/tap-darkskyapi',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['tap_darkskyapi'],
      install_requires=['singer-python>=0.1.0',
                        'backoff==1.3.2',
                        'requests==2.13.0'],
      entry_points='''
          [console_scripts]
          tap-darkskyapi=tap_darkskyapi:main
      ''',
)
