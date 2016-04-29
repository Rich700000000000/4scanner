# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='4scanner',
    version='1.1.0',
    description='4chan threads scanner',
    long_description=long_description,
    url='https://github.com/Lacsap-/4scanner',
    author='lacsap',
    author_email='lacsap@cock.li',
    license='MIT',
    scripts=['bin/4downloader', 'bin/4scanner'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='4chan scan download scrape scraper chan imageboard',
    packages=['scanner'],
    install_requires=['requests'],
)
