"""
Setup dzy package
"""
from setuptools import setup, find_packages


# gather install requirements
req = []
with open("requirements.txt", "r") as fh:
    for line in fh:
        req.append(line.strip())


setup(
    name="dzy",
    version="1.0.6",
    description="dzy Python package",
    author="dzy",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=req
)
