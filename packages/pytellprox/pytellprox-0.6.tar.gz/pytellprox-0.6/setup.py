#!/usr/bin/env python3

import os
from distutils.core import setup

setup(name='pytellprox',
      version='0.6',
      license='GPLv3',
      description='Python bindings for the Tellprox API',
      long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'r').read(),
      author='Christian Bryn',
      author_email='chr.bryn@gmail.com',
      url='https://github.com/epleterte/pytellprox',
      platform='Linux',
      #py_modules=['tellprox'],
      packages=['tellprox'],
      install_requires=[
        'requests'
      ]
     )
