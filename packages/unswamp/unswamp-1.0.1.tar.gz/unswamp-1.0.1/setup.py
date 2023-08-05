# https://github.com/pypa/sampleproject/blob/main/setup.py
from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="unswamp",
    version="1.0.1",
    author="Stefan Kaspar",
    author_email="me@fullbox.ch",
    description="A python package for data quality unit testing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/debugair/unswamp",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="data, quality, test, unittest",
    python_requires=">=3.6",
    package_data={
    
    },
    project_urls={  
        'Bug Reports': 'https://gitlab.com/debugair/unswamp',
        'Source': 'https://gitlab.com/debugair/unswamp',
    },
)
