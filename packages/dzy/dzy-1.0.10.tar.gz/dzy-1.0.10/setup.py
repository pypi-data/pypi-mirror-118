"""
Setup dzy package
"""
from setuptools import setup, find_packages


setup(
    name="dzy",
    version="1.0.10",
    description="dzy Python package",
    author="dzy",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "freezegun==1.1.0",
        "google-cloud-bigquery==2.23.2",
        "google-cloud-secret-manager==2.6.0",
        "google-cloud-storage==1.41.1",
        "pytz==2021.1",
    ]
)
