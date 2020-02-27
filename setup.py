#!/usr/bin/env python

from setuptools import setup
from _version import __version__

setup(
    name="monero_scripts",
    version=__version__,
    description="Get Monero meta data from Monero source code files.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Norman Moeschter-Schenck",
    author_email="<norman.moeschter@gmail.com>",
    maintainer="Norman Moeschter-Schenck",
    maintainer_email="<norman.moeschter@gmail.com>",
    url="https://github.com/normoes/monero_scripts",
    download_url=f"https://github.com/normoes/monero_scripts/archive/{__version__}.tar.gz",
    # packages=find_packages(exclude=["tests*"]),
    py_modules=["get_monero_hard_fork_info", "get_monero_seed_nodes"],
    install_requires=["requests>=2.23.0"],
    # extras_require={"test": ["mock", "pytest"]},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
