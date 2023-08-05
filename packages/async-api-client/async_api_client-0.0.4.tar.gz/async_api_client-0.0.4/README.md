# Async Http Client Base

Python base classes for async http requests.

## Prerequisites

- [Python](https://www.python.org/) > 3.8.0
- [aiohttp](https://docs.aiohttp.org/)

## Features
- `BaseAsyncClient`: base class for async API client
- `BaseAsyncResponse`: base class for response object
- `BaseValidator`: base class for response validators
- `ClientError`, `ClientConnectionError`, `ClientResponseError`: base client exceptions

### Install

- Install package by `pipenv install async-api-client`

## Usage
- Import base classes by `from async_http_client import <class_name>`
- Inherit base classes to build exact API client

## Environment Variables
- `SERVICE_API_URL`: default api root url;
