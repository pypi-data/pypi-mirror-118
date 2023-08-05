from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(
    name="dash-utils",
    version="0.0.1",
    author="Andrew Dircks",
    author_email="andrew@orenda.group",
    description="Utilities for Orenda serverless.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrewdircks/dash-utils",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    install_requires=[], # for use with recursive remote pipreqs to save storage
    packages=['dash_utils'],
    python_requires=">=3.7",
)