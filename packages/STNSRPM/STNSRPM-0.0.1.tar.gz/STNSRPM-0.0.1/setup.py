#!/usr/bin/env python

from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='STNSRPM',
      version='0.0.1',
      description='🌎 Scripts and information to synthetic generation of precipitation based on Point Processes.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Javier Diez Sierra',
      author_email='javier.diez@unican.es',
      maintainer       = 'Manuel del Jesus Peñil',
      maintainer_email = 'manuel.deljesus@unican.es',
      url = 'https://github.com/navass11/STNSRPM/tree/Crear-ejecutable',
      packages = ['NSRP'],
      include_package_data = True,
      python_requires='>=3.7, <4',
      install_requires=[
          'numpy',
          'pandas',
          'scipy',
          'datetime',
          'matplotlib',
          'pyyaml',
      ],
      extras_require={'plotting': ['matplotlib>=2.2.0', 'jupyter','jupyterlab']}
     )