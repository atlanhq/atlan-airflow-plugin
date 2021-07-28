
from setuptools import setup, find_packages

requirements = ["requests~=2.23.0", "apache-airflow>=1.10.0"]

setup_requirements = []

__version__ = '0.0.1'

setup(
    author="Atlan Technologies Pvt Ltd",
    author_email="eengineering@atlan.com",
    python_requires=">=3.5",
    classifiers=[
        'Environment :: Plugins'
        'License :: OSI Approved :: Apache Software License',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators"
    ],
    description="An Airflow plugin to connect with Atlan",
    install_requires=requirements,
    include_package_data=True,
    name="atlan-airflow-plugin",
    packages=find_packages(),
    setup_requires=setup_requirements,
    url="https://github.com/atlanhq/atlan-airflow-plugin",
    license='Apache License 2.0',
    version=__version__,
    zip_safe=False,
)
