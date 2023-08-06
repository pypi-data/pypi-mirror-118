#!/usr/bin/env python

"""Setup `pdfuris`."""

from setuptools import setup

setup(name='pdfuris',
      version='0.1',
      description='extract URIs from PDF',
      author='Michael Hoffman',
      author_email='michael.hoffman@utoronto.ca',
      license='GPLv3',
      package_data={"pdfuris": ["py.typed"]},
      packages=['pdfuris'],
      install_requires=['PyPDF2'],
      python_requires='>=3.6',
      entry_points={
        'console_scripts': ['pdfuris=pdfuris.__main__:main'],
      },
      zip_safe=False)
