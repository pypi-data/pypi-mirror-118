from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding = 'utf-8') as f:
    long_description = f.read()

setup(
    name = 'find_primes',
    version = '2.0.1',
    author = 'JamesJ',
    author_email = 'GGJamesQQ@yeah.net',
    description = 'A module for finding primes',
    classifiers = [
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Mathematics'
    ],
    url = 'https://github.com/git4robot/pypi_find_primes',
    packages = ['find_primes'],
    long_description = long_description,
    long_description_content_type = 'text/markdown',
)
#python_requires = '>=3.6'