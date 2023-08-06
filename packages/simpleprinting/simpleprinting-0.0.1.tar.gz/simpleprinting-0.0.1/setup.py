import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

setup(
    name="simpleprinting",
    version="0.0.1",
    author="Nikola Markovic",
    author_email="navarrete.wen@gmail.com",
    description="An easy and funny example of a Python package",
    long_description="simpleprinting just prinet hello world",
    long_description_content_type="text/markdown",
    url="https://github.com/mwpnava/Python-Code/tree/master/My_own_Python_package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)