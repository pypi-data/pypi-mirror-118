from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="unswamp",
    version="1.0.0.0",
    author="Stefan Kaspar",
    author_email="me@fullbox.ch",
    description="A python package for data quality unit testing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/debugair/unswamp",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    package_data={
    
    },
)
