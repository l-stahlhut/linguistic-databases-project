#!/usr/bin/env python

import os

import setuptools
from setuptools import setup

PROJECT_NAME = "lingu-wordnet-game"


def read(fname):
    """
    Helper to read README
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read().strip()


setup(
    name=PROJECT_NAME,
    version="0.0.1",  # DO NOT EDIT THIS LINE MANUALLY. LET bump2version UTILITY DO IT
    description="Game to learn basic English linguistics using Wordnet",  # keep it short
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="",
    author="Wendy, Laura and Deborah",
    include_package_data=True,
    zip_safe=False,
    packages=[PROJECT_NAME],
    # TODO: check script path
    #scripts=[f"{PROJECT_NAME}"],  # make sure there is a script here!
    author_email='',
    license="MIT",
    keywords=["corpus", "linguistics", "nlp", "wordnet"],
    install_requires=[
        "nltk==3.6.5",
        "wheel==0.37.0",
        "PySimpleGUI"
    ],
)
