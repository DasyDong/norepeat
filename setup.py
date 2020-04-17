"""Setup script for realpython-reader"""

import os.path
from setuptools import setup, find_packages

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
# https://packaging.python.org/tutorials/packaging-projects/
setup(
    name="norepeat",
    version="1.0.15",
    description="Less codes make more tools",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/DasyDong/python-norepeat",
    author="Dasy Dong",
    author_email="dasydong@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={"console_scripts": ["norepeat=norepeat.__main__:main"]},
)