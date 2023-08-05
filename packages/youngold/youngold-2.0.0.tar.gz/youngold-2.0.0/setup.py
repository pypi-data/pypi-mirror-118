from setuptools import setup, find_packages
import codecs
import os

VERSION = '2.0.0'
DESCRIPTION = 'Compare age with mickzaa'

# Setting up
setup(
    name="youngold",
    version=VERSION,
    author="NeuralNine (Florian Dedov)",
    author_email="<arceus@hotmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)