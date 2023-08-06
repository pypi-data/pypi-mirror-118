from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.rst"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Tool for benchmarking inference.'
# LONG_DESCRIPTION = 'A package tool used for benchmarking inference on deep-learning models. The program compares performance on the NCS2 and the CPU using the openvino toolkit.'

# Setting up
setup(
    name="infbench",
    version=VERSION,
    author="Radoslav Ralev)",
    author_email="radoslav.ralev@tum.de",
    description=DESCRIPTION,
    packages=find_packages(),
    keywords=['python', 'deep learning', 'benchmark', 'inference', 'openvino', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
