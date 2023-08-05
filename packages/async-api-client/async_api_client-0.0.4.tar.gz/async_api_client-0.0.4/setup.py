from setuptools import find_packages, setup

setup(
    name="async_api_client",
    version="0.0.4",
    author="Dmytro Kharchenko",
    author_email="dmitriy.kharchenko@chimplie.com",
    description="Package for base classes for asycn http client to inherit from.",
    url="https://github.com/chimplie/async-http-client",
    packages=find_packages(include=['async_http_client']),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'aiohttp',
    ],
    python_requires=">=3.8",
)
