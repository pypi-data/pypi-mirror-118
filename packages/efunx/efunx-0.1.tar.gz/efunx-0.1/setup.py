from setuptools import setup,find_packages
import os

setup(name='efunx',
      version='0.1',
      description='A simple tool for graph-based data persistence',
      author='Giuseppe Romano',
      author_email='romanog@mit.edu',
      install_requires=['dill','numpy','deepdiff','networkx','matplotlib','mpi4py'],
      classifiers=['Programming Language :: Python :: 3.6'],
      license='GPLv3',\
      packages = ['efunx'],
      entry_points = {'console_scripts':['efunx=efunx.__main__:main']},
      zip_safe=False)
