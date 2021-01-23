#!/usr/bin/env python

# https://packaging.python.org/tutorials/packaging-projects
# docker run -it  -v $PWD:/app  -w /app python:3.8  bash
# python3 -m pip install --user --upgrade twine
# python3 setup.py sdist clean
# python3 setup.py sdist bdist_wheel
# python3 -m twine upload --skip-existing --verbose dist/*

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pbn2html", # Replace with your own username
    version="0.0.28",
    author="Larry Cai",
	author_email='larry.caiyu@gmail.com',
	url='https://github.com/larrycai/pbn2html',
    description="converter from pbn files to html",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    package_data={'pbn2html': ['*.html']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['pbn2html=pbn2html.pbn2html:main'],
    },
    python_requires='>=3.6',
)
