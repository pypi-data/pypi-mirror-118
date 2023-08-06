# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="rrcf-outlier-detector-MA",
    version="0.1.0",
    description="Demo library",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://www.moodysanalytics.com/",
    author="Roberto Martinez Cruz",
    author_email="roberto.martinezcruz@moodys.com",
    license="Moody's Analytics",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["RRCF_Outlier_Detection"],
    include_package_data=True,
    install_requires=["numpy", 'pandas', 'rrcf', 'sklearn']
)
