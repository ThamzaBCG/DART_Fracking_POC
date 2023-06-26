from setuptools import setup

with open("./README.md") as fp:
    long_description = fp.read()

with open("./requirements.txt") as fp:
    dependencies = [line.strip() for line in fp.readlines()]

setup(
    name="Repsol Fracking POC",
    version="0.1",
    description="Validate all data source to create Fracking POC for Repsol",
    long_description=long_description,
    author="Cheng Li",
    author_email="li.cheng@bcg.com",
    packages=["src"],
    install_requires=dependencies,
)