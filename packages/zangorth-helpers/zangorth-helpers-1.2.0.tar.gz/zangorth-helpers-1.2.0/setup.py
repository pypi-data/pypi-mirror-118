import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()

setup(
      name='zangorth-helpers',
      version='1.2.0',
      description='Collection of helper functions for my projects',
      long_description=README,
      long_description_content_type='text/markdown',
      url='https://github.com/Zangorth/Helpers',
      author='Zangorth',
      py_modules=['SGA', 'arbitraryNN', 
                  'cross_validation', 'ramsey'],
      install_requires=open(r'C:\Users\Samuel\Google Drive\Portfolio\Helpers\requirements.txt', 'r').read().split('\n')[0:-1]
      )