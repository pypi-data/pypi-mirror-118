from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Handwritten Notes'
LONG_DESCRIPTION = 'A package for making handwritten notes'

# Setting up
setup(
    name="Handwritten Notes",
    version=VERSION,
    author="Aryan Abhay Verma",
    author_email="aryanabhayv@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['students', 'penned', 'handwritten', 'notes', 'aryan abhay'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)