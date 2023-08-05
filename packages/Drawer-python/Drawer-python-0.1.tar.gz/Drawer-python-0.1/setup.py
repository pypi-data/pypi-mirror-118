from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1'
DESCRIPTION = 'Rahul'
LONG_DESCRIPTION = 'this package can draw'

# Setting up
setup(
    name="Drawer-python",
    version=VERSION,
    author="Rahul",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['turtle'],
    keywords=['drawer'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)