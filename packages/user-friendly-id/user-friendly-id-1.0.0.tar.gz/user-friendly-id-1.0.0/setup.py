from setuptools import setup
from pathlib import Path

import ufid

long_description = (Path(__file__).parent / "README.md").read_text()

setup(
    name="user-friendly-id",
    version=ufid.__version__,
    description="Collection of functions to randomly and securely generate commonly used IDs.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="generator, strings, string, str, generate, user, user-friendly, ID, IDs, secure, safe",
    author="Remy Charlot <remy@personalstock.com>",
    author_email="remy@personalstock.com",
    url="https://github.com/lapinvert/user-friendly-id/",
    license="BSD",
    packages=["ufid"],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: BSD License",
        "Environment :: Web Environment",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
    ],
)
