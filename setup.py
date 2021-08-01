
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

with open(here / 'requirements.txt') as requirements_file:
    requirements = requirements_file.readlines()

__version__ = '0.0.1'

setup(
    name="atlan-airflow-plugin",
    description="An Airflow plugin to connect with Atlan",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://atlan.com",
    author="Atlan Technologies Pvt Ltd",
    author_email="engineering@atlan.com",
    python_requires=">=3.5",
    classifiers=[
        'Environment :: Plugins',
        'License :: OSI Approved :: Apache Software License',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators"
    ],
    keywords='atlan, airflow, plugin, lineage',
    install_requires=requirements,
    include_package_data=True,
    packages=find_packages(),
    license='Apache License 2.0',
    version=__version__,
)
